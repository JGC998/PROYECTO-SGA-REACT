import api from './axios'

export const getInventarios = async () => {
    const res = await api.get('/inventarios')
    return res.data
}

export const crearInventario = async (data) => {
    const res = await api.post('/inventarios', data)
    return res.data
}

export const actualizarLineaInventario = async (invId, lineaId, cant_fisica) => {
    const res = await api.put(`/inventarios/${invId}/lineas/${lineaId}?cant_fisica=${cant_fisica}`)
    return res.data
}

export const cerrarInventario = async (invId) => {
    const res = await api.post(`/inventarios/${invId}/cerrar`)
    return res.data
}
