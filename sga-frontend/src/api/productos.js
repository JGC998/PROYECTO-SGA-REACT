import api from './axios'

/**
 * API de Productos (tabla ARTICULO de LIN).
 * Los IDs son ahora strings (ARTCOD), no enteros.
 */
export const getProductos = (skip = 0, limit = 50, filtros = {}) => {
    const query = new URLSearchParams({ skip, limit, ...filtros }).toString()
    return api.get(`/productos/?${query}`)
}

export const getProducto = (sku) => api.get(`/productos/${sku}`)

export const createProducto = (data) => api.post('/productos/', data)

// id es ahora el SKU (string)
export const updateProducto = (sku, data) => api.put(`/productos/${sku}`, data)

// Borrado lógico — pone ARTMOS=1 (ocultar)
export const deleteProducto = (sku) => api.delete(`/productos/${sku}`)
