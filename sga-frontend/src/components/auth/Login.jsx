import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'

export default function Login() {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState(null)
    const [cargandoObj, setCargandoObj] = useState(false)
    const { login } = useAuth()
    const navigate = useNavigate()

    const manejarSubmit = async (e) => {
        e.preventDefault()
        setError(null)
        setCargandoObj(true)

        try {
            await login(email, password)
            navigate('/') // Redirigir al dashboard/inicio
        } catch (err) {
            setError(err.response?.data?.detail || 'Error al iniciar sesión')
        } finally {
            setCargandoObj(false)
        }
    }

    return (
        <div style={{ display: 'flex', minHeight: '100vh', background: 'var(--bg-900)' }}>
            
            {/* Panel Izquierdo - Branding */}
            <div style={{ 
                flex: 1, 
                backgroundColor: 'var(--bg-800)', 
                display: 'flex', 
                flexDirection: 'column',
                justifyContent: 'center',
                padding: '40px',
                borderRight: '1px solid var(--border)'
            }}>
                <div style={{ maxWidth: '400px', margin: '0 auto' }}>
                    <h1 style={{ color: 'var(--accent)', fontSize: '3rem', marginBottom: '10px' }}>
                        SGA Pro
                    </h1>
                    <p style={{ color: 'var(--text-300)', fontSize: '1.2rem', marginBottom: '40px' }}>
                        Sistema de Gestión de Almacén · Edición Enterprise
                    </p>
                    <ul style={{ listStyle: 'none', padding: 0, color: 'var(--text-200)', lineHeight: '2' }}>
                        <li>✓ Control de inventario en tiempo real</li>
                        <li>✓ Gestión multisucursal y multizona</li>
                        <li>✓ Trazabilidad completa de movimientos</li>
                        <li>✓ Accesos por roles (admin, supervisor, operario)</li>
                    </ul>
                </div>
            </div>

            {/* Panel Derecho - Formulario */}
            <div style={{ 
                flex: 1, 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center',
                padding: '40px' 
            }}>
                <div className="card fade-in" style={{ width: '100%', maxWidth: '400px', padding: '40px' }}>
                    <h2 style={{ marginBottom: '24px', textAlign: 'center' }}>Iniciar Sesión</h2>
                    
                    {error && (
                        <div style={{ 
                            background: 'var(--red-bg)', 
                            color: 'var(--red)', 
                            border: '1px solid var(--red)',
                            padding: '12px', 
                            borderRadius: '8px',
                            marginBottom: '20px',
                            fontSize: '0.9rem',
                            textAlign: 'center'
                        }}>
                            {error}
                        </div>
                    )}

                    <form onSubmit={manejarSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                        <div>
                            <label style={{ display: 'block', marginBottom: '8px', color: 'var(--text-200)' }}>Email</label>
                            <input 
                                type="email" 
                                value={email}
                                onChange={e => setEmail(e.target.value)}
                                placeholder="tu@email.com" 
                                required 
                            />
                        </div>
                        <div>
                            <label style={{ display: 'block', marginBottom: '8px', color: 'var(--text-200)' }}>Contraseña</label>
                            <input 
                                type="password" 
                                value={password}
                                onChange={e => setPassword(e.target.value)}
                                placeholder="••••••••" 
                                required 
                            />
                        </div>
                        <button 
                            type="submit" 
                            className="btn-accent" 
                            style={{ height: '42px', marginTop: '10px' }}
                            disabled={cargandoObj}
                        >
                            {cargandoObj ? 'Iniciando sesión...' : 'Entrar'}
                        </button>
                    </form>

                    <div style={{ marginTop: '30px', borderTop: '1px solid var(--border)', paddingTop: '20px' }}>
                        <p style={{ fontSize: '0.85rem', color: 'var(--text-400)', textAlign: 'center', marginBottom: '10px' }}>
                            Datos de prueba:
                        </p>
                        <div style={{ display: 'flex', gap: '10px', justifyContent: 'center' }}>
                            <button 
                                className="btn-outline" 
                                style={{ fontSize: '0.8rem', padding: '4px 8px' }}
                                onClick={() => { setEmail('admin@sga.com'); setPassword('admin123') }}
                                type="button"
                            >
                                Demo Admin
                            </button>
                            <button 
                                className="btn-outline" 
                                style={{ fontSize: '0.8rem', padding: '4px 8px' }}
                                onClick={() => { setEmail('supervisor@sga.com'); setPassword('sup123') }}
                                type="button"
                            >
                                Demo Sup
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
