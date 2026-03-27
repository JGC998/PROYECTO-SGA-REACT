import { useState, useEffect } from 'react'
import { getExpediciones, crearExpedicion, procesarExpedicion } from '../../api/expediciones'
import { getPicking } from '../../api/picking'
import EstadoCarga from '../comunes/EstadoCarga'
import Modal from '../comunes/Modal'
import Badge from '../comunes/Badge'
import toast from 'react-hot-toast'
import { format } from 'date-fns'

export default function Expediciones() {
    const [expediciones, setExpediciones] = useState([])
    const [pickings, setPickings] = useState([])
    const [cargando, setCargando] = useState(true)

    const [modalCrear, setModalCrear] = useState(false)
    const [formExp, setFormExp] = useState({ picking_id: '', agencia_transporte: '', tracking_number: '' })

    const cargar = async () => {
        try {
            setCargando(true)
            const [exps, piks] = await Promise.all([getExpediciones(), getPicking()])
            setExpediciones(exps)
            // Solo pickings completados que no tengan ya una expedición
            const expPikIds = exps.map(e => e.picking_id).filter(id => id)
            setPickings(piks.filter(p => p.estado === 'completado' && !expPikIds.includes(p.id)))
        } catch(e) {
            toast.error("Error al cargar Expediciones")
        } finally {
            setCargando(false)
        }
    }

    useEffect(() => { cargar() }, [])

    const handleCrear = async (e) => {
        e.preventDefault()
        try {
            await crearExpedicion({
                codigo: `EXP-${Date.now()}`,
                picking_id: formExp.picking_id ? parseInt(formExp.picking_id) : null,
                agencia_transporte: formExp.agencia_transporte,
                tracking_number: formExp.tracking_number
            })
            toast.success("Expedición Creada en Dársena")
            setModalCrear(false)
            cargar()
        } catch (err) {
            toast.error("Error al crear la salida")
        }
    }

    const handleEnviar = async (expId) => {
        if(!window.confirm("¿Confirmar salida del camión/envío físico?")) return
        try {
            await procesarExpedicion(expId)
            toast.success("Expedición marcada como enviada")
            cargar()
        } catch (err) {
            toast.error("Error al procesar envío")
        }
    }

    return (
        <div className="fade-in">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                <div>
                    <h1 className="page-title">Salidas y Expediciones</h1>
                    <p className="page-subtitle">Embarque de pedidos completados para su envío final al cliente/destino.</p>
                </div>
                <button className="btn-accent" onClick={() => { setFormExp({picking_id:'', agencia_transporte:'', tracking_number:''}); setModalCrear(true); }}>
                    + Preparar Nueva Expedición
                </button>
            </div>

            {cargando ? <EstadoCarga /> : (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '24px' }}>
                    {expediciones.length === 0 && <p style={{ color: 'var(--text-400)' }}>No hay envíos en curso ni históricos.</p>}
                    
                    {expediciones.map(e => (
                        <div key={e.id} className="card fade-in" style={{ padding: '24px', display: 'flex', flexDirection: 'column', borderTop: e.estado === 'enviada' ? '4px solid var(--green)' : '4px solid var(--purple)' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '16px' }}>
                                <h3 style={{ margin: 0 }}>{e.codigo}</h3>
                                {e.estado === 'enviada' ? <Badge texto="Enviada" variante="success" /> : <Badge texto="En Preparación" variante="default" />}
                            </div>
                            
                            <div style={{ marginBottom: '16px', color: 'var(--text-300)', fontSize: '0.9rem', flex: 1 }}>
                                <p style={{ margin: '0 0 8px 0' }}><strong>Creada:</strong> {format(new Date(e.creado_en), 'dd/MM/yyyy HH:mm')}</p>
                                <p style={{ margin: '0 0 8px 0' }}><strong>Ref. Picking:</strong> {e.picking_id ? `PIK ID ${e.picking_id}` : 'Manual / Sin Ref'}</p>
                                <p style={{ margin: '0 0 8px 0' }}><strong>Transportista:</strong> {e.agencia_transporte || 'Por Defecto'}</p>
                                <p style={{ margin: '0 0 8px 0' }}><strong>Tracking:</strong> {e.tracking_number || 'N/A'}</p>
                                {e.fecha_envio && (
                                    <p style={{ margin: '0 0 8px 0', color: 'var(--text-100)' }}><strong>Salida Efectiva:</strong> {format(new Date(e.fecha_envio), 'dd/MM/yyyy HH:mm')}</p>
                                )}
                            </div>

                            {e.estado === 'preparacion' && (
                                <button className="btn-accent" style={{ background: 'var(--purple)', width: '100%' }} onClick={() => handleEnviar(e.id)}>
                                    🚚 Validar Carga y Dar Salida
                                </button>
                            )}
                        </div>
                    ))}
                </div>
            )}

            <Modal isOpen={modalCrear} onClose={() => setModalCrear(false)} titulo="Planificar Carga / Expedición">
                <form onSubmit={handleCrear} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    <div>
                        <label>Vincular a Pedido Preparado (Picking) *</label>
                        <select required value={formExp.picking_id} onChange={e => setFormExp({...formExp, picking_id: e.target.value})}>
                            <option value="">Selecciona Picking...</option>
                            {pickings.map(p => <option key={p.id} value={p.id}>{p.codigo} - {p.lineas.length} Líneas a Enviar</option>)}
                        </select>
                    </div>
                    <div>
                        <label>Agencia de Transporte (Opcional)</label>
                        <input value={formExp.agencia_transporte} onChange={e => setFormExp({...formExp, agencia_transporte: e.target.value})} placeholder="SEUR, DHL..." />
                    </div>
                    <div>
                        <label>Número de Seguimiento (Tracking)</label>
                        <input value={formExp.tracking_number} onChange={e => setFormExp({...formExp, tracking_number: e.target.value})} placeholder="XXX-YYY-ZZZ" />
                    </div>

                    <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px', marginTop: '16px' }}>
                        <button type="submit" className="btn-accent" style={{ background: 'var(--purple)' }}>Crear Etiqueta de Salida</button>
                    </div>
                </form>
            </Modal>
        </div>
    )
}
