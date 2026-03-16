import axios from 'axios'
import toast from 'react-hot-toast'
import { useState, useEffect } from 'react'

export default function FilaProducto({ p, alActualizar }) {

    const [valorInput, setValorInput] = useState(p.cantidad)
    const esBajoMinimo = p.cantidad < p.stock_minimo

    useEffect(() => {
        setValorInput(p.cantidad)
    }, [p.cantidad])

    const gestionarStock = async (cambio) => {
        try {
            await axios.put(`http://127.0.0.1:8000/stock/${p.id}?cambio=${cambio}`)
            alActualizar()
        } catch (err) { toast.error('Error en el stock') }
    }

    const borrarProducto = async () => {
        if (!window.confirm("¿Seguro que quieres borrar este producto?")) return
        try {
            await axios.delete(`http://127.0.0.1:8000/productos/${p.id}`)
            toast.success('Producto eliminado')
            alActualizar()
        } catch (err) { toast.error('Error al borrar') }
    }

    const fijarStockManual = async () => {
        if (valorInput === p.cantidad) return
        try {
            await axios.put(`http://127.0.0.1:8000/stock/${p.id}/fijar?cantidad=${valorInput}`)
            toast.success('Stock actualizado')
            alActualizar()
        } catch (err) { toast.error('Error al fijar stock') }
    }

    return (
        <tr className={esBajoMinimo ? 'stock-bajo' : ''}>
            <td><strong>{p.sku}</strong></td>
            <td>{p.nombre}</td>
            <td>{p.stock_minimo} uds.</td>
            <td>
                <div className="controles-stock">
                    <button className="btn-stock" onClick={() => gestionarStock(-1)}>-</button>

                    <input
                        type="number"
                        className={`input-stock-tabla ${esBajoMinimo ? 'alerta-numero' : ''}`}
                        value={valorInput}
                        onChange={(e) => setValorInput(Number(e.target.value))}
                        onBlur={fijarStockManual}
                        onKeyDown={(e) => e.key === 'Enter' && fijarStockManual()}
                    />

                    <button className="btn-stock" onClick={() => gestionarStock(1)}>+</button>
                    {esBajoMinimo && <span title="Stock bajo mínimos">⚠️</span>}
                </div>
            </td>
            <td>
                <button className="btn-delete" onClick={borrarProducto}>Eliminar</button>
            </td>
        </tr>
    )
}