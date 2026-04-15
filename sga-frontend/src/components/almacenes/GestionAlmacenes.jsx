import { useState, useEffect } from 'react'
import { getAlmacenes, getUbicacionesAlmacen } from '../../api/almacenes'
import { createUbicacion } from '../../api/ubicaciones'
import EstadoCarga from '../comunes/EstadoCarga'
import Modal from '../comunes/Modal'
import toast from 'react-hot-toast'

export default function GestionAlmacenes() {
    const [almacenes, setAlmacenes] = useState([])
    const [ubicaciones, setUbicaciones] = useState([])
    const [almacenActivo, setAlmacenActivo] = useState(null)
    const [cargando, setCargando] = useState(true)
    const [cargandoUbics, setCargandoUbics] = useState(false)

    // Modal para crear nueva ubicación
    const [modalUbicacion, setModalUbicacion] = useState(false)
    const [formUbic, setFormUbic] = useState({ codigo: '', descripcion: '', tipo: '' })

    const cargarAlmacenes = async () => {
        try {
            setCargando(true)
            const res = await getAlmacenes()
            setAlmacenes(res)
            if (res.length > 0) {
                seleccionarAlmacen(res[0].codigo)
            }
        } catch (err) {
            toast.error('Error al cargar almacenes de LIN')
        } finally {
            setCargando(false)
        }
    }

    const seleccionarAlmacen = async (codigo) => {
        setAlmacenActivo(codigo)
        setCargandoUbics(true)
        try {
            const ubics = await getUbicacionesAlmacen(codigo)
            setUbicaciones(ubics)
        } catch (e) {
            toast.error('Error al cargar ubicaciones')
        } finally {
            setCargandoUbics(false)
        }
    }

    useEffect(() => { cargarAlmacenes() }, [])

    const guardarUbicacion = async (e) => {
        e.preventDefault()
        try {
            await createUbicacion({
                ...formUbic,
                almacen_cod: almacenActivo,
                codigo: formUbic.codigo.toUpperCase().trim()
            })
            toast.success('Ubicación registrada')
            setModalUbicacion(false)
            seleccionarAlmacen(almacenActivo)
        } catch (err) {
            toast.error(err.response?.data?.detail || 'Error al crear ubicación')
        }
    }

    const almActual = almacenes.find(a => a.codigo === almacenActivo)

    return (
        <div className="fade-in">
            <h1 className="page-title">Configuración Logística</h1>
            <p className="page-subtitle">Almacenes y ubicaciones de la base de datos LIN (ALMACENES + UBICACION)</p>

            {cargando ? <EstadoCarga /> : (
                <div style={{ display: 'flex', gap: '24px' }}>

                    {/* Lista de Almacenes */}
                    <div style={{ width: '260px', display: 'flex', flexDirection: 'column', gap: '12px', flexShrink: 0 }}>
                        <div style={{ fontWeight: '600', color: 'var(--text-300)', textTransform: 'uppercase', fontSize: '0.8rem', marginBottom: '4px' }}>
                            Red de Almacenes ({almacenes.length})
                        </div>
                        {almacenes.map(a => (
                            <button
                                key={a.codigo}
                                className={almacenActivo === a.codigo ? 'btn-accent' : 'card'}
                                style={{
                                    padding: '14px 16px',
                                    textAlign: 'left',
                                    border: almacenActivo === a.codigo ? '1px solid var(--accent)' : '1px solid var(--border)',
                                    cursor: 'pointer'
                                }}
                                onClick={() => seleccionarAlmacen(a.codigo)}
                            >
                                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '4px' }}>
                                    <span style={{ fontFamily: 'monospace', fontWeight: 'bold', fontSize: '1rem' }}>{a.codigo}</span>
                                    <span style={{ fontWeight: '600', fontSize: '0.95rem' }}>{a.nombre}</span>
                                </div>
                                <div style={{ fontSize: '0.8rem', opacity: 0.75 }}>
                                    {a.direccion || 'Sin dirección'} {a.poblacion ? `· ${a.poblacion}` : ''}
                                </div>
                                {a.num_ubicaciones !== undefined && (
                                    <div style={{ fontSize: '0.75rem', marginTop: '4px', opacity: 0.6 }}>
                                        {a.num_ubicaciones} ubicaciones
                                    </div>
                                )}
                            </button>
                        ))}
                    </div>

                    {/* Panel de Ubicaciones */}
                    <div className="card fade-in" style={{ flex: 1, padding: '24px' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                            <div>
                                <h2 style={{ margin: '0 0 4px 0' }}>
                                    {almActual ? `${almActual.codigo} — ${almActual.nombre}` : 'Almacén'}
                                </h2>
                                <p style={{ margin: 0, color: 'var(--text-400)', fontSize: '0.85rem' }}>
                                    Ubicaciones registradas en UBICACION (UBIALM = {almacenActivo})
                                </p>
                            </div>
                            <button
                                className="btn-accent"
                                onClick={() => { setFormUbic({ codigo: '', descripcion: '', tipo: '' }); setModalUbicacion(true) }}
                            >
                                + Nueva Ubicación
                            </button>
                        </div>

                        {cargandoUbics ? <EstadoCarga /> : (
                            ubicaciones.length === 0 ? (
                                <p style={{ color: 'var(--text-400)', textAlign: 'center', padding: '40px' }}>
                                    Este almacén no tiene ubicaciones registradas en LIN.
                                </p>
                            ) : (
                                <div style={{ overflowX: 'auto' }}>
                                    <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                                        <thead style={{ background: 'var(--surface-hover)' }}>
                                            <tr>
                                                <th style={{ padding: '10px 14px', fontSize: '0.8rem', color: 'var(--text-300)' }}>UBICON</th>
                                                <th style={{ padding: '10px 14px', fontSize: '0.8rem', color: 'var(--text-300)' }}>Código</th>
                                                <th style={{ padding: '10px 14px', fontSize: '0.8rem', color: 'var(--text-300)' }}>Tipo</th>
                                                <th style={{ padding: '10px 14px', fontSize: '0.8rem', color: 'var(--text-300)' }}>Descripción</th>
                                                <th style={{ padding: '10px 14px', fontSize: '0.8rem', color: 'var(--text-300)', textAlign: 'right' }}>Stock Total</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {ubicaciones.map(u => (
                                                <tr key={u.id} style={{ borderBottom: '1px solid var(--border)' }}>
                                                    <td style={{ padding: '10px 14px', fontFamily: 'monospace', color: 'var(--text-400)', fontSize: '0.85rem' }}>{u.ubicon}</td>
                                                    <td style={{ padding: '10px 14px', fontWeight: '500', color: 'var(--accent)', fontFamily: 'monospace' }}>{u.codigo || u.id}</td>
                                                    <td style={{ padding: '10px 14px', color: 'var(--text-300)' }}>{u.tipo || '—'}</td>
                                                    <td style={{ padding: '10px 14px', color: 'var(--text-400)', fontSize: '0.9rem' }}>{u.descripcion || '—'}</td>
                                                    <td style={{ padding: '10px 14px', textAlign: 'right', fontWeight: '500' }}>
                                                        {u.stock_total !== undefined ? u.stock_total : '—'}
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            )
                        )}
                    </div>
                </div>
            )}

            {/* Modal nueva Ubicación */}
            <Modal isOpen={modalUbicacion} onClose={() => setModalUbicacion(false)} titulo="Nueva Ubicación">
                <form onSubmit={guardarUbicacion} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    <div>
                        <label>Código de Ubicación * <span style={{ fontSize: '0.8rem', color: 'var(--text-400)' }}>(UBICODIGO)</span></label>
                        <input
                            required
                            value={formUbic.codigo}
                            onChange={e => setFormUbic({...formUbic, codigo: e.target.value})}
                            placeholder="Ej: A-01-01"
                            maxLength={20}
                        />
                    </div>
                    <div>
                        <label>Tipo <span style={{ fontSize: '0.8rem', color: 'var(--text-400)' }}>(UBITIP)</span></label>
                        <input
                            value={formUbic.tipo}
                            onChange={e => setFormUbic({...formUbic, tipo: e.target.value})}
                            placeholder="Ej: estantería, pallet, suelo..."
                            maxLength={10}
                        />
                    </div>
                    <div>
                        <label>Descripción</label>
                        <input
                            value={formUbic.descripcion}
                            onChange={e => setFormUbic({...formUbic, descripcion: e.target.value})}
                            placeholder="Observaciones opcionales"
                        />
                    </div>
                    <button type="submit" className="btn-accent" style={{ marginTop: '8px' }}>Registrar Ubicación</button>
                </form>
            </Modal>
        </div>
    )
}
