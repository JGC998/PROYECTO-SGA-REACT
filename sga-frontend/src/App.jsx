import { useState } from 'react'
import { Toaster } from 'react-hot-toast'
import PanelInicio from './components/inicio/PanelInicio'
import GestionInventario from './components/productos/GestionInventario'
import './App.css'

function App() {
  const [seccion, setSeccion] = useState('inicio')

  return (
    <div className="container">
      <Toaster position="top-right" />

      {/* Barra de navegación superior simple */}
      <header className="main-header">
        <h1 onClick={() => setSeccion('inicio')} style={{ cursor: 'pointer' }}>
          🏠 SGA Chasito
        </h1>
        {seccion !== 'inicio' && (
          <button onClick={() => setSeccion('inicio')}>Volver al Panel</button>
        )}
      </header>

      <main>
        {seccion === 'inicio' && <PanelInicio alNavegar={setSeccion} />}
        {seccion === 'inventario' && <GestionInventario />}
      </main>
    </div>
  )
}

export default App