import { useState } from 'react'
import MapaZonas from './MapaZonas'
import { getProductos } from '../../api/productos'
import { useEffect } from 'react'
import EstadoCarga from '../comunes/EstadoCarga'
import EstadoVacio from '../comunes/EstadoVacio'
import Badge from '../comunes/Badge'
import { getResumenStock } from '../../api/stock'
import { updateProducto } from '../../api/productos'
import toast from 'react-hot-toast'

export default function GestionStock() {
    const [vistaActiva, setVistaActiva] = useState('mapa') // 'mapa' o 'listado'
    const [productos, setProductos] = useState([])
    const [cargando, setCargando] = useState(false)
    const [filtro, setFiltro] = useState('')
    const [editando, setEditando] = useState(null)
    const [nuevaCant, setNuevaCant] = useState('')

    const cargarListado = async () => {
        try {
            setCargando(true)
            const res = await getProductos(0, 100) // Cargamos 100 max por ahora
            setProductos(res.data.productos)
        } catch (err) {
            console.error(err)
            toast.error("Error al cargar inventario")
        } finally {
            setCargando(false)
        }
    }

    useEffect(() => {
        if (vistaActiva === 'listado') {
            cargarListado()
        }
    }, [vistaActiva])

    const handleAjusteStock = async (sku) => {
        // En LIN no hay endpoint de fijar stock directamente.
        // Registramos el ajuste como un inventario puntual o lo dejamos como no-op por ahora.
        toast.info('Los ajustes de stock se realizan a través de la sección Inventarios')
        setEditando(null)
    }

    const Pestañas = () => (
        <div style={{ display: 'flex', gap: '8px', marginBottom: '24px', borderBottom: '1px solid var(--border)', paddingBottom: '16px' }}>
            <button 
                className={vistaActiva === 'mapa' ? 'btn-accent' : 'btn-ghost'} 
                onClick={() => setVistaActiva('mapa')}
            >
                🗺️ Mapa Visual de Zonas
            </button>
            <button 
                className={vistaActiva === 'listado' ? 'btn-accent' : 'btn-ghost'} 
                onClick={() => setVistaActiva('listado')}
            >
                📋 Listado Global
            </button>
        </div>
    )

    return (
        <div className="fade-in">
            <h1 className="page-title">Control de Inventario Físico</h1>
            <p className="page-subtitle">Visualiza la ocupación del almacén o ajusta el stock de productos</p>

            <Pestañas />

            {vistaActiva === 'mapa' && <MapaZonas />}

            {vistaActiva === 'listado' && (
                <div className="card fade-in">
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
                        <h2 style={{ fontSize: '1.2rem', margin: 0 }}>Listado de Existencias</h2>
                        <input 
                            type="text" 
                            placeholder="Buscar por SKU o Nombre..." 
                            value={filtro}
                            onChange={(e) => setFiltro(e.target.value)}
                            style={{ width: '300px' }}
                        />
                    </div>

                    {cargando ? <EstadoCarga /> : (
                        <div style={{ overflowX: 'auto' }}>
                            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                                <thead>
                                    <tr style={{ borderBottom: '1px solid var(--border)' }}>
                                        <th style={{ padding: '12px', color: 'var(--text-300)' }}>SKU</th>
                                        <th style={{ padding: '12px', color: 'var(--text-300)' }}>Nombre</th>
                                        <th style={{ padding: '12px', color: 'var(--text-300)' }}>Stock Mínimo</th>
                                        <th style={{ padding: '12px', color: 'var(--text-300)' }}>Físico</th>
                                        <th style={{ padding: '12px', color: 'var(--text-300)' }}>Estado</th>
                                        <th style={{ padding: '12px', color: 'var(--text-300)' }}>Acciones</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {productos.filter(p => p.sku.toLowerCase().includes(filtro.toLowerCase()) || p.nombre.toLowerCase().includes(filtro.toLowerCase())).map(p => (
                                        <tr key={p.sku} style={{ borderBottom: '1px solid var(--border)' }}>
                                            <td style={{ padding: '12px', fontWeight: '500', color: 'var(--accent)', fontFamily: 'monospace' }}>{p.sku}</td>
                                            <td style={{ padding: '12px' }}>{p.nombre}</td>
                                            <td style={{ padding: '12px', color: 'var(--text-400)' }}>{p.stock_min ?? 0}</td>
                                            <td style={{ padding: '12px', fontWeight: 'bold' }}>
                                                {editando === p.sku ? (
                                                    <div style={{ display: 'flex', gap: '8px', maxWidth: '150px' }}>
                                                        <input 
                                                            type="number" 
                                                            value={nuevaCant} 
                                                            onChange={e => setNuevaCant(e.target.value)}
                                                            autoFocus
                                                        />
                                                    </div>
                                                ) : (
                                                    <span style={{ color: p.cantidad <= 0 ? 'var(--red)' : p.cantidad <= (p.stock_min || 0) ? 'var(--yellow)' : 'var(--text-100)' }}>
                                                        {p.cantidad ?? 0}
                                                    </span>
                                                )}
                                            </td>
                                            <td style={{ padding: '12px' }}>
                                                {(p.cantidad ?? 0) <= 0 ? <Badge texto="AGOTADO" variante="danger" /> : 
                                                 (p.cantidad ?? 0) < (p.stock_min || 0) ? <Badge texto="BAJO MÍNIMO" variante="warning" /> : 
                                                 <Badge texto="OK" variante="success" />}
                                            </td>
                                            <td style={{ padding: '12px' }}>
                                                {editando === p.sku ? (
                                                    <div style={{ display: 'flex', gap: '8px' }}>
                                                        <button className="btn-accent" style={{ padding: '4px 8px', fontSize: '0.8rem' }} onClick={() => handleAjusteStock(p.sku)}>Guardar</button>
                                                        <button className="btn-ghost" style={{ padding: '4px 8px', fontSize: '0.8rem' }} onClick={() => setEditando(null)}>Cancelar</button>
                                                    </div>
                                                ) : (
                                                    <button className="btn-outline" style={{ padding: '4px 8px', fontSize: '0.8rem' }} onClick={() => { setEditando(p.sku); setNuevaCant(p.cantidad ?? 0) }}>Ver / Ajustar</button>
                                                )}
                                            </td>
                                        </tr>
                                    ))}
                                    {productos.length === 0 && (
                                        <tr><td colSpan="6" style={{ padding: '24px' }}><EstadoVacio titulo="No hay productos" descripcion="" /></td></tr>
                                    )}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}
