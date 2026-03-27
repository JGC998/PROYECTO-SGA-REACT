import { useEffect, useState } from 'react'
import toast from 'react-hot-toast'
import { getUbicaciones, createUbicacion } from '../../api/ubicaciones'

export default function GestionUbicaciones() {
    const [ubicaciones, setUbicaciones] = useState([])
    const [cargando, setCargando] = useState(true)
    const [error, setError] = useState(null)
    const [formulario, setFormulario] = useState({ codigo: '', descripcion: '' })

    const cargar = async () => {
        setCargando(true)
        setError(null)
        try {
            const res = await getUbicaciones()
            setUbicaciones(res.data)
        } catch (err) {
            setError('No se pudo cargar la lista de ubicaciones.')
        } finally {
            setCargando(false)
        }
    }

    useEffect(() => { cargar() }, [])

    const enviar = async (e) => {
        e.preventDefault()
        if (!formulario.codigo.trim()) {
            toast.error('El código no puede estar vacío')
            return
        }
        try {
            await createUbicacion({
                codigo: formulario.codigo.trim(),
                descripcion: formulario.descripcion.trim() || null,
            })
            toast.success('Ubicación creada')
            setFormulario({ codigo: '', descripcion: '' })
            cargar()
        } catch (err) {
            toast.error(err.response?.data?.detail || 'Error al crear la ubicación')
        }
    }

    return (
        <>
            <h2>📍 Gestión de Ubicaciones</h2>

            <form className="product-form" onSubmit={enviar}>
                <input
                    placeholder="Código (ej: A-01-01)"
                    value={formulario.codigo}
                    required
                    onChange={e => setFormulario({ ...formulario, codigo: e.target.value })}
                />
                <input
                    placeholder="Descripción (opcional)"
                    value={formulario.descripcion}
                    onChange={e => setFormulario({ ...formulario, descripcion: e.target.value })}
                />
                <button type="submit">Añadir</button>
            </form>

            {cargando && <p className="estado-info">Cargando ubicaciones…</p>}
            {!cargando && error && <p className="estado-error">{error}</p>}

            {!cargando && !error && (
                <table>
                    <thead>
                        <tr>
                            <th>Código</th>
                            <th>Descripción</th>
                        </tr>
                    </thead>
                    <tbody>
                        {ubicaciones.length > 0 ? (
                            ubicaciones.map(u => (
                                <tr key={u.id}>
                                    <td><strong>{u.codigo}</strong></td>
                                    <td>{u.descripcion || '—'}</td>
                                </tr>
                            ))
                        ) : (
                            <tr>
                                <td colSpan="2" style={{ textAlign: 'center', padding: '20px' }}>
                                    No hay ubicaciones registradas.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            )}
        </>
    )
}
