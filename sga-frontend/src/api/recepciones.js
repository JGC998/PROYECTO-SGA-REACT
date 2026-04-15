import api from './axios'

export const getRecepciones = async () => {
    const res = await api.get('/recepciones/')
    return res.data
}

export const crearRecepcion = async (data) => {
    const res = await api.post('/recepciones/', data)
    return res.data
}

export const actualizarLineaRecepcion = async (recepcionId, lineaId, cantidad_recibida, ubicacion_destino = null, lote = null) => {
    const params = new URLSearchParams({ cant_recibida: cantidad_recibida })
    if (ubicacion_destino) params.append('ubicacion_destino', ubicacion_destino)
    if (lote) params.append('lote', lote)
    const res = await api.put(`/recepciones/${recepcionId}/lineas/${lineaId}?${params.toString()}`)
    return res.data
}

export const confirmarRecepcion = async (recepcionId) => {
    const res = await api.put(`/recepciones/${recepcionId}/confirmar`)
    return res.data
}
