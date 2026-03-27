import api from './axios'

export const getCategorias = async () => {
    const response = await api.get('/categorias')
    return response.data
}

export const getProveedores = async () => {
    const response = await api.get('/proveedores')
    return response.data
}
