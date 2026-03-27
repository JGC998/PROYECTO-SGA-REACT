import { useState, useEffect } from 'react'
import { getAlmacenes, getZonas, createZona, createUbicacion } from '../../api/almacenes'
import EstadoCarga from '../comunes/EstadoCarga'
import Modal from '../comunes/Modal'
import toast from 'react-hot-toast'

export default function GestionAlmacenes() {
    const [almacenes, setAlmacenes] = useState([])
    const [zonas, setZonas] = useState([])
    const [almacenActivo, setAlmacenActivo] = useState(null)
    const [cargando, setCargando] = useState(true)

    // Form modals
    const [modalZona, setModalZona] = useState(false)
    const [modalUbicacion, setModalUbicacion] = useState(false)
    const [zonaParaUbicacion, setZonaParaUbicacion] = useState(null)

    const [formZona, setFormZona] = useState({ nombre: '', descripcion: '', activo: true })
    const [formUbic, setFormUbic] = useState({ codigo: '', descripcion: '', capacidad_max: 100, activo: true })

    const cargarDatos = async () => {
        try {
            setCargando(true)
            const res = await getAlmacenes()
            setAlmacenes(res)
            if (res.length > 0) {
                setAlmacenActivo(res[0].id)
                const resZonas = await getZonas(res[0].id)
                setZonas(resZonas)
            }
        } catch (err) {
            toast.error("Error al cargar almacenes")
        } finally {
            setCargando(false)
        }
    }

    useEffect(() => { cargarDatos() }, [])

    const recargarZonas = async (aId = almacenActivo) => {
        try {
            const z = await getZonas(aId)
            setZonas(z)
        } catch(e) {}
    }

    const guardarZona = async (e) => {
        e.preventDefault()
        try {
            await createZona(almacenActivo, formZona)
            toast.success("Zona agregada")
            setModalZona(false)
            recargarZonas()
        } catch (err) {
            toast.error(err.response?.data?.detail || "Error al crear zona")
        }
    }

    const guardarUbicacion = async (e) => {
        e.preventDefault()
        try {
            await createUbicacion({ 
                ...formUbic, 
                zona_id: zonaParaUbicacion,
                codigo: formUbic.codigo.toUpperCase()
            })
            toast.success("Estantería / Ubicación registrada")
            setModalUbicacion(false)
        } catch (err) {
            toast.error(err.response?.data?.detail || "Error al crear ubicación")
        }
    }

    return (
        <div className="fade-in">
            <h1 className="page-title">Configuración Logística</h1>
            <p className="page-subtitle">Define almacenes, zonas y las ubicaciones (racks/estanterías) donde guardar Stock</p>

            {cargando ? <EstadoCarga /> : (
                <div style={{ display: 'flex', gap: '24px' }}>
                    
                    <div style={{ width: '250px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
                        <div style={{ fontWeight: '600', color: 'var(--text-300)', textTransform: 'uppercase', fontSize: '0.8rem' }}>
                            Red de Almacenes
                        </div>
                        {almacenes.map(a => (
                            <button 
                                key={a.id} 
                                className={almacenActivo === a.id ? "btn-accent" : "card"} 
                                style={{ padding: '16px', textAlign: 'left', border: almacenActivo === a.id ? 'none' : '1px solid var(--border)' }}
                                onClick={() => {
                                    setAlmacenActivo(a.id)
                                    recargarZonas(a.id)
                                }}
                            >
                                <div style={{ fontWeight: 'bold' }}>{a.nombre}</div>
                                <div style={{ fontSize: '0.8rem', opacity: 0.8 }}>{a.direccion}</div>
                            </button>
                        ))}
                    </div>

                    <div className="card fade-in" style={{ flex: 1 }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '24px' }}>
                            <h2 style={{ margin: 0 }}>Zonas del Almacén</h2>
                            <button className="btn-accent" onClick={() => { setFormZona({nombre:'', descripcion:'', activo:true}); setModalZona(true) }}>
                                + Añadir Zona
                            </button>
                        </div>

                        {zonas.length === 0 ? (
                            <p style={{ color: 'var(--text-400)' }}>Este almacén aún no tiene zonas configuradas.</p>
                        ) : (
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                                {zonas.map(z => (
                                    <div key={z.id} style={{ border: '1px solid var(--border)', borderRadius: '8px', padding: '16px', background: 'var(--surface)' }}>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                                            <div>
                                                <h3 style={{ margin: '0 0 4px 0', color: 'var(--text-100)' }}>{z.nombre}</h3>
                                                <p style={{ margin: 0, fontSize: '0.85rem', color: 'var(--text-400)' }}>{z.descripcion || 'Sin descripción'}</p>
                                            </div>
                                            <button className="btn-outline" onClick={() => { setZonaParaUbicacion(z.id); setFormUbic({codigo:'', descripcion:'', capacidad_max:100, activo:true}); setModalUbicacion(true); }}>
                                                + Configurar Hueco/Rack
                                            </button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* Modal Zona */}
            <Modal isOpen={modalZona} onClose={() => setModalZona(false)} titulo="Nueva Zona / Sector">
                <form onSubmit={guardarZona} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    <div>
                        <label>Nombre de Zona</label>
                        <input required value={formZona.nombre} onChange={e => setFormZona({...formZona, nombre: e.target.value})} placeholder="Ej: Refrigerados, Pasillo A" />
                    </div>
                    <div>
                        <label>Descripción</label>
                        <input value={formZona.descripcion} onChange={e => setFormZona({...formZona, descripcion: e.target.value})} />
                    </div>
                    <button type="submit" className="btn-accent" style={{ marginTop: '10px' }}>Crear Zona</button>
                </form>
            </Modal>

            {/* Modal Ubicacion */}
            <Modal isOpen={modalUbicacion} onClose={() => setModalUbicacion(false)} titulo="Nuevo Hueco de Estantería">
                <form onSubmit={guardarUbicacion} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    <div>
                        <label>Código Ubicación *</label>
                        <input required value={formUbic.codigo} onChange={e => setFormUbic({...formUbic, codigo: e.target.value})} placeholder="Ej: A-01-01" />
                    </div>
                    <div>
                        <label>Capacidad (ud/kg recomendada)</label>
                        <input type="number" required min="1" value={formUbic.capacidad_max} onChange={e => setFormUbic({...formUbic, capacidad_max: parseInt(e.target.value)})} />
                    </div>
                    <div>
                        <label>Descripción (Opcional)</label>
                        <input value={formUbic.descripcion} onChange={e => setFormUbic({...formUbic, descripcion: e.target.value})} placeholder="Estantería baja, pallets..." />
                    </div>
                    <button type="submit" className="btn-accent" style={{ marginTop: '10px' }}>Registrar Ubicación en Zona</button>
                </form>
            </Modal>
        </div>
    )
}
