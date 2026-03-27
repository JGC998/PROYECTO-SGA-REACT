import toast from 'react-hot-toast'
import { useState, useEffect } from 'react'
import { updateStock, fijarStock, deleteProducto, updateProducto } from '../../api/productos'

export default function FilaProducto({ p, alActualizar }) {
    const [valorInput, setValorInput] = useState(p.cantidad)
    const [editando, setEditando] = useState(false)
    const [formEdit, setFormEdit] = useState({ sku: p.sku, nombre: p.nombre, stock_minimo: p.stock_minimo })
    const esBajoMinimo = p.cantidad < p.stock_minimo

    useEffect(() => {
        setValorInput(p.cantidad)
    }, [p.cantidad])

    const gestionarStock = async (cambio) => {
        try {
            await updateStock(p.id, cambio)
            alActualizar()
        } catch (err) { toast.error('Error al actualizar stock') }
    }

    const borrarProducto = () => {
        toast((t) => (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <p style={{ margin: 0 }}>¿Borrar <strong>{p.nombre}</strong>?</p>
                <div style={{ display: 'flex', gap: '8px' }}>
                    <button
                        style={{ background: '#e74c3c', color: 'white', border: 'none', padding: '6px 12px', borderRadius: '4px', cursor: 'pointer' }}
                        onClick={async () => {
                            toast.dismiss(t.id)
                            try {
                                await deleteProducto(p.id)
                                toast.success('Producto eliminado')
                                alActualizar()
                            } catch (err) {
                                toast.error('Error al borrar el producto')
                            }
                        }}
                    >
                        Confirmar
                    </button>
                    <button
                        style={{ background: '#555', color: 'white', border: 'none', padding: '6px 12px', borderRadius: '4px', cursor: 'pointer' }}
                        onClick={() => toast.dismiss(t.id)}
                    >
                        Cancelar
                    </button>
                </div>
            </div>
        ), { duration: Infinity })
    }

    const fijarStockManual = async () => {
        if (valorInput === p.cantidad) return
        try {
            await fijarStock(p.id, valorInput)
            toast.success('Stock actualizado')
            alActualizar()
        } catch (err) { toast.error('Error al fijar stock') }
    }

    const guardarEdicion = async () => {
        if (!formEdit.sku.trim()) { toast.error('El SKU no puede estar vacío'); return }
        if (!formEdit.nombre.trim()) { toast.error('El nombre no puede estar vacío'); return }
        if (formEdit.stock_minimo < 0) { toast.error('El stock mínimo no puede ser negativo'); return }
        try {
            await updateProducto(p.id, formEdit)
            toast.success('Producto actualizado')
            setEditando(false)
            alActualizar()
        } catch (err) {
            toast.error(err.response?.data?.detail || 'Error al actualizar')
        }
    }

    if (editando) {
        return (
            <tr>
                <td>
                    <input
                        className="input-stock-tabla"
                        style={{ width: '80px' }}
                        value={formEdit.sku}
                        onChange={e => setFormEdit({ ...formEdit, sku: e.target.value })}
                    />
                </td>
                <td>
                    <input
                        className="input-stock-tabla"
                        style={{ width: '140px' }}
                        value={formEdit.nombre}
                        onChange={e => setFormEdit({ ...formEdit, nombre: e.target.value })}
                    />
                </td>
                <td>
                    <input
                        type="number"
                        className="input-stock-tabla"
                        style={{ width: '60px' }}
                        value={formEdit.stock_minimo}
                        onChange={e => setFormEdit({ ...formEdit, stock_minimo: Number(e.target.value) })}
                    />
                </td>
                <td>{p.cantidad} uds.</td>
                <td style={{ display: 'flex', gap: '6px' }}>
                    <button onClick={guardarEdicion} style={{ background: '#27ae60' }}>✔ Guardar</button>
                    <button onClick={() => setEditando(false)} style={{ background: '#555' }}>✖ Cancelar</button>
                </td>
            </tr>
        )
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
            <td style={{ display: 'flex', gap: '6px' }}>
                <button className="btn-edit" onClick={() => setEditando(true)}>✏️</button>
                <button className="btn-delete" onClick={borrarProducto}>Eliminar</button>
            </td>
        </tr>
    )
}