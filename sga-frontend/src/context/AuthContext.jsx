import { createContext, useState, useEffect } from 'react'
import { getMe, login as apiLogin } from '../api/auth'
import api from '../api/axios'

export const AuthContext = createContext()

export function AuthProvider({ children }) {
    const [usuario, setUsuario] = useState(null)
    const [token, setToken] = useState(localStorage.getItem('token') || null)
    const [cargando, setCargando] = useState(true)

    // Configurar el interceptor de axios para inyectar el token en todas las peticiones
    useEffect(() => {
        const interceptor = api.interceptors.request.use(
            config => {
                if (token) {
                    config.headers.Authorization = `Bearer ${token}`
                }
                return config
            },
            error => Promise.reject(error)
        )
        return () => api.interceptors.request.eject(interceptor)
    }, [token])

    // Cargar perfil del usuario si hay token
    useEffect(() => {
        const fetchPerfil = async () => {
            if (token) {
                try {
                    const data = await getMe()
                    setUsuario(data)
                } catch (error) {
                    // Token inválido o expirado
                    console.error("Token inválido o expirado")
                    logout()
                }
            }
            setCargando(false)
        }

        fetchPerfil()
    }, [token])

    const login = async (email, password) => {
        try {
            const data = await apiLogin(email, password)
            setToken(data.access_token)
            localStorage.setItem('token', data.access_token)
            
            // Inmediatamente obtener el perfil
            const perfil = await getMe()
            setUsuario(perfil)
            return true
        } catch (error) {
            throw error
        }
    }

    const logout = () => {
        setToken(null)
        setUsuario(null)
        localStorage.removeItem('token')
    }

    return (
        <AuthContext.Provider value={{
            usuario,
            token,
            cargando,
            login,
            logout,
            isAdmin: usuario?.rol === 'admin',
            isSupervisor: usuario?.rol === 'supervisor'
        }}>
            {children}
        </AuthContext.Provider>
    )
}
