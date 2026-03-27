export default function EstadoVacio({ titulo, descripcion, accion }) {
    return (
        <div style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '40px',
            textAlign: 'center',
            background: 'var(--surface)',
            borderRadius: '12px',
            border: '1px dashed var(--border)'
        }}>
            <div style={{ fontSize: '3rem', marginBottom: '16px', opacity: 0.5 }}>📭</div>
            <h3 style={{ color: 'var(--text-100)', marginBottom: '8px' }}>{titulo}</h3>
            <p style={{ color: 'var(--text-300)', marginBottom: '20px', maxWidth: '400px' }}>
                {descripcion}
            </p>
            {accion && (
                <button className="btn-accent" onClick={accion.onClick}>
                    {accion.texto}
                </button>
            )}
        </div>
    )
}
