import { useEffect, useState } from 'react'
import { getMovimientos, crearMovimientoInterno } from '../../api/movimientos'
import { getProductos } from '../../api/productos'
import { getStock } from '../../api/stock'
import { getAlmacenes, getZonas } from '../../api/almacenes' 
import Modal from '../comunes/Modal'
import toast from 'react-hot-toast'

const PAGE_SIZE = 50

export default function Movimientos() {
    const [movimientos, setMovimientos] = useState([])
    const [total, setTotal] = useState(0)
    const [cargando, setCargando] = useState(true)
    const [error, setError] = useState(null)
    const [pagina, setPagina] = useState(0)
    const [filtroTipo, setFiltroTipo] = useState('')

    // Form data
    const [modalAbierto, setModalAbierto] = useState(false)
    const [productos, setProductos] = useState([])
    const [stockDir, setStockDir] = useState([]) // [ {producto_id, ubicacion_id, cantidad, ubicacion:{codigo} } ] 
    
    const [formMov, setFormMov] = useState({
        producto_id: '',
        ubicacion_origen_id: '',
        ubicacion_destino_id: '',
        cantidad: 1,
        motivo: ''
    })

    const cargar = async (pag = 0, tipo = filtroTipo) => {
        setCargando(true)
        setError(null)
        try {
            const params = { skip: pag * PAGE_SIZE, limit: PAGE_SIZE }
            if (tipo) params.tipo = tipo
            const res = await getMovimientos(params)
            setMovimientos(res.data.movimientos)
            setTotal(res.data.total)
        } catch (err) {
            setError('No se pudo cargar el historial de movimientos.')
        } finally {
            setCargando(false)
        }
    }

    const cargarFormData = async () => {
        try {
            const [prods, sts] = await Promise.all([getProductos(0, 1000), getStock()])
            setProductos(prods.data.productos)
            setStockDir(sts)
        } catch(e) {
            toast.error("Error al cargar dependencias de stock")
        }
    }

    useEffect(() => { 
        cargar(0) 
        cargarFormData()
    }, [])

    const totalPaginas = Math.ceil(total / PAGE_SIZE)

    const cambiarFiltro = (tipo) => {
        setFiltroTipo(tipo)
        setPagina(0)
        cargar(0, tipo)
    }

    const irPagina = (nuevaPag) => {
        setPagina(nuevaPag)
        cargar(nuevaPag)
    }

    const formatFecha = (iso) => {
        const d = new Date(iso)
        return d.toLocaleString('es-ES', {
            day: '2-digit', month: '2-digit', year: 'numeric',
            hour: '2-digit', minute: '2-digit'
        })
    }

    const handleCrearTraspaso = async (e) => {
        e.preventDefault()
        try {
            await crearMovimientoInterno({
                producto_id: parseInt(formMov.producto_id),
                ubicacion_origen_id: parseInt(formMov.ubicacion_origen_id),
                ubicacion_destino_id: parseInt(formMov.ubicacion_destino_id),
                cantidad: parseInt(formMov.cantidad),
                motivo: formMov.motivo
            })
            toast.success("Traspaso completado")
            setModalAbierto(false)
            cargar(0) // refrescar movs
            cargarFormData() // refrescar stock actual
        } catch (e) {
            toast.error(e.response?.data?.detail || "Error al realizar traspaso")
        }
    }

    return (
        <div className="fade-in">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                <div>
                    <h1 className="page-title">Movimientos y Traspasos</h1>
                    <p className="page-subtitle">Historial de todo lo que entra, sale o se mueve.</p>
                </div>
                <button className="btn-accent" onClick={() => {
                    setFormMov({producto_id:'', ubicacion_origen_id:'', ubicacion_destino_id:'', cantidad:1, motivo:''});
                    setModalAbierto(true);
                }}>
                    🔄 Nuevo Traspaso (M. Interno)
                </button>
            </div>

            <div className="filtros-movimientos card" style={{ padding: '16px', marginBottom: '24px' }}>
                <button className={filtroTipo === '' ? 'btn-filtro active' : 'btn-filtro'} onClick={() => cambiarFiltro('')}>
                    Todos
                </button>
                <button className={filtroTipo === 'entrada' ? 'btn-filtro active' : 'btn-filtro'} onClick={() => cambiarFiltro('entrada')}>
                    ↑ Entradas
                </button>
                <button className={filtroTipo === 'salida' ? 'btn-filtro active' : 'btn-filtro'} onClick={() => cambiarFiltro('salida')}>
                    ↓ Salidas
                </button>
                <button className={filtroTipo === 'transferencia' ? 'btn-filtro active' : 'btn-filtro'} onClick={() => cambiarFiltro('transferencia')}>
                    🔄 Traspasos Internos
                </button>
            </div>

            {cargando && <p className="estado-info">Cargando movimientos…</p>}
            {!cargando && error && <p className="estado-error">{error}</p>}

            {!cargando && !error && (
                <div className="card fade-in">
                    <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                        <thead>
                            <tr style={{ borderBottom: '1px solid var(--border)' }}>
                                <th style={{ padding: '12px' }}>Fecha</th>
                                <th style={{ padding: '12px' }}>Producto</th>
                                <th style={{ padding: '12px' }}>Tipo</th>
                                <th style={{ padding: '12px' }}>Cantidad</th>
                                <th style={{ padding: '12px' }}>Antes → Después</th>
                                <th style={{ padding: '12px' }}>Motivo</th>
                            </tr>
                        </thead>
                        <tbody>
                            {movimientos.length > 0 ? (
                                movimientos.map(m => (
                                    <tr key={m.id} style={{ borderBottom: '1px solid var(--surface-hover)' }}>
                                        <td style={{ fontSize: '0.85rem', color: 'var(--text-300)', padding: '12px' }}>
                                            {formatFecha(m.fecha)}
                                        </td>
                                        <td style={{ padding: '12px' }}>
                                            <strong style={{ color: 'var(--text-100)' }}>{m.producto_sku}</strong><br />
                                            <span style={{ fontSize: '0.85rem', color: 'var(--text-400)' }}>{m.producto_nombre}</span>
                                        </td>
                                        <td style={{ padding: '12px' }}>
                                            <span className={`badge badge-${m.tipo}`}>
                                                {m.tipo === 'entrada' ? '↑ Entrada' : m.tipo === 'salida' ? '↓ Salida' : '🔄 Transferencia'}
                                            </span>
                                        </td>
                                        <td style={{ fontWeight: 'bold', padding: '12px', color: 'var(--text-100)' }}>
                                            {m.tipo === 'entrada' ? '+' : m.tipo === 'salida' ? '-' : ''}{m.cantidad}
                                        </td>
                                        <td style={{ color: 'var(--text-400)', fontSize: '0.9rem', padding: '12px' }}>
                                            {m.cantidad_anterior} → {m.cantidad_nueva}
                                        </td>
                                        <td style={{ color: 'var(--text-300)', fontSize: '0.85rem', padding: '12px' }}>
                                            {m.motivo || '—'}
                                        </td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan="6" style={{ textAlign: 'center', padding: '24px', color: 'var(--text-400)' }}>
                                        No hay movimientos registrados aún.
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>

                    {totalPaginas > 1 && (
                        <div className="paginacion" style={{ padding: '16px', borderTop: '1px solid var(--border)' }}>
                            <button className="btn-outline" disabled={pagina === 0} onClick={() => irPagina(pagina - 1)}>← Anterior</button>
                            <span>Página {pagina + 1} de {totalPaginas} ({total} movimientos)</span>
                            <button className="btn-outline" disabled={pagina >= totalPaginas - 1} onClick={() => irPagina(pagina + 1)}>Siguiente →</button>
                        </div>
                    )}
                </div>
            )}

            {/* Modal Traspaso */}
            <Modal isOpen={modalAbierto} onClose={() => setModalAbierto(false)} titulo="Mover Stock / Traspaso">
                 <form onSubmit={handleCrearTraspaso} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    <div>
                        <label>Producto a Mover</label>
                        <select required value={formMov.producto_id} onChange={e => setFormMov({...formMov, producto_id: e.target.value, ubicacion_origen_id: ''})}>
                            <option value="">Selecciona Producto...</option>
                            {productos.map(p => <option key={p.id} value={p.id}>{p.sku} - {p.nombre}</option>)}
                        </select>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                        <div>
                            <label>Desde: Ubicación Origen</label>
                            <select required value={formMov.ubicacion_origen_id} onChange={e => setFormMov({...formMov, ubicacion_origen_id: e.target.value})}>
                                <option value="">Selecciona Origen...</option>
                                {stockDir.filter(s => s.producto_id === parseInt(formMov.producto_id) && s.cantidad > 0).map(st => (
                                    <option key={st.id} value={st.ubicacion_id}>Ubic {st.ubicacion?.codigo} (Max disp: {st.cantidad})</option>
                                ))}
                            </select>
                        </div>
                        <div>
                            <label>Hacia: Ubicación Destino</label>
                            {/* En la vida real, el destino podría ser cualquier ubicación existente. 
                                Como el GET /ubicaciones no existe suelto aún (lo unimos a zonas), usamos un text input o listamos las del backend.
                                Como tenemos un dropdown de ubicaciones activas en stockDir, podemos permitir mover a una existente,
                                pero eso limitaría mover a sitios nuevos vacíos. Vamos a simplificar usando las mismas ubicaciones generadas.  */}
                            <input 
                                required type="number" placeholder="ID de Ubicación (Ej: 1)" 
                                value={formMov.ubicacion_destino_id} 
                                onChange={e => setFormMov({...formMov, ubicacion_destino_id: e.target.value})} 
                                title="En la versión completa habría un selector de árbol de Almacén > Zona > Ubicación libre"
                            />
                        </div>
                    </div>

                    <div>
                        <label>Cantidad (ud/kg)</label>
                        <input required type="number" min="1" value={formMov.cantidad} onChange={e => setFormMov({...formMov, cantidad: e.target.value})} />
                    </div>
                    
                    <div>
                        <label>Motivo</label>
                        <input value={formMov.motivo} onChange={e => setFormMov({...formMov, motivo: e.target.value})} placeholder="Ej. Reorganización" />
                    </div>

                    <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px', marginTop: '16px' }}>
                        <button type="button" className="btn-ghost" onClick={() => setModalAbierto(false)}>Cancelar</button>
                        <button type="submit" className="btn-accent">Confirmar Traspaso</button>
                    </div>
                 </form>
            </Modal>
        </div>
    )
}
