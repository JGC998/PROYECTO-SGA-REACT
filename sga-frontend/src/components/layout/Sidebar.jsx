import { NavLink } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'

export default function Sidebar() {
    const { isAdmin } = useAuth()

    return (
        <aside style={{ 
            width: 'var(--sidebar-w)', 
            backgroundColor: 'var(--bg-800)', 
            borderRight: '1px solid var(--border)',
            display: 'flex',
            flexDirection: 'column',
            height: '100vh',
            position: 'fixed'
        }}>
            {/* Branding */}
            <div style={{ padding: '24px', borderBottom: '1px solid var(--border)' }}>
                <h2 style={{ color: 'var(--accent)', fontSize: '1.5rem', marginBottom: '4px' }}>SGA Pro</h2>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-400)' }}>v2.0.0 — Enterprise</span>
            </div>

            {/* Nav */}
            <nav style={{ flex: 1, padding: '20px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '24px' }}>
                
                {/* Sección 1 */}
                <div>
                    <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: 'var(--text-400)', fontWeight: '600', marginBottom: '12px', letterSpacing: '0.05em' }}>
                        PRINCIPAL
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                        <NavLink to="/" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>
                            🏠 Dashboard
                        </NavLink>
                        <NavLink to="/inventario" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>
                            📦 Control de Stock
                        </NavLink>
                    </div>
                </div>

                {/* Sección 2 */}
                <div>
                    <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: 'var(--text-400)', fontWeight: '600', marginBottom: '12px', letterSpacing: '0.05em' }}>
                        OPERACIONES
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                        <NavLink to="/recepciones" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>
                            📥 Recepciones
                        </NavLink>
                        <NavLink to="/movimientos" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>
                            🔄 Movimientos Int.
                        </NavLink>
                        <NavLink to="/picking" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>
                            🛒 Picking
                        </NavLink>
                        <NavLink to="/expediciones" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>
                            📤 Expediciones
                        </NavLink>
                        <NavLink to="/inventarios" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>
                            📋 Recuentos Físicos
                        </NavLink>
                    </div>
                </div>

                {/* Sección 3 */}
                <div>
                    <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: 'var(--text-400)', fontWeight: '600', marginBottom: '12px', letterSpacing: '0.05em' }}>
                        CONFIGURACIÓN
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                        <NavLink to="/productos" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>
                            🏷️ Catálogo Productos
                        </NavLink>
                        <NavLink to="/ubicaciones" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>
                            📍 Almacenes / Ubic.
                        </NavLink>
                    </div>
                </div>

                {/* Admin */}
                {isAdmin && (
                    <div>
                        <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: 'var(--purple)', fontWeight: '600', marginBottom: '12px', letterSpacing: '0.05em' }}>
                            SISTEMA (ADMIN)
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                            <NavLink to="/historial" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>
                                📜 Historial Global
                            </NavLink>
                            <NavLink to="/usuarios" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>
                                👥 Usuarios y Roles
                            </NavLink>
                            <NavLink to="/auditoria" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>
                                🔒 Log de Auditoría
                            </NavLink>
                        </div>
                    </div>
                )}
            </nav>

            <style>{`
                .nav-item {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    padding: 8px 12px;
                    color: var(--text-200);
                    text-decoration: none;
                    border-radius: 8px;
                    font-size: 0.9rem;
                    transition: all 0.2s;
                }
                .nav-item:hover {
                    background: var(--surface-hover);
                    color: var(--text-100);
                }
                .nav-item.active {
                    background: var(--accent);
                    color: white;
                    font-weight: 500;
                }
            `}</style>
        </aside>
    )
}
