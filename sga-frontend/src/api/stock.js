import api from './axios'

export const getStock = async () => {
    const res = await api.get('/stock')
    return res.data
}

export const getMapaZona = async (zonaId) => {
    const response = await api.get(`/stock/mapa/${zonaId}`)
    return response.data
}

export const fijarStock = async (productoId, cantidad, motivo) => {
    const response = await api.put(`/stock/${productoId}/fijar?cantidad=${cantidad}&motivo=${motivo || ''}`)
    return response.data
}
