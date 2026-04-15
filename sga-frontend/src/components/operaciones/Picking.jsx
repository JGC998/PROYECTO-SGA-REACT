import { useState, useEffect } from 'react'
import { getPicking, crearPicking, asignarPicking, recogerLineaPicking, completarPicking } from '../../api/picking'
import { getUsuarios } from '../../api/usuarios'
import { getProductos } from '../../api/productos'
import { getStock } from '../../api/stock'
import EstadoCarga from '../comunes/EstadoCarga'
import Modal from '../comunes/Modal'
import Badge from '../comunes/Badge'
import toast from 'react-hot-toast'
import { useAuth } from '../../hooks/useAuth'
import { format } from 'date-fns'

export default function Picking() {
    const { usuario, isAdmin, isSupervisor } = useAuth()
    const [ordenes, setOrdenes] = useState([])
    const [cargando, setCargando] = useState(true)
    const [activa, setActiva] = useState(null)
    
    // Para administradores/supervisores: Crear Orden / Asignar
    const [usuarios, setUsuarios] = useState([])
    const [productosCat, setProductosCat] = useState([])
    const [stockDir, setStockDir] = useState([])
    const [modalCrear, setModalCrear] = useState(false)
    const [formOrden, setFormOrden] = useState({ notas: '', prioridad: 1, operario_id: '' })
    const [formLineas, setFormLineas] = useState([])

    const cargarDatos = async () => {
        try {
            setCargando(true)
            const [ords, usrs, prods, sts] = await Promise.all([
                getPicking(),
                (isAdmin || isSupervisor) ? getUsuarios() : Promise.resolve([]),
                (isAdmin || isSupervisor) ? getProductos(0,1000) : Promise.resolve({data:{productos:[]}}),
                (isAdmin || isSupervisor) ? getStock() : Promise.resolve([])
            ])
            
            // Si es operario, solo ve las suyas o las no asignadas. Si es admin, ve todas.
            if (isAdmin || isSupervisor) {
                setOrdenes(ords)
                setUsuarios(usrs)
                setProductosCat(prods.data.productos)
                setStockDir(sts.stock || [])
            } else {
                // Para operario: filtrar por su email (que es ahora el operario_cod)
                setOrdenes(ords.filter(o => o.operario_cod === usuario.email || !o.operario_cod))
            }

            if (activa) {
                const refreshed = ords.find(o => o.id === activa.id)
                setActiva(refreshed)
            }
        } catch(e) {
            toast.error("Error al cargar órdenes de Picking")
        } finally {
            setCargando(false)
        }
    }

    useEffect(() => { cargarDatos() }, [])

    const handleCrear = async (e) => {
        e.preventDefault()
        if (formLineas.length === 0) return toast.error('Añade líneas al picking')
        try {
            await crearPicking({
                // operario_cod es string, no int
                operario_cod: formOrden.operario_id || null,
                prioridad: parseInt(formOrden.prioridad),  // prioridad sí es int
                notas: formOrden.notas,
                lineas: formLineas.map(l => ({
                    // articulo_cod es string (ARTCOD), no int
                    articulo_cod: l.producto_id,
                    cantidad_solicitada: parseFloat(l.cantidad_solicitada) || 0,
                    // ubicacion_origen es string (UBICON), no int
                    ubicacion_origen: l.ubicacion_id || null
                }))
            })
            toast.success('Orden de Picking generada')
            setModalCrear(false)
            cargarDatos()
        } catch (err) {
            toast.error('Error al crear Orden')
        }
    }

    const tomarOrden = async (orden) => {
        try {
            // usuario.email o usuario.cod_lin es el cod string; usamos email como fallback
            await asignarPicking(orden.id, usuario.email || String(usuario.id))
            toast.success('Te has asignado esta orden')
            cargarDatos()
        } catch (e) {
            toast.error('No se pudo asignar la orden')
        }
    }

    const marcarRecogida = async (lineaId, cant) => {
        try {
            await recogerLineaPicking(activa.id, lineaId, cant)
            toast.success("Línea actualizada")
            cargarDatos()
        } catch(e) {
            toast.error("Error: " + (e.response?.data?.detail || e.message))
        }
    }

    const finalizarOrden = async () => {
        if(!window.confirm("¿Dar por finalizado el picking? El stock físico se descontará ahora mismo.")) return
        try {
            await completarPicking(activa.id)
            toast.success("Picking completado correctamente")
            cargarDatos()
        } catch(e) {
            toast.error("Error al finalizar: " + (e.response?.data?.detail || e.message))
        }
    }

    return (
        <div className="fade-in" style={{ height: 'calc(100vh - 120px)', display: 'flex', flexDirection: 'column' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', flexShrink: 0 }}>
                <div>
                    <h1 className="page-title">Preparación de Pedidos (Picking)</h1>
                    <p className="page-subtitle">Zafarrancho de salida: Asignación y comprobación táctil en estantería</p>
                </div>
                {(isAdmin || isSupervisor) && (
                    <button className="btn-accent" onClick={() => {
                        setFormOrden({ notas: '', prioridad: 1, operario_id: '' })
                        setFormLineas([])
                        setModalCrear(true)
                    }}>
                        + Nueva Orden de Picking
                    </button>
                )}
            </div>

            <div style={{ display: 'flex', gap: '24px', flex: 1, minHeight: 0 }}>
                {/* Lista de Órdenes */}
                <div className="card fade-in" style={{ width: '350px', overflowY: 'auto', padding: '16px 0' }}>
                    <div style={{ padding: '0 16px 16px 16px', fontWeight: 'bold', borderBottom: '1px solid var(--border)' }}>
                        Cola de Trabajo
                    </div>
                    {cargando && !ordenes.length ? <EstadoCarga /> : (
                        <div style={{ display: 'flex', flexDirection: 'column', padding: '8px' }}>
                            {ordenes.map(o => (
                                <div 
                                    key={o.id}
                                    style={{
                                        padding: '16px',
                                        marginBottom: '8px',
                                        background: activa?.id === o.id ? 'var(--surface-hover)' : 'var(--surface)',
                                        border: activa?.id === o.id ? '1px solid var(--accent)' : '1px solid var(--border)',
                                        borderRadius: '8px',
                                        cursor: 'pointer'
                                    }}
                                    onClick={() => setActiva(o)}
                                >
                                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                                        <span style={{ fontWeight: 'bold', color: o.prioridad === 2 ? 'var(--red)' : 'var(--text-100)' }}>
                                            {o.prioridad === 2 ? '🔥 ' : ''}{o.codigo}
                                        </span>
                                        {o.estado === 'completado' ? <Badge texto="Hecho" variante="success" /> : 
                                         o.estado === 'en_proceso' ? <Badge texto="En Curso" variante="warning" /> :
                                         <Badge texto="Pendiente" variante="default" />}
                                    </div>
                                    <div style={{ fontSize: '0.85rem', color: 'var(--text-400)' }}>
                                        Asignado a: {o.operario_cod || 'Nadie (Libre)'}
                                    </div>
                                    {o.estado === 'pendiente' && !o.operario_id && (
                                        <button className="btn-outline" style={{ width: '100%', marginTop: '12px', padding: '4px' }} onClick={(e) => {
                                            e.stopPropagation(); tomarOrden(o);
                                        }}>
                                            Tomar Tarea
                                        </button>
                                    )}
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                {/* Ejecución de Picking */}
                <div className="card fade-in" style={{ flex: 1, overflowY: 'auto', position: 'relative' }}>
                    {!activa ? (
                        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-400)' }}>
                            Selecciona una orden de trabajo de la izquierda.
                        </div>
                    ) : (
                        <div>
                            <div style={{ borderBottom: '1px solid var(--border)', paddingBottom: '16px', marginBottom: '16px' }}>
                                <h2>Ejecución de {activa.codigo}</h2>
                                <p style={{ margin: 0, color: 'var(--text-300)' }}>{activa.notas || "Sin instrucciones especiales."}</p>
                            </div>

                            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                                {activa.lineas.map(l => (
                                    <div key={l.id} style={{ 
                                        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                                        padding: '16px', border: '1px solid var(--border)', borderRadius: '8px',
                                        background: l.estado === 'completada' ? 'var(--surface-hover)' : 'var(--surface)',
                                        opacity: l.estado === 'completada' ? 0.6 : 1
                                    }}>
                                        <div style={{ flex: 1 }}>
                                            <div style={{ fontSize: '1.2rem', fontWeight: 'bold', marginBottom: '4px' }}>
                                                {l.articulo_cod || l.producto_id}
                                            </div>
                                            <div style={{ display: 'flex', gap: '12px', color: 'var(--text-300)', fontSize: '0.9rem' }}>
                                                <span>Ubicación: <strong>{l.ubicacion_origen || 'Cualquiera'}</strong></span>
                                                <span>Estado: <Badge texto={l.estado} variante={l.estado === 'completada' ? 'success' : 'warning'} /></span>
                                            </div>
                                        </div>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '24px' }}>
                                            <div style={{ textAlign: 'center' }}>
                                                <div style={{ fontSize: '0.8rem', color: 'var(--text-400)' }}>A RECOGER</div>
                                                <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{l.cantidad_solicitada}</div>
                                            </div>
                                            
                                            {activa.estado !== 'completado' && (
                                                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                                    <input 
                                                        type="number" 
                                                        defaultValue={l.cantidad_recogida} 
                                                        style={{ width: '80px', height: '40px', fontSize: '1.2rem', textAlign: 'center' }}
                                                        onBlur={(e) => marcarRecogida(l.id, parseFloat(e.target.value))}
                                                    />
                                                    <button className="btn-accent" style={{ height: '40px' }} onClick={() => marcarRecogida(l.id, l.cantidad_solicitada)}>
                                                        Todo OK
                                                    </button>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                ))}
                            </div>

                            {/* Panel inferior completado */}
                            {activa.estado !== 'completado' && activa.operario_cod === (usuario.email || String(usuario.id)) && (
                                <div style={{ position: 'sticky', bottom: 0, padding: '24px', background: 'var(--bg-900)', borderTop: '1px solid var(--border)', marginTop: '24px', textAlign: 'right' }}>
                                    <button className="btn-accent" style={{ fontSize: '1.1rem', padding: '12px 24px' }} onClick={finalizarOrden}>
                                        🏁 Finalizar Picking y Reservar Stock
                                    </button>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>

            {/* Modal Creacion Admin */}
            {(isAdmin || isSupervisor) && (
                <Modal isOpen={modalCrear} onClose={() => setModalCrear(false)} titulo="Planificar Picking">
                    <form onSubmit={handleCrear} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                            <div>
                                <label>Prioridad</label>
                                <select value={formOrden.prioridad} onChange={e => setFormOrden({...formOrden, prioridad: e.target.value})}>
                                    <option value="1">Normal (1)</option>
                                    <option value="2">Alta/Urgente (2)</option>
                                </select>
                            </div>
                            <div>
                                <label>Asignado A (Opcional)</label>
                                <select value={formOrden.operario_id} onChange={e => setFormOrden({...formOrden, operario_id: e.target.value})}>
                                    <option value="">A la piscina / Libre</option>
                                    {usuarios.map(u => <option key={u.id} value={u.id}>{u.nombre} ({u.rol})</option>)}
                                </select>
                            </div>
                        </div>
                        <div>
                            <label>Notas de Orden</label>
                            <input value={formOrden.notas} onChange={e => setFormOrden({...formOrden, notas: e.target.value})} placeholder="Pedidos de Amazon, Exportación..." />
                        </div>
                        
                        <div style={{ borderTop: '1px solid var(--border)', paddingTop: '16px', marginTop: '8px' }}>
                            <h4>Líneas a Recoger</h4>
                            {formLineas.map((l, idx) => (
                                <div key={idx} style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr auto', gap: '8px', marginBottom: '8px' }}>
                                    <select required value={l.producto_id} onChange={e => {
                                        const nl = [...formLineas]; nl[idx].producto_id = e.target.value; setFormLineas(nl)
                                    }}>
                                        <option value="">Producto...</option>
                                    {productosCat.map(p => <option key={p.sku} value={p.sku}>{p.sku}</option>)}
                                    </select>
                                    
                                    <input type="number" required min="1" placeholder="Cant." value={l.cantidad_solicitada} onChange={e => {
                                        const nl = [...formLineas]; nl[idx].cantidad_solicitada = e.target.value; setFormLineas(nl)
                                    }}/>

                                    <select value={l.ubicacion_id} onChange={e => {
                                        const nl = [...formLineas]; nl[idx].ubicacion_id = e.target.value; setFormLineas(nl)
                                    }}>
                                        <option value="">Cualquier Ubic.</option>
                                        {/* stockDir contiene entradas con articulo_cod (str) */}
                                        {stockDir.filter(s => s.articulo_cod === l.producto_id).map(st => (
                                            <option key={`${st.articulo_cod}-${st.ubicacion}`} value={st.ubicacion}>
                                                Ubic {st.ubicacion} (Stock: {st.cantidad})
                                            </option>
                                        ))}
                                    </select>
                                    <button type="button" className="btn-ghost" style={{ color: 'var(--red)' }} onClick={() => setFormLineas(formLineas.filter((_, i) => i !== idx))}>X</button>
                                </div>
                            ))}
                            <button type="button" className="btn-outline" onClick={() => setFormLineas([...formLineas, {producto_id: '', cantidad_solicitada: '', ubicacion_id: ''}])} style={{ marginTop: '8px' }}>
                                + Línea de Picking
                            </button>
                        </div>

                        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px', marginTop: '16px' }}>
                            <button type="submit" className="btn-accent">Lanzar Orden</button>
                        </div>
                    </form>
                </Modal>
            )}
        </div>
    )
}
