import api from './axios'

export const getUbicaciones = (params = {}) => {
    const query = new URLSearchParams(params).toString()
    return api.get(`/ubicaciones/${query ? '?' + query : ''}`)
}

export const getUbicacion = (id) => api.get(`/ubicaciones/${id}`)

export const createUbicacion = (data) => api.post('/ubicaciones/', data)

export const updateUbicacion = (id, data) => api.put(`/ubicaciones/${id}`, data)

export const deleteUbicacion = (id) => api.delete(`/ubicaciones/${id}`)

export const getStockUbicacion = (id) => api.get(`/ubicaciones/${id}/stock`)
