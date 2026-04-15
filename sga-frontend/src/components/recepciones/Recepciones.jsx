import { useState, useEffect } from 'react'
import { getRecepciones, crearRecepcion, actualizarLineaRecepcion, confirmarRecepcion } from '../../api/recepciones'
import { getProveedores } from '../../api/catalog'
import { getProductos } from '../../api/productos'
import EstadoCarga from '../comunes/EstadoCarga'
import EstadoVacio from '../comunes/EstadoVacio'
import Modal from '../comunes/Modal'
import Badge from '../comunes/Badge'
import toast from 'react-hot-toast'
import { format } from 'date-fns'

export default function Recepciones() {
    const [recepciones, setRecepciones] = useState([])
    const [proveedores, setProveedores] = useState([])
    const [productosCat, setProductosCat] = useState([])
    
    const [cargando, setCargando] = useState(true)
    const [activa, setActiva] = useState(null) // Recepción seleccionada en el detalle
    
    const [formCabecera, setFormCabecera] = useState({ proveedor_id: '', notas: '' })
    const [formLineas, setFormLineas] = useState([]) // [{articulo_cod, cantidad_esperada, ubicacion_destino, lote}]
    const [modalAbierto, setModalAbierto] = useState(false)

    const cargarDatos = async () => {
        try {
            setCargando(true)
            const [recs, provs, prods] = await Promise.all([
                getRecepciones(),
                getProveedores(),
                getProductos(0, 1000)
            ])
            setRecepciones(recs)
            setProveedores(provs.data.proveedores || [])
            setProductosCat(prods.data.productos)
            
            if (activa) {
                const refreshed = recs.find(r => r.id === activa.id)
                setActiva(refreshed)
            }
        } catch (err) {
            toast.error('Error al cargar las recepciones')
        } finally {
            setCargando(false)
        }
    }

    useEffect(() => { cargarDatos() }, [])


    const handleCrear = async (e) => {
        e.preventDefault()
        if (formLineas.length === 0) return toast.error('La recepción debe tener al menos 1 línea')
        try {
            await crearRecepcion({
                // proveedor_cod es string (CLICOD), no int
                proveedor_cod: formCabecera.proveedor_id || null,
                notas: formCabecera.notas,
                lineas: formLineas.map(l => ({
                    // articulo_cod es string (ARTCOD), no int
                    articulo_cod: l.producto_id,
                    cantidad_esperada: parseFloat(l.cantidad_esperada) || 0,
                    ubicacion_destino: l.ubicacion_destino || '',
                    lote: l.lote || ''
                }))
            })
            toast.success('Albaran de recepción creado')
            setModalAbierto(false)
            cargarDatos()
        } catch (err) {
            toast.error('Error creando la recepción')
        }
    }

    const handleActualizarLinea = async (lineaId, nuevaCantidad) => {
        try {
            await actualizarLineaRecepcion(activa.id, lineaId, nuevaCantidad)
            toast.success("Línea actualizada")
            cargarDatos()
        } catch (err) {
            toast.error("Error actualizando cantidad")
        }
    }

    const handleConfirmar = async () => {
        if (!window.confirm("¿Confirmar recepción? Esto ingresará las cantidades recibidas al stock físico y no se puede deshacer.")) return
        try {
            await confirmarRecepcion(activa.id)
            toast.success("Cantidades ingresadas al stock. Recepción completada.")
            cargarDatos()
        } catch (err) {
            toast.error(err.response?.data?.detail || "Error confirmando recepción")
        }
    }

    return (
        <div className="fade-in" style={{ height: 'calc(100vh - 120px)', display: 'flex', flexDirection: 'column' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', flexShrink: 0 }}>
                <div>
                    <h1 className="page-title">Entradas (Recepciones)</h1>
                    <p className="page-subtitle">Gestiona la llegada de mercancía y el ingreso al stock</p>
                </div>
                <button className="btn-accent" onClick={() => {
                    setFormCabecera({ proveedor_id: '', notas: '', codigo: '' })
                    setFormLineas([])
                    setModalAbierto(true)
                }}>
                    + Nuevo Albarán de Entrada
                </button>
            </div>

            <div style={{ display: 'flex', gap: '24px', flex: 1, minHeight: 0 }}>
                {/* Panel Lados: Lista */}
                <div className="card fade-in" style={{ width: '350px', overflowY: 'auto', padding: '16px 0' }}>
                    <div style={{ padding: '0 16px 16px 16px', fontWeight: 'bold', borderBottom: '1px solid var(--border)', marginBottom: '16px' }}>
                        Albaranes en Curso / Histórico
                    </div>
                    {cargando && !recepciones.length ? <EstadoCarga /> : (
                        <div style={{ display: 'flex', flexDirection: 'column' }}>
                            {recepciones.map(r => (
                                <button 
                                    key={r.id}
                                    onClick={() => setActiva(r)}
                                    style={{
                                        padding: '16px',
                                        textAlign: 'left',
                                        background: activa?.id === r.id ? 'var(--surface-hover)' : 'transparent',
                                        border: 'none',
                                        borderLeft: activa?.id === r.id ? '4px solid var(--accent)' : '4px solid transparent',
                                        borderBottom: '1px solid var(--border)',
                                        cursor: 'pointer',
                                        transition: 'all 0.2s',
                                        display: 'flex',
                                        flexDirection: 'column',
                                        gap: '8px'
                                    }}
                                >
                                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                                        <span style={{ fontWeight: 'bold', color: 'var(--text-100)' }}>{r.codigo}</span>
                                        {r.estado === 'completada' ? <Badge texto="Completada" variante="success" /> : <Badge texto="Pdte." variante="warning" />}
                                    </div>
                                    <div style={{ fontSize: '0.85rem', color: 'var(--text-300)' }}>
                                        {format(new Date(r.creado_en), 'dd MMM yyyy HH:mm')}
                                    </div>
                                    <div style={{ fontSize: '0.9rem', color: 'var(--text-200)' }}>
                                        {r.lineas.length} líneas documentadas
                                    </div>
                                </button>
                            ))}
                            {recepciones.length === 0 && <p style={{ padding: '24px', textAlign: 'center', color: 'var(--text-400)' }}>No hay recepciones registradas.</p>}
                        </div>
                    )}
                </div>

                {/* Panel Central: Detalle y Ejecución */}
                <div className="card fade-in" style={{ flex: 1, overflowY: 'auto' }}>
                    {!activa ? (
                        <EstadoVacio titulo="Ninguna recepción seleccionada" descripcion="Selecciona un albarán de la lista para gestionar su entrada o inspeccionar su estado." />
                    ) : (
                        <div>
                            <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border)', paddingBottom: '24px', marginBottom: '24px' }}>
                                <div>
                                    <h2 style={{ margin: '0 0 8px 0', fontSize: '1.4rem' }}>{activa.codigo}</h2>
                                    <p style={{ margin: 0, color: 'var(--text-300)' }}>{activa.notas || "Sin notas de proveedor"}</p>
                                </div>
                                <div style={{ textAlign: 'right' }}>
                                    {activa.estado === 'pendiente' && (
                                        <button className="btn-accent" onClick={handleConfirmar}>✓ Confirmar e Ingresar Stock</button>
                                    )}
                                    {activa.estado === 'completada' && (
                                        <p style={{ color: 'var(--green)', fontWeight: 'bold', margin: 0 }}>✓ Stock Ingresado</p>
                                    )}
                                </div>
                            </div>

                            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                                <thead>
                                    <tr style={{ borderBottom: '1px solid var(--border)' }}>
                                        <th style={{ padding: '12px', color: 'var(--text-300)' }}>Producto (SKU)</th>
                                        <th style={{ padding: '12px', color: 'var(--text-300)', textAlign: 'right' }}>Pedidas</th>
                                        <th style={{ padding: '12px', color: 'var(--text-300)', textAlign: 'right' }}>Recibidas Físicas</th>
                                        <th style={{ padding: '12px', color: 'var(--text-300)' }}>Estado Línea</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {activa.lineas.map(l => {
                                        // Buscar el producto por articulo_cod (str)
                                        const prod = productosCat.find(p => p.sku === l.articulo_cod)
                                        return (
                                            <tr key={l.id} style={{ borderBottom: '1px solid var(--border)', background: l.cantidad_recibida !== l.cantidad_esperada && activa.estado === 'completada' ? 'var(--red-bg)' : 'transparent' }}>
                                                <td style={{ padding: '12px' }}>
                                                    <div style={{ fontWeight: '500', color: 'var(--text-100)', fontFamily: 'monospace' }}>{l.articulo_cod}</div>
                                                    <div style={{ fontSize: '0.85rem', color: 'var(--text-400)' }}>{prod?.nombre || ''}</div>
                                                </td>
                                                <td style={{ padding: '12px', textAlign: 'right', fontWeight: 'bold' }}>{l.cantidad_esperada}</td>
                                                <td style={{ padding: '12px', textAlign: 'right' }}>
                                                    {activa.estado === 'pendiente' ? (
                                                        <input 
                                                            type="number" 
                                                            style={{ width: '80px', textAlign: 'right' }} 
                                                            defaultValue={l.cantidad_recibida}
                                                            onBlur={(e) => handleActualizarLinea(l.id, parseFloat(e.target.value))}
                                                            onKeyDown={(e) => {
                                                                if(e.key === 'Enter') handleActualizarLinea(l.id, parseFloat(e.target.value))
                                                            }}
                                                        />
                                                    ) : (
                                                        <span style={{ fontWeight: 'bold', color: l.cantidad_recibida < l.cantidad_esperada ? 'var(--red)' : 'var(--text-100)' }}>
                                                            {l.cantidad_recibida}
                                                        </span>
                                                    )}
                                                </td>
                                                <td style={{ padding: '12px' }}>
                                                    {l.estado === 'recibida' ? <Badge texto="OK" variante="success" /> : 
                                                     l.estado === 'discrepancia' ? <Badge texto="Discrepancia" variante="danger" /> :
                                                     <Badge texto="Pendiente de Cierre" variante="default" />}
                                                </td>
                                            </tr>
                                        )
                                    })}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            </div>

            {/* Modal Creación de Albarán */}
            <Modal isOpen={modalAbierto} onClose={() => setModalAbierto(false)} titulo="Registrar Pedido de Compra / Albarán">
                <form onSubmit={handleCrear} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                        <div>
                            <label>Código Albarán / Factura</label>
                            <input value={formCabecera.codigo} onChange={e => setFormCabecera({...formCabecera, codigo: e.target.value})} placeholder="Auto si se deja vacío" />
                        </div>
                        <div>
                            <label>Proveedor</label>
                            <select required value={formCabecera.proveedor_id} onChange={e => setFormCabecera({...formCabecera, proveedor_id: e.target.value})}>
                                    <option value="">Selecciona Proveedor</option>
                                    {/* p.id es CLICOD (string) */}
                                    {proveedores.map(p => <option key={p.id} value={p.id}>{p.nombre}</option>)}
                            </select>
                        </div>
                    </div>
                    <div>
                        <label>Notas de Entrada</label>
                        <input value={formCabecera.notas} onChange={e => setFormCabecera({...formCabecera, notas: e.target.value})} placeholder="Ej: Mercancía prioritaria..." />
                    </div>

                    <div style={{ borderTop: '1px solid var(--border)', paddingTop: '16px', marginTop: '8px' }}>
                        <h4>Líneas de Producto</h4>
                        {formLineas.map((l, idx) => (
                            <div key={idx} style={{ display: 'flex', gap: '12px', marginBottom: '8px' }}>
                                <select 
                                    required 
                                    style={{ flex: 1 }}
                                    value={l.producto_id}
                                    onChange={e => {
                                        const nl = [...formLineas]; nl[idx].producto_id = e.target.value; setFormLineas(nl)
                                    }}
                                >
                                    <option value="">Seleccionar Producto...</option>
                                    {productosCat.map(p => <option key={p.sku} value={p.sku}>{p.sku} - {p.nombre}</option>)}
                                </select>
                                <input 
                                    type="number" 
                                    required 
                                    min="1" 
                                    placeholder="Cant ESPERADA" 
                                    style={{ width: '150px' }}
                                    value={l.cantidad_esperada}
                                    onChange={e => {
                                        const nl = [...formLineas]; nl[idx].cantidad_esperada = e.target.value; setFormLineas(nl)
                                    }}
                                />
                                <button type="button" className="btn-ghost" style={{ color: 'var(--red)' }} onClick={() => {
                                    setFormLineas(formLineas.filter((_, i) => i !== idx))
                                }}>X</button>
                            </div>
                        ))}
                        <button type="button" className="btn-outline" onClick={() => setFormLineas([...formLineas, {producto_id: '', cantidad_esperada: ''}])} style={{ marginTop: '8px', padding: '6px 12px', fontSize: '0.8rem' }}>
                            + Añadir Línea
                        </button>
                    </div>

                    <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px', marginTop: '16px' }}>
                        <button type="button" className="btn-ghost" onClick={() => setModalAbierto(false)}>Cancelar</button>
                        <button type="submit" className="btn-accent">Registrar Documento</button>
                    </div>
                </form>
            </Modal>
        </div>
    )
}
