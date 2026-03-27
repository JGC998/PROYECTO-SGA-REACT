import api from './axios'

export const login = async (email, password) => {
    // fastapi OAuth2 password flow requires form data
    const formData = new URLSearchParams()
    formData.append('username', email)
    formData.append('password', password)

    const response = await api.post('/auth/login', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
    return response.data
}

export const getMe = async () => {
    const response = await api.get('/auth/me')
    return response.data
}
