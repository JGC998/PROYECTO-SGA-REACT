import api from './axios'

/**
 * Categorías = SUBFAMILIA en LIN (id es el código string SUBFAMCOD).
 * Proveedores = tabla PROVEEDOR en LIN (id es CLICOD string).
 */

export const getCategorias = async () => {
    const response = await api.get('/categorias/')
    return response
}

export const getProveedores = async (params = {}) => {
    const query = new URLSearchParams(params).toString()
    const response = await api.get(`/proveedores/${query ? '?' + query : ''}`)
    return response
}
