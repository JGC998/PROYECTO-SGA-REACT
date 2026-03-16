export default function PanelInicio({ alNavegar }) {
    return (
        <div className="dashboard">
            <h2>Bienvenido al SGA Chasito Pro</h2>
            <p>Selecciona un módulo para empezar a trabajar:</p>

            <div className="grid-modulos">
                <div className="tarjeta" onClick={() => alNavegar('inventario')}>
                    <span className="icono">📦</span>
                    <h3>Inventario</h3>
                    <p>Control de stock y productos</p>
                </div>

                <div className="tarjeta deshabilitada">
                    <span className="icono">📍</span>
                    <h3>Ubicaciones</h3>
                    <p>Gestión de pasillos y estanterías (Próximamente)</p>
                </div>

                <div className="tarjeta deshabilitada">
                    <span className="icono">🚚</span>
                    <h3>Pedidos</h3>
                    <p>Entradas y salidas de material (Próximamente)</p>
                </div>
            </div>
        </div>
    )
}