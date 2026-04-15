/**
 * MapaZonas → MapaAlmacen
 * Adaptado a LIN: muestra ubicaciones con su stock real, agrupadas por almacén.
 * No existe el concepto de "Zona" en LIN — las ubicaciones pertenecen directamente a ALMACENES.
 */
import { useState, useEffect } from 'react'
import { getAlmacenes, getUbicacionesAlmacen } from '../../api/almacenes'
import EstadoCarga from '../comunes/EstadoCarga'
import EstadoVacio from '../comunes/EstadoVacio'

export default function MapaZonas() {
    const [almacenes, setAlmacenes] = useState([])
    const [almacenActivo, setAlmacenActivo] = useState(null)
    const [ubicaciones, setUbicaciones] = useState([])
    const [cargando, setCargando] = useState(true)
    const [cargandoMap, setCargandoMap] = useState(false)

    useEffect(() => {
        const cargar = async () => {
            try {
                const alms = await getAlmacenes()
                setAlmacenes(alms)
                if (alms.length > 0) {
                    await cargarMapa(alms[0].codigo)
                }
            } catch (err) {
                console.error('Error cargando almacenes:', err)
            } finally {
                setCargando(false)
            }
        }
        cargar()
    }, [])

    const cargarMapa = async (cod) => {
        setAlmacenActivo(cod)
        setCargandoMap(true)
        try {
            const ubics = await getUbicacionesAlmacen(cod)
            setUbicaciones(ubics)
        } catch (err) {
            console.error('Error cargando ubicaciones:', err)
        } finally {
            setCargandoMap(false)
        }
    }

    if (cargando) return <EstadoCarga />

    if (almacenes.length === 0) return (
        <EstadoVacio
            titulo="No hay almacenes"
            descripcion="No se encontraron almacenes en la base de datos LIN."
        />
    )

    return (
        <div style={{ display: 'flex', gap: '24px' }}>
            {/* Lista de almacenes */}
            <div style={{ width: '200px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <h3 style={{ fontSize: '0.85rem', color: 'var(--text-400)', textTransform: 'uppercase', marginBottom: '8px' }}>
                    Almacenes LIN
                </h3>
                {almacenes.map(a => (
                    <button
                        key={a.codigo}
                        onClick={() => cargarMapa(a.codigo)}
                        style={{
                            padding: '12px 16px',
                            background: almacenActivo === a.codigo ? 'var(--accent)' : 'var(--surface)',
                            color: almacenActivo === a.codigo ? 'white' : 'var(--text-200)',
                            border: `1px solid ${almacenActivo === a.codigo ? 'var(--accent)' : 'var(--border)'}`,
                            borderRadius: '8px',
                            textAlign: 'left',
                            fontWeight: '500',
                            transition: 'all 0.2s',
                            cursor: 'pointer'
                        }}
                    >
                        <span style={{ fontFamily: 'monospace', fontWeight: 'bold' }}>{a.codigo}</span>{' '}
                        {a.nombre}
                    </button>
                ))}
            </div>

            {/* Mapa de ubicaciones */}
            <div className="card fade-in" style={{ flex: 1 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                    <h2 style={{ fontSize: '1.2rem', margin: 0 }}>
                        Ubicaciones — Almacén {almacenActivo}
                    </h2>
                    <div style={{ display: 'flex', gap: '12px', fontSize: '0.8rem', color: 'var(--text-300)' }}>
                        <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                            <div style={{width: 12, height: 12, borderRadius: '50%', background: 'var(--green-bg)', border: '1px solid var(--green)'}}/> Sin stock
                        </span>
                        <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                            <div style={{width: 12, height: 12, borderRadius: '50%', background: 'var(--yellow-bg)', border: '1px solid var(--yellow)'}}/> Con stock
                        </span>
                    </div>
                </div>

                {cargandoMap ? (
                    <EstadoCarga />
                ) : ubicaciones.length > 0 ? (
                    <div style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fill, minmax(110px, 1fr))',
                        gap: '12px'
                    }}>
                        {ubicaciones.map(u => {
                            const tieneStock = (u.stock_total || 0) > 0
                            return (
                                <div
                                    key={u.id}
                                    title={`UBICON: ${u.ubicon}\nStock: ${u.stock_total ?? 0}`}
                                    style={{
                                        background: tieneStock ? 'var(--yellow-bg)' : 'var(--green-bg)',
                                        border: `1px solid ${tieneStock ? 'var(--yellow)' : 'var(--green)'}`,
                                        borderRadius: '8px',
                                        padding: '12px',
                                        display: 'flex',
                                        flexDirection: 'column',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        gap: '6px',
                                        cursor: 'default'
                                    }}
                                >
                                    <span style={{ fontWeight: 'bold', fontSize: '0.9rem', color: 'var(--text-100)', textAlign: 'center', fontFamily: 'monospace' }}>
                                        {u.codigo || u.ubicon}
                                    </span>
                                    <span style={{
                                        fontSize: '0.75rem',
                                        color: tieneStock ? 'var(--yellow)' : 'var(--green)',
                                        fontWeight: '600'
                                    }}>
                                        {tieneStock ? `${u.stock_total} uds` : 'Vacío'}
                                    </span>
                                </div>
                            )
                        })}
                    </div>
                ) : (
                    <EstadoVacio
                        titulo="Sin ubicaciones"
                        descripcion={`El almacén ${almacenActivo} no tiene ubicaciones registradas en LIN`}
                    />
                )}
            </div>
        </div>
    )
}
