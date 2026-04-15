import api from './axios'

/**
 * API de Almacenes (tabla ALMACENES de LIN).
 * Los IDs son ahora strings de 2 chars (ALMCOD), no enteros.
 * No existen Zonas en LIN — se accede directamente a Ubicaciones.
 */
export const getAlmacenes = async () => {
    const response = await api.get('/almacenes/')
    return response.data
}

export const getAlmacen = async (codigo) => {
    const response = await api.get(`/almacenes/${codigo}`)
    return response.data
}

export const createAlmacen = async (data) => {
    const response = await api.post('/almacenes/', data)
    return response.data
}

export const updateAlmacen = async (codigo, data) => {
    const response = await api.put(`/almacenes/${codigo}`, data)
    return response.data
}

export const deleteAlmacen = async (codigo) => {
    const response = await api.delete(`/almacenes/${codigo}`)
    return response.data
}

// Lista las ubicaciones de un almacén concreto (reemplaza getZonas)
export const getUbicacionesAlmacen = async (codigo) => {
    const response = await api.get(`/almacenes/${codigo}/ubicaciones`)
    return response.data
}
