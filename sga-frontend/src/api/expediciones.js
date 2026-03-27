import api from './axios'

export const getExpediciones = async () => {
    const res = await api.get('/expediciones')
    return res.data
}

export const crearExpedicion = async (data) => {
    const res = await api.post('/expediciones', data)
    return res.data
}

export const procesarExpedicion = async (expId, agencia, tracking) => {
    const res = await api.put(`/expediciones/${expId}/procesar?agencia=${agencia || ''}&tracking=${tracking || ''}`)
    return res.data
}
