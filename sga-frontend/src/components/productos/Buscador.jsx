export default function Buscador({ filtro, alCambiarFiltro }) {
    return (
        <div className="contenedor-buscador">
            <input
                type="text"
                placeholder="🔍 Buscar por nombre o SKU..."
                value={filtro}
                onChange={(e) => alCambiarFiltro(e.target.value)}
                className="input-buscador"
            />
        </div>
    )
}