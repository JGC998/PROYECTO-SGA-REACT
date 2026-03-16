import { useState } from 'react'
import axios from 'axios'
import toast from 'react-hot-toast'

export default function FormularioProducto({ alCrear }) {
    const [formulario, setFormulario] = useState({ sku: '', nombre: '', stock_minimo: 0 })

    const enviarFormulario = async (e) => {
        e.preventDefault()
        try {
            await axios.post('http://127.0.0.1:8000/productos', formulario)
            toast.success('¡Producto creado!')
            setFormulario({ sku: '', nombre: '', stock_minimo: 0 })
            alCrear()
        } catch (err) {
            const mensaje = err.response?.data?.detail || 'Error al crear'
            toast.error(mensaje)
        }
    }

    return (
        <form className="product-form" onSubmit={enviarFormulario}>
            <input placeholder="SKU" value={formulario.sku} required
                onChange={e => setFormulario({ ...formulario, sku: e.target.value })} />
            <input placeholder="Nombre" value={formulario.nombre} required
                onChange={e => setFormulario({ ...formulario, nombre: e.target.value })} />
            <input type="number" value={formulario.stock_minimo}
                onChange={e => setFormulario({ ...formulario, stock_minimo: Number(e.target.value) })} />
            <button type="submit">Añadir</button>
        </form>
    )
}