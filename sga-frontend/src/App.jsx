import { useEffect, useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [productos, setProductos] = useState([])
  const [form, setForm] = useState({ sku: '', nombre: '', stock_minimo: 0 });

  // 1. Función para cargar los productos (reutilizable)
  const cargarProductos = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:8000/productos')
      setProductos(res.data)
    } catch (err) {
      console.error("Error cargando productos", err)
    }
  }

  // 2. Ejecutar al cargar la web
  useEffect(() => {
    cargarProductos()
  }, [])

  // 3. Crear producto
  const handleCrear = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://127.0.0.1:8000/productos', form);
      setForm({ sku: '', nombre: '', stock_minimo: 0 }); // Limpiar formulario
      cargarProductos(); // Actualizar lista sin recargar página
    } catch (err) {
      console.error("Error al crear", err)
    }
  };

  {/* Función para cambiar stock */ }
  const handleStock = async (id, cantidad) => {
    try {
      await axios.put(`http://127.0.0.1:8000/stock/${id}?cambio=${cantidad}`)
      cargarProductos()
    } catch (err) {
      console.error("Error al actualizar stock", err)
    }
  }

  // 4. Eliminar producto
  const handleEliminar = async (id) => {
    if (window.confirm("¿Seguro que quieres borrar este producto?")) {
      try {
        await axios.delete(`http://127.0.0.1:8000/productos/${id}`)
        cargarProductos() // Actualizar lista
      } catch (err) {
        console.error("Error al borrar", err)
      }
    }
  }

  return (
    <div className="container">
      <h1>📦 SGA - Chasito Pro</h1>

      {/* Formulario con los estilos del CSS */}
      <form className="product-form" onSubmit={handleCrear}>
        <input
          placeholder="SKU"
          value={form.sku}
          onChange={e => setForm({ ...form, sku: e.target.value })}
          required
        />
        <input
          placeholder="Nombre"
          value={form.nombre}
          onChange={e => setForm({ ...form, nombre: e.target.value })}
          required
        />
        <input
          type="number"
          placeholder="Stock Mínimo"
          value={form.stock_minimo}
          onChange={e => setForm({ ...form, stock_minimo: e.target.value })}
        />
        <button type="submit">Añadir Producto</button>
      </form>

      <table>
        <thead>
          <tr>
            <th>SKU</th>
            <th>Nombre</th>
            <th>Stock Mínimo</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {productos.map(p => (
            <tr key={p.id}>
              <td><strong>{p.sku}</strong></td>
              <td>{p.nombre}</td>
              <td>{p.stock_minimo} uds.</td>
              <td>
                <button className="btn-delete" onClick={() => handleEliminar(p.id)}>
                  Eliminar
                </button>
              </td>
              {/* En el map de la tabla, cambia la parte del stock por esto: */}
              <td>
                <button className="btn-stock" onClick={() => handleStock(p.id, -1)}>-</button>
                <span style={{ margin: '0 10px', fontWeight: 'bold' }}>
                  {p.cantidad}
                </span>
                <button className="btn-stock" onClick={() => handleStock(p.id, 1)}>+</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default App