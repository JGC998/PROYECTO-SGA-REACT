import { Toaster } from 'react-hot-toast'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import AppLayout from './components/layout/AppLayout'
import RutaProtegida from './components/comunes/RutaProtegida'
import { AuthProvider } from './context/AuthContext'
import Login from './components/auth/Login'
import Dashboard from './components/dashboard/Dashboard'
import GestionStock from './components/stock/GestionStock'
import Movimientos from './components/movimientos/Movimientos'
import GestionProductos from './components/productos/GestionProductos'
import GestionAlmacenes from './components/almacenes/GestionAlmacenes'
import Recepciones from './components/recepciones/Recepciones'
import Picking from './components/operaciones/Picking'
import Expediciones from './components/expediciones/Expediciones'
import Inventarios from './components/inventarios/Inventarios'
import './index.css'

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Toaster position="top-right" />
        <Routes>
          {/* Ruta pública */}
          <Route path="/login" element={<Login />} />

          {/* Rutas protegidas dentro del Layout */}
          <Route path="/" element={<RutaProtegida><AppLayout /></RutaProtegida>}>
            <Route index element={<Dashboard />} />
            <Route path="inventario" element={<GestionStock />} />
            <Route path="productos" element={<GestionProductos />} />
            <Route path="movimientos" element={<Movimientos />} />
            <Route path="ubicaciones" element={<GestionAlmacenes />} />
            
            {/* Phase 3 */}
            <Route path="recepciones" element={<Recepciones />} />
            <Route path="picking" element={<Picking />} />
            <Route path="expediciones" element={<Expediciones />} />
            <Route path="inventarios" element={<Inventarios />} />
          </Route>

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App