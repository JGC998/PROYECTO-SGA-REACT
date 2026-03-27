export default function Badge({ texto, variante = 'default' }) {
    let bg, color, border

    switch (variante) {
        case 'success':
        case 'entrada':
        case 'completada':
            bg = 'var(--green-bg)'
            color = 'var(--green)'
            border = '1px solid rgba(16, 185, 129, 0.3)'
            break
        case 'warning':
        case 'pendiente':
        case 'urgente':
            bg = 'var(--yellow-bg)'
            color = 'var(--yellow)'
            border = '1px solid rgba(245, 158, 11, 0.3)'
            break
        case 'danger':
        case 'salida':
        case 'incidencia':
            bg = 'var(--red-bg)'
            color = 'var(--red)'
            border = '1px solid rgba(239, 68, 68, 0.3)'
            break
        case 'info':
        case 'en_proceso':
            bg = 'var(--cyan-bg)'
            color = 'var(--cyan)'
            border = '1px solid rgba(6, 182, 212, 0.3)'
            break
        default:
            bg = 'var(--surface-hover)'
            color = 'var(--text-200)'
            border = '1px solid var(--border)'
    }

    return (
        <span style={{
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '2px 8px',
            borderRadius: '12px',
            fontSize: '0.75rem',
            fontWeight: '600',
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
            background: bg,
            color: color,
            border: border
        }}>
            {texto}
        </span>
    )
}
