import { useEffect, useState } from 'react'
import { getProductos } from '../../api/productos'
import FormularioProducto from './FormularioProducto'
import FilaProducto from './FilaProducto'
import Buscador from './Buscador'

const PAGE_SIZE = 50

export default function GestionInventario() {
    const [productos, setProductos] = useState([])
    const [terminoBusqueda, setTerminoBusqueda] = useState('')
    const [cargando, setCargando] = useState(true)
    const [error, setError] = useState(null)
    const [total, setTotal] = useState(0)
    const [pagina, setPagina] = useState(0)

    const cargarProductos = async (pag = pagina) => {
        setCargando(true)
        setError(null)
        try {
            const respuesta = await getProductos(pag * PAGE_SIZE, PAGE_SIZE)
            setProductos(respuesta.data.productos)
            setTotal(respuesta.data.total)
        } catch (err) {
            setError('No se pudo conectar con el servidor. ¿Está el backend arrancado?')
        } finally {
            setCargando(false)
        }
    }

    useEffect(() => { cargarProductos(0) }, [])

    const productosFiltrados = productos.filter(p =>
        p.nombre.toLowerCase().includes(terminoBusqueda.toLowerCase()) ||
        p.sku.toLowerCase().includes(terminoBusqueda.toLowerCase())
    )

    const totalPaginas = Math.ceil(total / PAGE_SIZE)

    const irPagina = (nuevaPag) => {
        setPagina(nuevaPag)
        cargarProductos(nuevaPag)
    }

    return (
        <>
            <h2>📦 Gestión de Inventario</h2>

            <div className="controles-inventario">
                <FormularioProducto alCrear={() => cargarProductos(0)} />
                <Buscador filtro={terminoBusqueda} alCambiarFiltro={setTerminoBusqueda} />
            </div>

            {cargando && (
                <p className="estado-info">Cargando productos…</p>
            )}

            {!cargando && error && (
                <p className="estado-error">{error}</p>
            )}

            {!cargando && !error && (
                <>
                    <table>
                        <thead>
                            <tr>
                                <th>SKU</th><th>Nombre</th><th>Mínimo</th><th>Existencias</th><th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            {productosFiltrados.length > 0 ? (
                                productosFiltrados.map(p => (
                                    <FilaProducto key={p.id} p={p} alActualizar={() => cargarProductos(pagina)} />
                                ))
                            ) : (
                                <tr>
                                    <td colSpan="5" style={{ textAlign: 'center', padding: '20px' }}>
                                        {terminoBusqueda ? 'No hay productos que coincidan con la búsqueda.' : 'No hay productos en el almacén.'}
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>

                    {totalPaginas > 1 && (
                        <div className="paginacion">
                            <button
                                disabled={pagina === 0}
                                onClick={() => irPagina(pagina - 1)}
                            >
                                ← Anterior
                            </button>
                            <span>Página {pagina + 1} de {totalPaginas} ({total} productos)</span>
                            <button
                                disabled={pagina >= totalPaginas - 1}
                                onClick={() => irPagina(pagina + 1)}
                            >
                                Siguiente →
                            </button>
                        </div>
                    )}
                </>
            )}
        </>
    )
}