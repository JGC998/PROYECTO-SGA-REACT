export default function Modal({ titulo, children, onClose, isOpen }) {
    if (!isOpen) return null

    return (
        <div style={{
            position: 'fixed',
            top: 0, left: 0, right: 0, bottom: 0,
            backgroundColor: 'rgba(0,0,0,0.7)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000
        }}>
            <div className="card fade-in" style={{ 
                width: '100%', 
                maxWidth: '500px', 
                padding: '24px',
                position: 'relative'
            }}>
                <button 
                    onClick={onClose}
                    style={{
                        position: 'absolute',
                        top: '16px',
                        right: '16px',
                        background: 'transparent',
                        color: 'var(--text-300)',
                        fontSize: '1.2rem',
                    }}
                >
                    ✕
                </button>
                
                <h2 style={{ marginBottom: '20px', fontSize: '1.2rem' }}>{titulo}</h2>
                
                {children}
            </div>
        </div>
    )
}
