import api from './axios'

export const getPicking = async () => {
    const res = await api.get('/picking')
    return res.data
}

export const crearPicking = async (data) => {
    const res = await api.post('/picking', data)
    return res.data
}

export const asignarPicking = async (pickingId, operarioId) => {
    const res = await api.put(`/picking/${pickingId}/asignar?operario_id=${operarioId}`)
    return res.data
}

export const recogerLineaPicking = async (pickingId, lineaId, cantidad) => {
    const res = await api.put(`/picking/${pickingId}/lineas/${lineaId}/recoger?c_recogida=${cantidad}`)
    return res.data
}

export const completarPicking = async (pickingId) => {
    const res = await api.put(`/picking/${pickingId}/completar`)
    return res.data
}
