import { useState, useEffect } from 'react'
import { getProductos, createProducto, updateProducto, deleteProducto } from '../../api/productos'
import { getCategorias, getProveedores } from '../../api/catalog'
import EstadoCarga from '../comunes/EstadoCarga'
import EstadoVacio from '../comunes/EstadoVacio'
import Modal from '../comunes/Modal'
import Badge from '../comunes/Badge'
import toast from 'react-hot-toast'

export default function GestionProductos() {
    const [productos, setProductos] = useState([])
    const [categorias, setCategorias] = useState([])
    const [proveedores, setProveedores] = useState([])
    
    const [cargando, setCargando] = useState(true)
    const [modalAbierto, setModalAbierto] = useState(false)
    const [editando, setEditando] = useState(null)
    
    // Filtros
    const [filtroTexto, setFiltroTexto] = useState('')
    const [filtroCat, setFiltroCat] = useState('')
    
    // Formulario
    const defaultForm = {
        sku: '', nombre: '', descripcion: '', categoria_id: '', proveedor_id: '',
        unidad_medida: 'ud', stock_minimo: 0, stock_maximo: 0, precio_coste: 0, 
        codigo_barras: '', activo: true
    }
    const [form, setForm] = useState(defaultForm)

    const cargarDatos = async () => {
        try {
            setCargando(true)
            const [prodRes, catRes, provRes] = await Promise.all([
                getProductos(0, 500, filtroCat ? { categoria_id: filtroCat } : {}),
                getCategorias(),
                getProveedores()
            ])
            setProductos(prodRes.data.productos)
            setCategorias(catRes.data)
            setProveedores(provRes.data)
        } catch (err) {
            toast.error("Error al cargar datos del catálogo")
        } finally {
            setCargando(false)
        }
    }

    useEffect(() => { cargarDatos() }, [filtroCat])

    const abrirNuevo = () => {
        setEditando(null)
        setForm(defaultForm)
        setModalAbierto(true)
    }

    const abrirEditar = (p) => {
        setEditando(p.id)
        setForm({
            ...p,
            categoria_id: p.categoria_id || '',
            proveedor_id: p.proveedor_id || '',
            descripcion: p.descripcion || '',
            codigo_barras: p.codigo_barras || '',
            precio_coste: p.precio_coste || 0
        })
        setModalAbierto(true)
    }

    const handleGuardar = async (e) => {
        e.preventDefault()
        try {
            const data = {
                ...form,
                categoria_id: form.categoria_id ? parseInt(form.categoria_id) : null,
                proveedor_id: form.proveedor_id ? parseInt(form.proveedor_id) : null,
                stock_minimo: parseInt(form.stock_minimo),
                stock_maximo: parseInt(form.stock_maximo) || null,
                precio_coste: parseFloat(form.precio_coste) || null
            }

            if (editando) {
                await updateProducto(editando, data)
                toast.success("Producto actualizado")
            } else {
                await createProducto(data)
                toast.success("Producto creado exitosamente")
            }
            setModalAbierto(false)
            cargarDatos()
        } catch (err) {
            toast.error(err.response?.data?.detail || "Error al guardar el producto")
        }
    }

    const handleBorrar = async (id) => {
        if (!window.confirm("¿Seguro que deseas eliminar este producto? Se borrará todo su registro de stock (pero los logs de auditoría se conservan).")) return
        try {
            await deleteProducto(id)
            toast.success("Producto eliminado")
            cargarDatos()
        } catch (err) {
            toast.error(err.response?.data?.detail || "Error al eliminar")
        }
    }

    const prodFiltrados = productos.filter(p => 
        p.sku.toLowerCase().includes(filtroTexto.toLowerCase()) || 
        p.nombre.toLowerCase().includes(filtroTexto.toLowerCase())
    )

    return (
        <div className="fade-in">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                <div>
                    <h1 className="page-title">Catálogo de Productos</h1>
                    <p className="page-subtitle">Gestión unificada de SKUs, proveedores y mínimos de stock</p>
                </div>
                <button className="btn-accent" onClick={abrirNuevo}>
                    + Nuevo Producto
                </button>
            </div>

            <div className="card" style={{ marginBottom: '24px', display: 'flex', gap: '16px', background: 'var(--surface)' }}>
                <input 
                    type="text" 
                    placeholder="Buscar por código SKU o nombre..." 
                    value={filtroTexto} 
                    onChange={e => setFiltroTexto(e.target.value)}
                    style={{ flex: 1 }}
                />
                <select 
                    value={filtroCat} 
                    onChange={e => setFiltroCat(e.target.value)}
                    style={{ width: '250px' }}
                >
                    <option value="">Todas las categorías</option>
                    {categorias.map(c => <option key={c.id} value={c.id}>{c.nombre}</option>)}
                </select>
            </div>

            {cargando ? <EstadoCarga /> : (
                <div className="card fade-in" style={{ padding: 0, overflow: 'hidden' }}>
                    <div style={{ overflowX: 'auto' }}>
                        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                            <thead style={{ background: 'var(--surface-hover)' }}>
                                <tr>
                                    <th style={{ padding: '16px' }}>SKU</th>
                                    <th style={{ padding: '16px' }}>Nombre</th>
                                    <th style={{ padding: '16px' }}>Categoría</th>
                                    <th style={{ padding: '16px' }}>Stock Base</th>
                                    <th style={{ padding: '16px' }}>Estado</th>
                                    <th style={{ padding: '16px', textAlign: 'right' }}>Acciones</th>
                                </tr>
                            </thead>
                            <tbody>
                                {prodFiltrados.map(p => {
                                    const cat = categorias.find(c => c.id === p.categoria_id)
                                    return (
                                        <tr key={p.id} style={{ borderBottom: '1px solid var(--border)' }}>
                                            <td style={{ padding: '16px', fontWeight: '500', color: 'var(--accent)' }}>{p.sku}</td>
                                            <td style={{ padding: '16px' }}>
                                                {p.nombre}
                                                <div style={{ fontSize: '0.8rem', color: 'var(--text-400)' }}>
                                                    EAN: {p.codigo_barras || 'N/A'}
                                                </div>
                                            </td>
                                            <td style={{ padding: '16px' }}>{cat ? cat.nombre : 'Sin categorizar'}</td>
                                            <td style={{ padding: '16px', color: 'var(--text-300)' }}>
                                                Mín: {p.stock_minimo} {p.unidad_medida} <br/>
                                                <span style={{ fontSize: '0.8rem' }}>Máx: {p.stock_maximo || 'N/A'}</span>
                                            </td>
                                            <td style={{ padding: '16px' }}>
                                                {p.activo ? <Badge texto="Activo" variante="success" /> : <Badge texto="Inactivo" variante="default" />}
                                            </td>
                                            <td style={{ padding: '16px', textAlign: 'right' }}>
                                                <button className="btn-ghost" onClick={() => abrirEditar(p)}>✏️</button>
                                                <button className="btn-ghost" onClick={() => handleBorrar(p.id)} style={{ color: 'var(--red)' }}>🗑️</button>
                                            </td>
                                        </tr>
                                    )
                                })}
                                {prodFiltrados.length === 0 && (
                                    <tr><td colSpan="6" style={{ padding: '32px' }}>
                                        <EstadoVacio titulo="Sin resultados" descripcion="No se encontraron productos con estos filtros." />
                                    </td></tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}

            <Modal 
                isOpen={modalAbierto} 
                onClose={() => setModalAbierto(false)} 
                titulo={editando ? 'Editar Producto' : 'Nuevo Producto'}
            >
                <form onSubmit={handleGuardar} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                    
                    <div style={{ gridColumn: 'span 2' }}>
                        <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '6px', color: 'var(--text-300)' }}>Nombre del Producto *</label>
                        <input required type="text" value={form.nombre} onChange={e => setForm({...form, nombre: e.target.value})} />
                    </div>

                    <div>
                        <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '6px', color: 'var(--text-300)' }}>Unidad M.</label>
                        <select value={form.unidad_medida} onChange={e => setForm({...form, unidad_medida: e.target.value})}>
                            <option value="ud">Unidades (ud)</option>
                            <option value="kg">Kilogramos (kg)</option>
                            <option value="l">Litros (l)</option>
                            <option value="caja">Cajas</option>
                            <option value="pallet">Pallets</option>
                        </select>
                    </div>

                    <div>
                        <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '6px', color: 'var(--text-300)' }}>SKU (Código Interno) *</label>
                        <input required type="text" value={form.sku} onChange={e => setForm({...form, sku: e.target.value.toUpperCase()})} />
                    </div>

                    <div>
                        <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '6px', color: 'var(--text-300)' }}>Categoría</label>
                        <select value={form.categoria_id} onChange={e => setForm({...form, categoria_id: e.target.value})}>
                            <option value="">-- Sin categoría --</option>
                            {categorias.map(c => <option key={c.id} value={c.id}>{c.nombre}</option>)}
                        </select>
                    </div>

                    <div>
                        <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '6px', color: 'var(--text-300)' }}>Proveedor Habitual</label>
                        <select value={form.proveedor_id} onChange={e => setForm({...form, proveedor_id: e.target.value})}>
                            <option value="">-- Sin proveedor --</option>
                            {proveedores.map(p => <option key={p.id} value={p.id}>{p.nombre}</option>)}
                        </select>
                    </div>

                    <div style={{ padding: '16px', background: 'var(--bg-900)', borderRadius: '8px', gridColumn: 'span 2', display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '12px' }}>
                        <div>
                            <label style={{ display: 'block', fontSize: '0.75rem', marginBottom: '6px', color: 'var(--text-300)' }}>Stock Mínimo</label>
                            <input type="number" min="0" required value={form.stock_minimo} onChange={e => setForm({...form, stock_minimo: e.target.value})} />
                        </div>
                        <div>
                            <label style={{ display: 'block', fontSize: '0.75rem', marginBottom: '6px', color: 'var(--text-300)' }}>Stock Máximo</label>
                            <input type="number" min="0" value={form.stock_maximo} onChange={e => setForm({...form, stock_maximo: e.target.value})} placeholder="Opt" />
                        </div>
                        <div>
                            <label style={{ display: 'block', fontSize: '0.75rem', marginBottom: '6px', color: 'var(--text-300)' }}>Precio Coste (€)</label>
                            <input type="number" step="0.01" min="0" value={form.precio_coste} onChange={e => setForm({...form, precio_coste: e.target.value})} placeholder="0.00" />
                        </div>
                    </div>

                    <div style={{ gridColumn: 'span 2' }}>
                        <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '6px', color: 'var(--text-300)' }}>Código Barras (EAN)</label>
                        <input type="text" value={form.codigo_barras} onChange={e => setForm({...form, codigo_barras: e.target.value})} />
                    </div>

                    <div style={{ gridColumn: 'span 2', display: 'flex', alignItems: 'center', gap: '8px', marginTop: '8px' }}>
                        <input type="checkbox" checked={form.activo} onChange={e => setForm({...form, activo: e.target.checked})} style={{ width: 'auto' }} id="activo" />
                        <label htmlFor="activo" style={{ color: 'var(--text-200)', cursor: 'pointer' }}>Artículo activo para operaciones</label>
                    </div>

                    <div style={{ gridColumn: 'span 2', display: 'flex', justifyContent: 'flex-end', gap: '12px', marginTop: '16px', borderTop: '1px solid var(--border)', paddingTop: '20px' }}>
                        <button type="button" className="btn-ghost" onClick={() => setModalAbierto(false)}>Cancelar</button>
                        <button type="submit" className="btn-accent">Guardar Producto</button>
                    </div>
                </form>
            </Modal>
        </div>
    )
}
