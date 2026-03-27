import { useAuth } from '../../hooks/useAuth'

export default function Topbar() {
    const { usuario, logout } = useAuth()

    return (
        <header style={{
            height: 'var(--header-h)',
            backgroundColor: 'var(--bg-800)',
            borderBottom: '1px solid var(--border)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '0 24px',
            position: 'sticky',
            top: 0,
            zIndex: 10
        }}>
            
            {/* Buscador global vacio por ahora */}
            <div style={{ width: '300px' }}>
                <input 
                    type="text" 
                    placeholder="Buscar (Ctrl+K)..." 
                    style={{ 
                        height: '36px', 
                        width: '100%', 
                        background: 'var(--bg-900)',
                        borderRadius: '20px'
                    }} 
                />
            </div>

            {/* Perfil */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                <div style={{ textAlign: 'right' }}>
                    <div style={{ fontWeight: '500', color: 'var(--text-100)', fontSize: '0.9rem' }}>
                        {usuario?.nombre}
                    </div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-400)', textTransform: 'capitalize' }}>
                        Rol: {usuario?.rol}
                    </div>
                </div>
                
                <div style={{
                    width: '36px',
                    height: '36px',
                    borderRadius: '50%',
                    background: 'var(--accent)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    fontWeight: 'bold',
                    fontSize: '1rem'
                }}>
                    {usuario?.nombre?.charAt(0).toUpperCase()}
                </div>

                <button 
                    onClick={logout}
                    className="btn-outline" 
                    style={{ padding: '6px 12px', fontSize: '0.8rem' }}
                >
                    Salir
                </button>
            </div>
            
        </header>
    )
}
