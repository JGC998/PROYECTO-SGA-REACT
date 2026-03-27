import { useNavigate } from 'react-router-dom'

export default function PanelInicio() {
    const navigate = useNavigate()

    return (
        <div className="dashboard">
            <h2>Bienvenido al SGA Chasito Pro</h2>
            <p>Selecciona un módulo para empezar a trabajar:</p>

            <div className="grid-modulos">
                <div className="tarjeta" onClick={() => navigate('/inventario')}>
                    <span className="icono">📦</span>
                    <h3>Inventario</h3>
                    <p>Control de stock y productos</p>
                </div>

                <div className="tarjeta" onClick={() => navigate('/movimientos')}>
                    <span className="icono">🔄</span>
                    <h3>Movimientos</h3>
                    <p>Historial de entradas y salidas</p>
                </div>

                <div className="tarjeta" onClick={() => navigate('/ubicaciones')}>
                    <span className="icono">📍</span>
                    <h3>Ubicaciones</h3>
                    <p>Gestión de pasillos y estanterías</p>
                </div>
            </div>
        </div>
    )
}