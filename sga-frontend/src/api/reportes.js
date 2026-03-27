import api from './axios'

export const getResumen = () => api.get('/reportes/resumen')

export const getStockBajo = () => api.get('/reportes/stock-bajo')
