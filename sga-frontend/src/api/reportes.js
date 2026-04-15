import api from './axios'

export const getResumen = async () => {
    const response = await api.get('/reportes/resumen')
    return response.data
}

export const getMovimientosPorDia = async (dias = 7) => {
    const response = await api.get(`/reportes/movimientos-por-dia?dias=${dias}`)
    return response.data
}

export const getOcupacionZonas = async () => {
    const response = await api.get('/reportes/ocupacion-almacenes')
    return response.data
}
