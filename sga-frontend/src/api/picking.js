import api from './axios'

export const getPicking = async () => {
    const res = await api.get('/picking/')
    return res.data
}

export const crearPicking = async (data) => {
    const res = await api.post('/picking/', data)
    return res.data
}

// operario_cod es ahora string (antes operario_id int)
export const asignarPicking = async (pickingId, operario_cod) => {
    const res = await api.put(`/picking/${pickingId}/asignar?operario_cod=${operario_cod}`)
    return res.data
}

export const recogerLineaPicking = async (pickingId, lineaId, cantidad) => {
    const res = await api.put(`/picking/${pickingId}/lineas/${lineaId}/recoger?cantidad_recogida=${cantidad}`)
    return res.data
}

export const completarPicking = async (pickingId) => {
    const res = await api.put(`/picking/${pickingId}/completar`)
    return res.data
}
