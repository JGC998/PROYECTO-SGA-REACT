import api from './axios'

/**
 * API de Stock (tabla STOCK de LIN).
 * El stock se identifica por la combinación articulo_cod + ubicacion + lote.
 * No hay endpoint PUT /stock/:id/fijar — los ajustes se hacen via inventarios.
 */

// Lista el stock (con filtros opcionales)
export const getStock = async (params = {}) => {
    const query = new URLSearchParams(params).toString()
    const res = await api.get(`/stock/${query ? '?' + query : ''}`)
    return res.data
}

// Resumen de stock total por artículo (útil para dashboard y alertas)
export const getResumenStock = async () => {
    const res = await api.get('/stock/resumen')
    return res.data
}

// Stock de un artículo concreto por su SKU
export const getStockArticulo = async (sku) => {
    const res = await api.get(`/stock/${sku}`)
    return res.data
}
