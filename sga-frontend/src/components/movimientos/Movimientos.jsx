import { useEffect, useState } from 'react'
import { getMovimientos } from '../../api/movimientos'
import EstadoCarga from '../comunes/EstadoCarga'
import toast from 'react-hot-toast'

const PAGE_SIZE = 50

export default function Movimientos() {
    const [movimientos, setMovimientos] = useState([])
    const [total, setTotal] = useState(0)
    const [cargando, setCargando] = useState(true)
    const [error, setError] = useState(null)
    const [pagina, setPagina] = useState(0)
    const [filtroArticulo, setFiltroArticulo] = useState('')
    const [filtroAlmacen, setFiltroAlmacen] = useState('')

    const cargar = async (pag = 0) => {
        setCargando(true)
        setError(null)
        try {
            const params = { skip: pag * PAGE_SIZE, limit: PAGE_SIZE }
            // Filtros adaptados a ALBARANCS (sin tipo, con articulo_cod y almacen_cod)
            if (filtroArticulo) params.articulo_cod = filtroArticulo
            if (filtroAlmacen) params.almacen_cod = filtroAlmacen
            const res = await getMovimientos(params)
            setMovimientos(res.data.movimientos)
            setTotal(res.data.total)
        } catch (err) {
            setError('No se pudo cargar el historial de movimientos.')
        } finally {
            setCargando(false)
        }
    }

    useEffect(() => { cargar(0) }, [filtroArticulo, filtroAlmacen])

    const totalPaginas = Math.ceil(total / PAGE_SIZE)

    const irPagina = (nuevaPag) => {
        setPagina(nuevaPag)
        cargar(nuevaPag)
    }

    const formatFecha = (iso) => {
        if (!iso) return '—'
        const d = new Date(iso)
        return d.toLocaleString('es-ES', {
            day: '2-digit', month: '2-digit', year: 'numeric',
            hour: '2-digit', minute: '2-digit'
        })
    }

    return (
        <div className="fade-in">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                <div>
                    <h1 className="page-title">Movimientos de Stock</h1>
                    <p className="page-subtitle">Historial de entradas y salidas desde la base de datos LIN (ALBARANCS)</p>
                </div>
            </div>

            {/* Filtros */}
            <div className="card" style={{ marginBottom: '24px', display: 'flex', gap: '16px', padding: '16px', background: 'var(--surface)' }}>
                <input
                    type="text"
                    placeholder="Filtrar por código de artículo (SKU)..."
                    value={filtroArticulo}
                    onChange={e => setFiltroArticulo(e.target.value)}
                    style={{ flex: 1 }}
                />
                <input
                    type="text"
                    placeholder="Filtrar por almacén (ej: A1)..."
                    value={filtroAlmacen}
                    onChange={e => setFiltroAlmacen(e.target.value)}
                    style={{ width: '200px' }}
                />
                <button className="btn-ghost" onClick={() => { setFiltroArticulo(''); setFiltroAlmacen('') }}>✕ Limpiar</button>
            </div>

            {cargando && <EstadoCarga />}
            {!cargando && error && <p className="estado-error">{error}</p>}

            {!cargando && !error && (
                <div className="card fade-in">
                    <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                        <thead>
                            <tr style={{ borderBottom: '1px solid var(--border)' }}>
                                <th style={{ padding: '12px' }}>Fecha</th>
                                <th style={{ padding: '12px' }}>Artículo</th>
                                <th style={{ padding: '12px' }}>Movimiento</th>
                                <th style={{ padding: '12px' }}>Cantidad</th>
                                <th style={{ padding: '12px' }}>Ubicación</th>
                                <th style={{ padding: '12px' }}>Albarán</th>
                                <th style={{ padding: '12px' }}>Cliente</th>
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
                                            <strong style={{ color: 'var(--accent)', fontFamily: 'monospace' }}>{m.articulo_cod}</strong>
                                        </td>
                                        <td style={{ padding: '12px' }}>
                                            <span style={{
                                                padding: '2px 8px',
                                                borderRadius: '4px',
                                                fontSize: '0.8rem',
                                                background: m.mov === 'E' ? 'rgba(34,197,94,0.15)' : 'rgba(239,68,68,0.15)',
                                                color: m.mov === 'E' ? 'var(--green)' : 'var(--red)'
                                            }}>
                                                {m.tipo_mov || m.mov || '—'}
                                            </span>
                                        </td>
                                        <td style={{ fontWeight: 'bold', padding: '12px', color: 'var(--text-100)' }}>
                                            {m.cantidad ?? '—'}
                                        </td>
                                        <td style={{ padding: '12px', color: 'var(--text-400)', fontSize: '0.9rem' }}>
                                            {m.ubicacion || '—'}
                                            {m.almacen_cod ? <div style={{ fontSize: '0.75rem' }}>Alm: {m.almacen_cod}</div> : null}
                                        </td>
                                        <td style={{ padding: '12px', color: 'var(--text-300)', fontSize: '0.85rem' }}>
                                            {m.num_alb || `${m.serie || ''}-${m.numero || ''}`}
                                        </td>
                                        <td style={{ padding: '12px', color: 'var(--text-300)', fontSize: '0.85rem' }}>
                                            {m.cliente_nom || m.cliente_cod || '—'}
                                        </td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan="7" style={{ textAlign: 'center', padding: '24px', color: 'var(--text-400)' }}>
                                        No hay movimientos registrados o los filtros no devuelven resultados.
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>

                    {totalPaginas > 1 && (
                        <div className="paginacion" style={{ padding: '16px', borderTop: '1px solid var(--border)', display: 'flex', gap: '12px', alignItems: 'center', justifyContent: 'center' }}>
                            <button className="btn-outline" disabled={pagina === 0} onClick={() => irPagina(pagina - 1)}>← Anterior</button>
                            <span>Página {pagina + 1} de {totalPaginas} ({total} movimientos)</span>
                            <button className="btn-outline" disabled={pagina >= totalPaginas - 1} onClick={() => irPagina(pagina + 1)}>Siguiente →</button>
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}
