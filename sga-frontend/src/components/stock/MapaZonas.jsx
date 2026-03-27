import { useState, useEffect } from 'react'
import { getMapaZona } from '../../api/stock'
import api from '../../api/axios' // Temporal para llamadas directas
import EstadoCarga from '../comunes/EstadoCarga'
import EstadoVacio from '../comunes/EstadoVacio'
import Badge from '../comunes/Badge'

export default function MapaZonas() {
    const [zonas, setZonas] = useState([])
    const [zonaActiva, setZonaActiva] = useState(null)
    const [mapa, setMapa] = useState(null)
    const [cargando, setCargando] = useState(true)

    useEffect(() => {
        const cargarZonas = async () => {
            try {
                // Obtener zonas
                const res = await api.get('/almacenes/1/zonas') // Asumimos almacén principal
                setZonas(res.data)
                if (res.data.length > 0) {
                    setZonaActiva(res.data[0].id)
                }
            } catch (err) {
                console.error("Error cargando zonas:", err)
            } finally {
                setCargando(false)
            }
        }
        cargarZonas()
    }, [])

    useEffect(() => {
        const cargarMapa = async () => {
            if (!zonaActiva) return
            try {
                setCargando(true)
                const data = await getMapaZona(zonaActiva)
                setMapa(data)
            } catch (err) {
                console.error("Error cargando mapa:", err)
            } finally {
                setCargando(false)
            }
        }
        cargarMapa()
    }, [zonaActiva])

    if (cargando && zonas.length === 0) return <EstadoCarga />
    
    if (zonas.length === 0) return (
        <EstadoVacio 
            titulo="No hay zonas configuradas" 
            descripcion="El almacén principal no tiene zonas creadas aún." 
        />
    )

    return (
        <div style={{ display: 'flex', gap: '24px' }}>
            {/* Lista de zonas (pestañas verticales) */}
            <div style={{ width: '200px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <h3 style={{ fontSize: '0.85rem', color: 'var(--text-400)', textTransform: 'uppercase', marginBottom: '8px' }}>
                    Zonas del Almacén
                </h3>
                {zonas.map(z => (
                    <button 
                        key={z.id}
                        onClick={() => setZonaActiva(z.id)}
                        style={{
                            padding: '12px 16px',
                            background: zonaActiva === z.id ? 'var(--accent)' : 'var(--surface)',
                            color: zonaActiva === z.id ? 'white' : 'var(--text-200)',
                            border: `1px solid ${zonaActiva === z.id ? 'var(--accent)' : 'var(--border)'}`,
                            borderRadius: '8px',
                            textAlign: 'left',
                            fontWeight: '500',
                            transition: 'all 0.2s',
                            cursor: 'pointer'
                        }}
                    >
                        {z.nombre}
                    </button>
                ))}
            </div>

            {/* Vista del Mapa */}
            <div className="card fade-in" style={{ flex: 1 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                    <h2 style={{ fontSize: '1.2rem', margin: 0 }}>Mapa de Ubicaciones</h2>
                    <div style={{ display: 'flex', gap: '12px', fontSize: '0.8rem', color: 'var(--text-300)' }}>
                        <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                            <div style={{width: 12, height: 12, borderRadius: '50%', background: 'var(--green-bg)', border: '1px solid var(--green)'}}/> Vacío
                        </span>
                        <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                            <div style={{width: 12, height: 12, borderRadius: '50%', background: 'var(--yellow-bg)', border: '1px solid var(--yellow)'}}/> Medio
                        </span>
                        <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                            <div style={{width: 12, height: 12, borderRadius: '50%', background: 'var(--red-bg)', border: '1px solid var(--red)'}}/> Lleno
                        </span>
                    </div>
                </div>

                {cargando ? (
                    <EstadoCarga texto="Cargando ubicaciones..." />
                ) : mapa?.ubicaciones.length > 0 ? (
                    <div style={{ 
                        display: 'grid', 
                        gridTemplateColumns: 'repeat(auto-fill, minmax(120px, 1fr))', 
                        gap: '16px' 
                    }}>
                        {mapa.ubicaciones.map(u => {
                            let bg, borderColor, textColor
                            if (!u.activo) {
                                bg = 'var(--surface-hover)'
                                borderColor = 'var(--border)'
                                textColor = 'var(--text-400)'
                            } else if (u.estado === 'lleno') {
                                bg = 'var(--red-bg)'
                                borderColor = 'var(--red)'
                                textColor = 'var(--red)'
                            } else if (u.estado === 'medio') {
                                bg = 'var(--yellow-bg)'
                                borderColor = 'var(--yellow)'
                                textColor = 'var(--yellow)'
                            } else {
                                bg = 'var(--green-bg)'
                                borderColor = 'var(--green)'
                                textColor = 'var(--green)'
                            }

                            return (
                                <div key={u.id} style={{
                                    background: bg,
                                    border: `1px solid ${borderColor}`,
                                    borderRadius: '8px',
                                    padding: '16px',
                                    display: 'flex',
                                    flexDirection: 'column',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    gap: '8px',
                                    position: 'relative',
                                    opacity: u.activo ? 1 : 0.5
                                }}>
                                    <span style={{ fontWeight: 'bold', fontSize: '1.1rem', color: 'var(--text-100)' }}>{u.codigo}</span>
                                    <span style={{ fontSize: '0.8rem', color: textColor, fontWeight: '600' }}>
                                        {u.ocupacion_porcentaje}%
                                    </span>
                                    {!u.activo && (
                                        <div style={{ position: 'absolute', top: 4, right: 4 }}>
                                            <Badge texto="Inactiva" />
                                        </div>
                                    )}
                                </div>
                            )
                        })}
                    </div>
                ) : (
                    <EstadoVacio 
                        titulo="No hay ubicaciones" 
                        descripcion={`No se han creado ubicaciones para la zona ${mapa?.zona_nombre || ''}`} 
                    />
                )}
            </div>
        </div>
    )
}
