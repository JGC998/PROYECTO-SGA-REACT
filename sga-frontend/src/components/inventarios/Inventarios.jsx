import { useState, useEffect } from 'react'
import { getInventarios, crearInventario, actualizarLineaInventario, cerrarInventario } from '../../api/inventarios'
import { getZonas } from '../../api/almacenes' // En este backend mock, habría que conseguir las zonas
import { getProductos } from '../../api/productos'
import { useAuth } from '../../hooks/useAuth'
import EstadoCarga from '../comunes/EstadoCarga'
import EstadoVacio from '../comunes/EstadoVacio'
import Modal from '../comunes/Modal'
import Badge from '../comunes/Badge'
import toast from 'react-hot-toast'
import { format } from 'date-fns'

export default function Inventarios() {
    const { usuario, isAdmin, isSupervisor } = useAuth()
    const [inventarios, setInventarios] = useState([])
    const [cargando, setCargando] = useState(true)
    const [activa, setActiva] = useState(null)
    
    // Modal Creación
    const [modalCrear, setModalCrear] = useState(false)
    const [formInv, setFormInv] = useState({ zona_id: '' })
    const [zonas, setZonas] = useState([])
    const [productos, setProductos] = useState([])

    const cargar = async () => {
        setCargando(true)
        try {
            const [invs, prods] = await Promise.all([
                getInventarios(),
                getProductos(0, 1000)
            ])
            setInventarios(invs)
            setProductos(prods.data.productos)
            if (activa) {
                setActiva(invs.find(i => i.id === activa.id))
            }
        } catch(e) {
            toast.error("Error al cargar rondas de inventario")
        } finally {
            setCargando(false)
        }
    }

    const cargarFormDependencias = async () => {
        try {
            // Mock: Idealmente llamaríamos a todos los almacenes o zonas, 
            // no tenemos GET /zonas sin almacenId. Lo saltaremos o simularemos para simplificar
            // por ahora dejamos el form manual sin zonas si falla
        } catch(e) {}
    }

    useEffect(() => { 
        cargar() 
        cargarFormDependencias()
    }, [])

    const handleCrear = async (e) => {
        e.preventDefault()
        try {
            const res = await crearInventario({
                codigo: `INV-${Date.now()}`,
                responsable_id: usuario.id,
                zona_id: formInv.zona_id ? parseInt(formInv.zona_id) : null,
                lineas: [] // Inicialmente vacío. El backend o supervisor añadirá las líneas a contar, o lo haremos ciego 100%.
            })
            toast.success("Ronda de Inventario creada")
            setModalCrear(false)
            cargar()
        } catch(err) {
            toast.error("Error al crear inventario")
        }
    }

    const guardarLineaFisica = async (lineaId, cantFisica) => {
        try {
            await actualizarLineaInventario(activa.id, lineaId, cantFisica)
            toast.success("Conteo registrado")
            cargar()
        } catch(err) {
            toast.error(err?.response?.data?.detail || "Error al actualizar")
        }
    }

    const handleCerrar = async () => {
        if(!window.confirm("¿Seguro que deseas CERRAR el inventario? Se forzará la creación de movimientos de ajuste por cada diferencia.")) return
        try {
            await cerrarInventario(activa.id)
            toast.success("Inventario cerrado y diferencias reguladas con éxito")
            cargar()
        } catch(err) {
            toast.error(err?.response?.data?.detail || "Error al cerrar")
        }
    }

    return (
        <div className="fade-in" style={{ height: 'calc(100vh - 120px)', display: 'flex', flexDirection: 'column' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', flexShrink: 0 }}>
                <div>
                    <h1 className="page-title">Recuentos de Inventario</h1>
                    <p className="page-subtitle">Verifica el stock real contra el stock del SGA para corregir discrepancias.</p>
                </div>
                {(isAdmin || isSupervisor) && (
                    <button className="btn-accent" onClick={() => { setFormInv({zona_id:''}); setModalCrear(true); }}>
                        + Nueva Ronda de Conteo
                    </button>
                )}
            </div>

            <div style={{ display: 'flex', gap: '24px', flex: 1, minHeight: 0 }}>
                {/* Lista de Recuentos */}
                <div className="card fade-in" style={{ width: '350px', overflowY: 'auto', padding: '16px 0' }}>
                    <div style={{ padding: '0 16px 16px 16px', fontWeight: 'bold', borderBottom: '1px solid var(--border)' }}>
                        Histórico de Auditorías
                    </div>
                    {cargando && !inventarios.length ? <EstadoCarga /> : (
                        <div style={{ display: 'flex', flexDirection: 'column', padding: '8px' }}>
                            {inventarios.map(i => (
                                <button 
                                    key={i.id}
                                    style={{
                                        padding: '16px',
                                        marginBottom: '8px',
                                        background: activa?.id === i.id ? 'var(--surface-hover)' : 'var(--surface)',
                                        border: activa?.id === i.id ? '1px solid var(--accent)' : '1px solid var(--border)',
                                        borderRadius: '8px',
                                        cursor: 'pointer',
                                        textAlign: 'left'
                                    }}
                                    onClick={() => setActiva(i)}
                                >
                                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                                        <span style={{ fontWeight: 'bold' }}>{i.codigo}</span>
                                        {i.estado === 'cerrado' ? <Badge texto="Cerrado" variante="success" /> : <Badge texto="Abierto" variante="warning" />}
                                    </div>
                                    <div style={{ fontSize: '0.85rem', color: 'var(--text-400)' }}>
                                        {format(new Date(i.creado_en), 'dd/MM/yyyy HH:mm')}
                                    </div>
                                </button>
                            ))}
                        </div>
                    )}
                </div>

                {/* Vista Detalle (Conteo) */}
                <div className="card fade-in" style={{ flex: 1, overflowY: 'auto' }}>
                    {!activa ? (
                        <EstadoVacio titulo="Ningún inventario seleccionado" descripcion="Selecciona un inventario a la izquierda para continuar." />
                    ) : (
                        <div>
                            <div style={{ borderBottom: '1px solid var(--border)', paddingBottom: '16px', marginBottom: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                                <div>
                                    <h2>Detalle: {activa.codigo}</h2>
                                    <p style={{ margin: 0, color: 'var(--text-300)' }}>Modo de Conteo Físico</p>
                                </div>
                                <div>
                                    {activa.estado === 'abierto' && (isAdmin || isSupervisor) && activa.lineas.length > 0 && (
                                        <button className="btn-accent" onClick={handleCerrar}>🔒 Aplicar Cierre y Discrepancias</button>
                                    )}
                                </div>
                            </div>

                            {activa.lineas.length === 0 ? (
                                <EstadoVacio 
                                    titulo="Ronda vacía" 
                                    descripcion="El administrador debe volcar lineas previas para habilitar el conteo. (La API lo preparó pero el formulario UI no provee carga automática en este MVP)" 
                                />
                            ) : (
                                <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                                    <thead style={{ borderBottom: '1px solid var(--border)' }}>
                                        <tr>
                                            <th style={{ padding: '12px' }}>Ubicación</th>
                                            <th style={{ padding: '12px' }}>Producto</th>
                                            <th style={{ padding: '12px', textAlign: 'right' }}>Cant. Sistema</th>
                                            <th style={{ padding: '12px', textAlign: 'right' }}>Cant. Contada Físicamente</th>
                                            <th style={{ padding: '12px', textAlign: 'right' }}>Descuadre</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {activa.lineas.map(l => {
                                            const pr = productos.find(p => p.id === l.producto_id)
                                            return (
                                                <tr key={l.id} style={{ borderBottom: '1px solid var(--border)' }}>
                                                    <td style={{ padding: '12px' }}>Ubic ID: {l.ubicacion_id}</td>
                                                    <td style={{ padding: '12px' }}>
                                                        <div style={{ fontWeight: 'bold' }}>{pr?.sku || l.producto_id}</div>
                                                        <div style={{ fontSize: '0.8rem', color: 'var(--text-400)' }}>{pr?.nombre}</div>
                                                    </td>
                                                    <td style={{ padding: '12px', textAlign: 'right', color: 'var(--text-400)' }}>
                                                        {l.cantidad_sistema}
                                                    </td>
                                                    <td style={{ padding: '12px', textAlign: 'right' }}>
                                                        {activa.estado === 'abierto' ? (
                                                            <input 
                                                                type="number" min="0" 
                                                                defaultValue={l.cantidad_fisica === null ? '' : l.cantidad_fisica}
                                                                onBlur={e => {
                                                                    if(e.target.value !== '') guardarLineaFisica(l.id, parseInt(e.target.value))
                                                                }}
                                                                onKeyDown={e => {
                                                                    if(e.key === 'Enter' && e.target.value !== '') guardarLineaFisica(l.id, parseInt(e.target.value))
                                                                }}
                                                                style={{ width: '80px', textAlign: 'center', fontWeight: 'bold' }}
                                                            />
                                                        ) : (
                                                            <strong style={{ color: 'var(--text-100)' }}>{l.cantidad_fisica ?? 'No contado'}</strong>
                                                        )}
                                                    </td>
                                                    <td style={{ padding: '12px', textAlign: 'right', fontWeight: 'bold', color: l.diferencia === 0 ? 'var(--green)' : l.diferencia ? 'var(--red)' : '' }}>
                                                        {l.diferencia !== null ? (l.diferencia > 0 ? `+${l.diferencia}` : l.diferencia) : '-'}
                                                    </td>
                                                </tr>
                                            )
                                        })}
                                    </tbody>
                                </table>
                            )}
                        </div>
                    )}
                </div>
            </div>

            <Modal isOpen={modalCrear} onClose={() => setModalCrear(false)} titulo="Planificar Ronda de Inventario">
                <form onSubmit={handleCrear} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    <div>
                        <label>Zona Específica (Opcional)</label>
                        <select value={formInv.zona_id} onChange={e => setFormInv({...formInv, zona_id: e.target.value})}>
                            <option value="">Todo el Almacén Ppal.</option>
                        </select>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px', marginTop: '16px' }}>
                        <button type="submit" className="btn-accent">Iniciar Auditoría Ciega</button>
                    </div>
                </form>
            </Modal>
        </div>
    )
}
