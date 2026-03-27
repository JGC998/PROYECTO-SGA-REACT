import api from './axios'

export const getProductos = (skip = 0, limit = 50, filtros = {}) => {
    const query = new URLSearchParams({ skip, limit, ...filtros }).toString()
    return api.get(`/productos/?${query}`)
}

export const createProducto = (data) => api.post('/productos', data)

export const updateProducto = (id, data) => api.put(`/productos/${id}`, data)

export const deleteProducto = (id) => api.delete(`/productos/${id}`)

export const updateStock = (id, cambio, motivo = null) => {
    const params = new URLSearchParams({ cambio })
    if (motivo) params.append('motivo', motivo)
    return api.put(`/stock/${id}?${params.toString()}`)
}

export const fijarStock = (id, cantidad, motivo = null) => {
    const params = new URLSearchParams({ cantidad })
    if (motivo) params.append('motivo', motivo)
    return api.put(`/stock/${id}/fijar?${params.toString()}`)
}
