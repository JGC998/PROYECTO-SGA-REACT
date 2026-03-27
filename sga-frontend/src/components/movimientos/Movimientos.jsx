import { useEffect, useState } from 'react'
import { getMovimientos } from '../../api/movimientos'

const PAGE_SIZE = 50

export default function Movimientos() {
    const [movimientos, setMovimientos] = useState([])
    const [total, setTotal] = useState(0)
    const [cargando, setCargando] = useState(true)
    const [error, setError] = useState(null)
    const [pagina, setPagina] = useState(0)
    const [filtroTipo, setFiltroTipo] = useState('')

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

    useEffect(() => { cargar(0) }, [])

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

    return (
        <>
            <h2>🔄 Historial de Movimientos</h2>

            <div className="filtros-movimientos">
                <button
                    className={filtroTipo === '' ? 'btn-filtro active' : 'btn-filtro'}
                    onClick={() => cambiarFiltro('')}
                >
                    Todos
                </button>
                <button
                    className={filtroTipo === 'entrada' ? 'btn-filtro active' : 'btn-filtro'}
                    onClick={() => cambiarFiltro('entrada')}
                >
                    ↑ Entradas
                </button>
                <button
                    className={filtroTipo === 'salida' ? 'btn-filtro active' : 'btn-filtro'}
                    onClick={() => cambiarFiltro('salida')}
                >
                    ↓ Salidas
                </button>
            </div>

            {cargando && <p className="estado-info">Cargando movimientos…</p>}
            {!cargando && error && <p className="estado-error">{error}</p>}

            {!cargando && !error && (
                <>
                    <table>
                        <thead>
                            <tr>
                                <th>Fecha</th>
                                <th>Producto</th>
                                <th>Tipo</th>
                                <th>Cantidad</th>
                                <th>Antes → Después</th>
                                <th>Motivo</th>
                            </tr>
                        </thead>
                        <tbody>
                            {movimientos.length > 0 ? (
                                movimientos.map(m => (
                                    <tr key={m.id}>
                                        <td style={{ fontSize: '0.85rem', color: '#aaa' }}>
                                            {formatFecha(m.fecha)}
                                        </td>
                                        <td>
                                            <strong>{m.producto_sku}</strong><br />
                                            <span style={{ fontSize: '0.85rem', color: '#ccc' }}>{m.producto_nombre}</span>
                                        </td>
                                        <td>
                                            <span className={`badge badge-${m.tipo}`}>
                                                {m.tipo === 'entrada' ? '↑ Entrada' : '↓ Salida'}
                                            </span>
                                        </td>
                                        <td style={{ fontWeight: 'bold' }}>
                                            {m.tipo === 'entrada' ? '+' : '-'}{m.cantidad}
                                        </td>
                                        <td style={{ color: '#aaa', fontSize: '0.9rem' }}>
                                            {m.cantidad_anterior} → {m.cantidad_nueva}
                                        </td>
                                        <td style={{ color: '#aaa', fontSize: '0.85rem' }}>
                                            {m.motivo || '—'}
                                        </td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan="6" style={{ textAlign: 'center', padding: '20px' }}>
                                        No hay movimientos registrados aún.
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>

                    {totalPaginas > 1 && (
                        <div className="paginacion">
                            <button disabled={pagina === 0} onClick={() => irPagina(pagina - 1)}>← Anterior</button>
                            <span>Página {pagina + 1} de {totalPaginas} ({total} movimientos)</span>
                            <button disabled={pagina >= totalPaginas - 1} onClick={() => irPagina(pagina + 1)}>Siguiente →</button>
                        </div>
                    )}
                </>
            )}
        </>
    )
}
