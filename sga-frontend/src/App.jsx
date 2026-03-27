import { Toaster } from 'react-hot-toast'
import { BrowserRouter, Routes, Route, Navigate, NavLink } from 'react-router-dom'
import PanelInicio from './components/inicio/PanelInicio'
import GestionInventario from './components/productos/GestionInventario'
import Movimientos from './components/movimientos/Movimientos'
import GestionUbicaciones from './components/ubicaciones/GestionUbicaciones'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <div className="container">
        <Toaster position="top-right" />

        <header className="main-header">
          <NavLink to="/" className="logo-link">
            <h1>🏠 SGA Chasito</h1>
          </NavLink>
          <nav className="nav-links">
            <NavLink to="/inventario" className={({ isActive }) => isActive ? 'nav-btn active' : 'nav-btn'}>
              📦 Inventario
            </NavLink>
            <NavLink to="/movimientos" className={({ isActive }) => isActive ? 'nav-btn active' : 'nav-btn'}>
              🔄 Movimientos
            </NavLink>
            <NavLink to="/ubicaciones" className={({ isActive }) => isActive ? 'nav-btn active' : 'nav-btn'}>
              📍 Ubicaciones
            </NavLink>
          </nav>
        </header>

        <main>
          <Routes>
            <Route path="/" element={<PanelInicio />} />
            <Route path="/inventario" element={<GestionInventario />} />
            <Route path="/movimientos" element={<Movimientos />} />
            <Route path="/ubicaciones" element={<GestionUbicaciones />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App