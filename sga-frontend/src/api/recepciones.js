import api from './axios'

export const getRecepciones = async () => {
    const res = await api.get('/recepciones')
    return res.data
}

export const crearRecepcion = async (data) => {
    const res = await api.post('/recepciones', data)
    return res.data
}

export const actualizarLineaRecepcion = async (recepcionId, lineaId, cantidad_recibida) => {
    const res = await api.put(`/recepciones/${recepcionId}/lineas/${lineaId}?cant_recibida=${cantidad_recibida}`)
    return res.data
}

export const confirmarRecepcion = async (recepcionId) => {
    const res = await api.put(`/recepciones/${recepcionId}/confirmar`)
    return res.data
}
