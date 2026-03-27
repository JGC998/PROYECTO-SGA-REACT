export default function KpiCard({ titulo, valor, subtitulo, tendencia, color = 'var(--accent)' }) {
    return (
        <div className="card fade-in" style={{ borderTop: `3px solid ${color}` }}>
            <h3 style={{ fontSize: '0.85rem', color: 'var(--text-400)', textTransform: 'uppercase', marginBottom: '8px' }}>
                {titulo}
            </h3>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--text-100)', marginBottom: '8px' }}>
                {valor}
            </div>
            
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                {tendencia && (
                    <span style={{ 
                        fontSize: '0.75rem', 
                        fontWeight: 'bold',
                        color: tendencia > 0 ? 'var(--green)' : tendencia < 0 ? 'var(--red)' : 'var(--text-400)' 
                    }}>
                        {tendencia > 0 ? '↑' : tendencia < 0 ? '↓' : '—'} {Math.abs(tendencia)}%
                    </span>
                )}
                <span style={{ fontSize: '0.75rem', color: 'var(--text-400)' }}>
                    {subtitulo}
                </span>
            </div>
        </div>
    )
}
