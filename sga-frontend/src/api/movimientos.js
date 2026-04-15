import api from './axios'

/**
 * API de Movimientos (tabla ALBARANCS de LIN — solo lectura).
 * Se eliminó el endpoint de creación manual (crearMovimientoInterno)
 * ya que los movimientos los genera el ERP legacy.
 */
export const getMovimientos = (params = {}) => {
    const query = new URLSearchParams()
    if (params.skip !== undefined) query.append('skip', params.skip)
    if (params.limit !== undefined) query.append('limit', params.limit)
    // Filtros adaptados a ALBARANCS
    if (params.articulo_cod) query.append('articulo_cod', params.articulo_cod)
    if (params.almacen_cod) query.append('almacen_cod', params.almacen_cod)
    if (params.ubicacion) query.append('ubicacion', params.ubicacion)
    return api.get(`/movimientos?${query.toString()}`)
}

export const getMovimientosRecientes = (limit = 20) => {
    return api.get(`/movimientos/recientes?limit=${limit}`)
}
