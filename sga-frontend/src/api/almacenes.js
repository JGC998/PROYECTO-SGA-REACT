import api from './axios'

export const getAlmacenes = async () => {
    const response = await api.get('/almacenes')
    return response.data
}

export const getZonas = async (almacenId) => {
    const response = await api.get(`/almacenes/${almacenId}/zonas`)
    return response.data
}

export const createZona = async (almacenId, data) => {
    const response = await api.post(`/almacenes/${almacenId}/zonas`, data)
    return response.data
}

export const createUbicacion = async (data) => {
    const response = await api.post('/ubicaciones', data)
    return response.data
}

export const getUbicacionesPorZona = async (zonaId) => {
    // El backend espera parámetros en la query si los tuvieramos, pero podemos usar el mapa de stock por ahora, o crear endpoint en el futuro.
    // Usaremos llamadas a las ubicaciones base filtradas si fuera necesario.
}
