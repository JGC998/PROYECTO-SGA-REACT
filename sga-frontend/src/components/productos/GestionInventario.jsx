import { useEffect, useState } from 'react'
import axios from 'axios'
import FormularioProducto from './FormularioProducto'
import FilaProducto from './FilaProducto'
import Buscador from './Buscador' // Importamos el buscador

export default function GestionInventario() {
    const [productos, setProductos] = useState([])
    const [terminoBusqueda, setTerminoBusqueda] = useState('')

    const cargarProductos = async () => {
        try {
            const respuesta = await axios.get('http://127.0.0.1:8000/productos')
            setProductos(respuesta.data)
        } catch (err) { console.error("Error al cargar", err) }
    }

    useEffect(() => { cargarProductos() }, [])

    // Lógica de filtrado: buscamos en nombre y SKU (pasándolo todo a minúsculas)
    const productosFiltrados = productos.filter(p =>
        p.nombre.toLowerCase().includes(terminoBusqueda.toLowerCase()) ||
        p.sku.toLowerCase().includes(terminoBusqueda.toLowerCase())
    )

    return (
        <>
            <h2>📦 Gestión de Inventario</h2>

            <div className="controles-inventario">
                <FormularioProducto alCrear={cargarProductos} />
                <Buscador filtro={terminoBusqueda} alCambiarFiltro={setTerminoBusqueda} />
            </div>

            <table>
                <thead>
                    <tr>
                        <th>SKU</th><th>Nombre</th><th>Mínimo</th><th>Existencias</th><th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {productosFiltrados.length > 0 ? (
                        productosFiltrados.map(p => (
                            <FilaProducto key={p.id} p={p} alActualizar={cargarProductos} />
                        ))
                    ) : (
                        <tr>
                            <td colSpan="5" style={{ textAlign: 'center', padding: '20px' }}>
                                No se han encontrado productos que coincidan.
                            </td>
                        </tr>
                    )}
                </tbody>
            </table>
        </>
    )
}