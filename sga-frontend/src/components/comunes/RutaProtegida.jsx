import { Navigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'

export default function RutaProtegida({ children, roles_permitidos = [] }) {
    const { usuario, token, cargando } = useAuth()

    if (cargando) {
        return <div className="estado-info">Cargando sesión...</div>
    }

    if (!token) {
        return <Navigate to="/login" replace />
    }

    if (roles_permitidos.length > 0 && usuario && !roles_permitidos.includes(usuario.rol)) {
        return <div className="estado-error" style={{ margin: '40px' }}>
            Acceso denegado: No tienes permiso para ver esta sección.
        </div>
    }

    return children
}
