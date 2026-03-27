import { useState } from 'react'
import toast from 'react-hot-toast'
import { createProducto } from '../../api/productos'

export default function FormularioProducto({ alCrear }) {
    const [formulario, setFormulario] = useState({ sku: '', nombre: '', stock_minimo: 0 })

    const enviarFormulario = async (e) => {
        e.preventDefault()

        // Validaciones frontend
        if (!formulario.sku.trim()) {
            toast.error('El SKU no puede estar vacío')
            return
        }
        if (!formulario.nombre.trim()) {
            toast.error('El nombre no puede estar vacío')
            return
        }
        if (formulario.stock_minimo < 0) {
            toast.error('El stock mínimo no puede ser negativo')
            return
        }

        try {
            await createProducto({
                sku: formulario.sku.trim(),
                nombre: formulario.nombre.trim(),
                stock_minimo: formulario.stock_minimo,
            })
            toast.success('¡Producto creado!')
            setFormulario({ sku: '', nombre: '', stock_minimo: 0 })
            alCrear()
        } catch (err) {
            const mensaje = err.response?.data?.detail || 'Error al crear el producto'
            toast.error(mensaje)
        }
    }

    return (
        <form className="product-form" onSubmit={enviarFormulario}>
            <input
                placeholder="SKU"
                value={formulario.sku}
                required
                onChange={e => setFormulario({ ...formulario, sku: e.target.value })}
            />
            <input
                placeholder="Nombre del producto"
                value={formulario.nombre}
                required
                onChange={e => setFormulario({ ...formulario, nombre: e.target.value })}
            />
            <input
                type="number"
                placeholder="Stock mínimo"
                min="0"
                value={formulario.stock_minimo}
                onChange={e => setFormulario({ ...formulario, stock_minimo: Number(e.target.value) })}
            />
            <button type="submit">Añadir</button>
        </form>
    )
}