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
    
    // Formulario adaptado a los campos de la tabla ARTICULO de LIN
    const defaultForm = {
        sku: '', nombre: '', barcode: '', barcode_caja: '', codigo_largo: '',
        unidad_medida: '', peso_uni: 0, stock_min: 0, stock_max: 0, precio_coste: 0,
        grupo: '', material: '', color: '', imagen_url: '', oculto: 0
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
        setEditando(p.sku)  // La PK es el SKU (str)
        setForm({
            sku: p.sku,
            nombre: p.nombre || '',
            barcode: p.barcode || '',
            barcode_caja: p.barcode_caja || '',
            codigo_largo: p.codigo_largo || '',
            unidad_medida: p.unidad_medida || '',
            peso_uni: p.peso_uni || 0,
            stock_min: p.stock_min ?? 0,
            stock_max: p.stock_max ?? 0,
            precio_coste: p.precio_coste || 0,
            grupo: p.grupo || '',
            material: p.material || '',
            color: p.color || '',
            imagen_url: p.imagen_url || '',
            oculto: p.oculto ?? 0
        })
        setModalAbierto(true)
    }

    const handleGuardar = async (e) => {
        e.preventDefault()
        try {
            const data = {
                ...form,
                // Nunca parseInt en campos string de LIN
                sku: form.sku.trim().toUpperCase(),
                nombre: form.nombre.trim(),
                stock_min: parseFloat(form.stock_min) || 0,
                stock_max: parseFloat(form.stock_max) || 0,
                precio_coste: parseFloat(form.precio_coste) || 0,
                peso_uni: parseFloat(form.peso_uni) || 0,
            }

            if (editando) {
                await updateProducto(editando, data)  // editando es el SKU (str)
                toast.success('Artículo actualizado')
            } else {
                await createProducto(data)
                toast.success('Artículo creado exitosamente')
            }
            setModalAbierto(false)
            cargarDatos()
        } catch (err) {
            toast.error(err.response?.data?.detail || 'Error al guardar el artículo')
        }
    }

    const handleBorrar = async (sku) => {
        if (!window.confirm(`¿Marcar el artículo '${sku}' como inactivo? Se ocultará de las operaciones pero su historial de stock se conserva.`)) return
        try {
            await deleteProducto(sku)  // sku es string
            toast.success('Artículo marcado como inactivo')
            cargarDatos()
        } catch (err) {
            toast.error(err.response?.data?.detail || 'Error al desactivar')
        }
    }

    const prodFiltrados = productos.filter(p =>
        (p.sku || '').toLowerCase().includes(filtroTexto.toLowerCase()) ||
        (p.nombre || '').toLowerCase().includes(filtroTexto.toLowerCase()) ||
        (p.barcode || '').toLowerCase().includes(filtroTexto.toLowerCase())
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
                    placeholder="Buscar por SKU, nombre o código de barras..." 
                    value={filtroTexto} 
                    onChange={e => setFiltroTexto(e.target.value)}
                    style={{ flex: 1 }}
                />
                <select 
                    value={filtroCat} 
                    onChange={e => setFiltroCat(e.target.value)}
                    style={{ width: '250px' }}
                >
                    <option value="">Todos los grupos</option>
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
                                    return (
                                        <tr key={p.sku} style={{ borderBottom: '1px solid var(--border)' }}>
                                            <td style={{ padding: '16px', fontWeight: '500', color: 'var(--accent)', fontFamily: 'monospace' }}>{p.sku}</td>
                                            <td style={{ padding: '16px' }}>
                                                {p.nombre}
                                                <div style={{ fontSize: '0.8rem', color: 'var(--text-400)' }}>
                                                    EAN: {p.barcode || 'N/A'} {p.unidad_medida ? `· ${p.unidad_medida}` : ''}
                                                </div>
                                            </td>
                                            <td style={{ padding: '16px' }}>{p.grupo || <span style={{ color: 'var(--text-400)' }}>Sin grupo</span>}</td>
                                            <td style={{ padding: '16px', color: 'var(--text-300)' }}>
                                                <span style={{ color: p.cantidad <= (p.stock_min || 0) && p.cantidad > 0 ? 'var(--red)' : 'inherit' }}>
                                                    Stock: {p.cantidad ?? 0}
                                                </span><br/>
                                                <span style={{ fontSize: '0.8rem' }}>Mín: {p.stock_min ?? 0} / Máx: {p.stock_max || 'N/A'}</span>
                                            </td>
                                            <td style={{ padding: '16px' }}>
                                                {p.activo ? <Badge texto="Activo" variante="success" /> : <Badge texto="Inactivo" variante="default" />}
                                            </td>
                                            <td style={{ padding: '16px', textAlign: 'right' }}>
                                                <button className="btn-ghost" onClick={() => abrirEditar(p)}>✏️</button>
                                                <button className="btn-ghost" onClick={() => handleBorrar(p.sku)} style={{ color: 'var(--red)' }}>🗑️</button>
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
                    
                    <div>
                        <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '6px', color: 'var(--text-300)' }}>SKU / Código Artículo (ARTCOD) *</label>
                        <input
                            required type="text" value={form.sku}
                            onChange={e => setForm({...form, sku: e.target.value.toUpperCase().trim()})}
                            disabled={!!editando}  // No se puede cambiar el código en edición
                            title="Código único del artículo (máx. 10 chars)"
                            maxLength={10}
                        />
                    </div>

                    <div>
                        <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '6px', color: 'var(--text-300)' }}>Nombre *</label>
                        <input required type="text" value={form.nombre} onChange={e => setForm({...form, nombre: e.target.value})} maxLength={50} />
                    </div>

                    <div>
                        <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '6px', color: 'var(--text-300)' }}>Código de Barras (EAN)</label>
                        <input type="text" value={form.barcode} onChange={e => setForm({...form, barcode: e.target.value})} maxLength={30} />
                    </div>

                    <div>
                        <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '6px', color: 'var(--text-300)' }}>Código de Barras Caja</label>
                        <input type="text" value={form.barcode_caja} onChange={e => setForm({...form, barcode_caja: e.target.value})} maxLength={30} />
                    </div>

                    <div>
                        <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '6px', color: 'var(--text-300)' }}>Grupo/Subfamilia (ARTGRUCOD)</label>
                        <input type="text" value={form.grupo} onChange={e => setForm({...form, grupo: e.target.value.toUpperCase()})} maxLength={5} placeholder="Ej: FERR" />
                    </div>

                    <div>
                        <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '6px', color: 'var(--text-300)' }}>Unidad de Medida</label>
                        <input type="text" value={form.unidad_medida} onChange={e => setForm({...form, unidad_medida: e.target.value})} maxLength={20} placeholder="kg, ud, caja..." />
                    </div>

                    <div style={{ padding: '16px', background: 'var(--bg-900)', borderRadius: '8px', gridColumn: 'span 2', display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr', gap: '12px' }}>
                        <div>
                            <label style={{ display: 'block', fontSize: '0.75rem', marginBottom: '6px', color: 'var(--text-300)' }}>Peso Unitario</label>
                            <input type="number" step="0.001" min="0" value={form.peso_uni} onChange={e => setForm({...form, peso_uni: e.target.value})} />
                        </div>
                        <div>
                            <label style={{ display: 'block', fontSize: '0.75rem', marginBottom: '6px', color: 'var(--text-300)' }}>Stock Mínimo</label>
                            <input type="number" step="0.01" min="0" value={form.stock_min} onChange={e => setForm({...form, stock_min: e.target.value})} />
                        </div>
                        <div>
                            <label style={{ display: 'block', fontSize: '0.75rem', marginBottom: '6px', color: 'var(--text-300)' }}>Stock Máximo</label>
                            <input type="number" step="0.01" min="0" value={form.stock_max} onChange={e => setForm({...form, stock_max: e.target.value})} placeholder="Opt" />
                        </div>
                        <div>
                            <label style={{ display: 'block', fontSize: '0.75rem', marginBottom: '6px', color: 'var(--text-300)' }}>Precio Coste (€)</label>
                            <input type="number" step="0.01" min="0" value={form.precio_coste} onChange={e => setForm({...form, precio_coste: e.target.value})} placeholder="0.00" />
                        </div>
                    </div>

                    <div>
                        <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '6px', color: 'var(--text-300)' }}>Material</label>
                        <input type="text" value={form.material} onChange={e => setForm({...form, material: e.target.value})} maxLength={20} />
                    </div>

                    <div>
                        <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '6px', color: 'var(--text-300)' }}>Color</label>
                        <input type="text" value={form.color} onChange={e => setForm({...form, color: e.target.value})} maxLength={20} />
                    </div>

                    <div style={{ gridColumn: 'span 2', display: 'flex', alignItems: 'center', gap: '8px', marginTop: '8px' }}>
                        <input
                            type="checkbox"
                            checked={form.oculto === 0}
                            onChange={e => setForm({...form, oculto: e.target.checked ? 0 : 1})}
                            style={{ width: 'auto' }}
                            id="activo-art"
                        />
                        <label htmlFor="activo-art" style={{ color: 'var(--text-200)', cursor: 'pointer' }}>Artículo activo (ARTMOS = visible)</label>
                    </div>

                    <div style={{ gridColumn: 'span 2', display: 'flex', justifyContent: 'flex-end', gap: '12px', marginTop: '16px', borderTop: '1px solid var(--border)', paddingTop: '20px' }}>
                        <button type="button" className="btn-ghost" onClick={() => setModalAbierto(false)}>Cancelar</button>
                        <button type="submit" className="btn-accent">Guardar Artículo</button>
                    </div>
                </form>
            </Modal>
        </div>
    )
}
