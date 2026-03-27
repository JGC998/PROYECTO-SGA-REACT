import { useState, useEffect } from 'react'
import { getResumen, getMovimientosPorDia, getOcupacionZonas } from '../../api/reportes'
import KpiCard from '../comunes/KpiCard'
import EstadoCarga from '../comunes/EstadoCarga'
import EstadoVacio from '../comunes/EstadoVacio'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts'
import { format, parseISO } from 'date-fns'
import { es } from 'date-fns/locale'

export default function Dashboard() {
    const [datos, setDatos] = useState(null)
    const [cargando, setCargando] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        const cargarDatos = async () => {
            try {
                setCargando(true)
                const [resumen, grafico, zonas] = await Promise.all([
                    getResumen(),
                    getMovimientosPorDia(7),
                    getOcupacionZonas()
                ])
                setDatos({ resumen, grafico, zonas })
                setError(null)
            } catch (err) {
                console.error(err)
                setError('No se pudo cargar el dashboard. Comprueba la conexión.')
            } finally {
                setCargando(false)
            }
        }
        cargarDatos()
    }, [])

    if (cargando) return <EstadoCarga texto="Cargando métricas en tiempo real..." />
    if (error) return <EstadoVacio titulo="Error de Conexión" descripcion={error} accion={{ texto: "Reintentar", onClick: () => window.location.reload() }} />
    if (!datos) return null

    const CustomTooltip = ({ active, payload, label }) => {
        if (active && payload && payload.length) {
            return (
                <div style={{ background: 'var(--surface)', padding: '12px', border: '1px solid var(--border)', borderRadius: '8px' }}>
                    <p style={{ margin: '0 0 8px 0', fontWeight: 'bold' }}>
                        {format(parseISO(label), "d MMM yyyy", { locale: es })}
                    </p>
                    {payload.map((entry, index) => (
                        <p key={index} style={{ color: entry.color, margin: 0, fontSize: '0.9rem' }}>
                            {entry.name === 'entradas' ? '📥 Entradas: ' : '📤 Salidas: '} 
                            {entry.value} uds
                        </p>
                    ))}
                </div>
            )
        }
        return null
    }

    return (
        <div className="fade-in">
            <h1 className="page-title">Dashboard</h1>
            <p className="page-subtitle">Panel de control de almacén en tiempo real</p>

            {/* Fila KPIs */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '20px', marginBottom: '24px' }}>
                <KpiCard 
                    titulo="Productos Activos" 
                    valor={datos.resumen.productos_activos} 
                    subtitulo="en el catálogo general" 
                    color="var(--accent)"
                />
                <KpiCard 
                    titulo="Unidades en Stock" 
                    valor={datos.resumen.unidades_stock?.toLocaleString('es-ES') || '0'} 
                    subtitulo="total de mercancía física" 
                    color="var(--cyan)"
                />
                <KpiCard 
                    titulo="Alertas Stock Mínimo" 
                    valor={datos.resumen.alertas_stock} 
                    subtitulo="productos requieren reposición" 
                    color={datos.resumen.alertas_stock > 0 ? "var(--red)" : "var(--green)"}
                />
                <KpiCard 
                    titulo="Operaciones de Hoy" 
                    valor={datos.resumen.movimientos_hoy} 
                    subtitulo="movimientos registrados hoy" 
                    color="var(--purple)"
                />
            </div>

            {/* Fila Gráficas */}
            <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 2fr) minmax(0, 1fr)', gap: '24px' }}>
                
                {/* Gráfica principal */}
                <div className="card" style={{ display: 'flex', flexDirection: 'column' }}>
                    <h2 style={{ fontSize: '1.1rem', marginBottom: '20px' }}>Actividad Últimos 7 Días</h2>
                    <div style={{ flex: 1, minHeight: '300px' }}>
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={datos.grafico} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
                                <XAxis 
                                    dataKey="fecha" 
                                    stroke="var(--text-400)" 
                                    tickFormatter={(str) => format(parseISO(str), "d MMM", { locale: es })}
                                    tick={{ fontSize: 12 }}
                                    axisLine={false}
                                    tickLine={false}
                                />
                                <YAxis 
                                    stroke="var(--text-400)" 
                                    tick={{ fontSize: 12 }}
                                    axisLine={false}
                                    tickLine={false}
                                />
                                <Tooltip content={<CustomTooltip />} cursor={{ fill: 'var(--surface-hover)' }} />
                                <Legend wrapperStyle={{ paddingTop: '20px' }} />
                                <Bar dataKey="entradas" name="Entradas" fill="var(--green)" radius={[4, 4, 0, 0]} maxBarSize={40} />
                                <Bar dataKey="salidas" name="Salidas" fill="var(--yellow)" radius={[4, 4, 0, 0]} maxBarSize={40} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Ocupación por Zonas */}
                <div className="card">
                    <h2 style={{ fontSize: '1.1rem', marginBottom: '20px' }}>Ocupación por Zonas</h2>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                        {datos.zonas.length > 0 ? datos.zonas.map((zona, idx) => {
                            const p = zona.porcentaje
                            const color = p > 90 ? 'var(--red)' : p > 70 ? 'var(--yellow)' : 'var(--green)'
                            
                            return (
                                <div key={idx}>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', fontSize: '0.9rem' }}>
                                        <span style={{ fontWeight: '500', color: 'var(--text-200)' }}>{zona.zona}</span>
                                        <span style={{ color: color, fontWeight: 'bold' }}>{p}%</span>
                                    </div>
                                    <div style={{ height: '8px', background: 'var(--surface)', borderRadius: '4px', overflow: 'hidden' }}>
                                        <div style={{ 
                                            width: `${p}%`, 
                                            height: '100%', 
                                            background: color,
                                            borderRadius: '4px',
                                            transition: 'width 1s ease-in-out'
                                        }} />
                                    </div>
                                </div>
                            )
                        }) : (
                            <p style={{ color: 'var(--text-400)', fontSize: '0.9rem', textAlign: 'center', marginTop: '40px' }}>
                                No hay zonas configuradas.
                            </p>
                        )}
                    </div>
                </div>

            </div>
        </div>
    )
}
