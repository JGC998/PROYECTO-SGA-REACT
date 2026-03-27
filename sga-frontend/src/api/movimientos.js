import api from './axios'

export const getMovimientos = (params = {}) => {
    const query = new URLSearchParams()
    if (params.skip !== undefined) query.append('skip', params.skip)
    if (params.limit !== undefined) query.append('limit', params.limit)
    if (params.producto_id !== undefined) query.append('producto_id', params.producto_id)
    if (params.tipo) query.append('tipo', params.tipo)
    return api.get(`/movimientos?${query.toString()}`)
}

export const crearMovimientoInterno = async (data) => {
    const response = await api.post('/movimientos/interno', data)
    return response.data
}
