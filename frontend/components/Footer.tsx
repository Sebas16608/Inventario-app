'use client'

export function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="w-full" style={{ backgroundColor: '#1A1A1A' }}>
      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex flex-col items-center md:items-start text-center md:text-left">
            <span 
              className="text-xl font-semibold tracking-tight"
              style={{ color: '#FF4500' }}
            >
              INVORAX
            </span>
            <p className="text-sm mt-1" style={{ color: '#9CA3AF' }}>
              Minimalista. Rápido. Confiable. Diseñado para el control.
            </p>
          </div>

          <div className="flex flex-col items-center md:items-end text-center md:text-right">
            <p className="text-sm text-white">
              © {currentYear} INVORAX
            </p>
            <p className="text-xs" style={{ color: '#9CA3AF' }}>
              Todos los derechos reservados.
            </p>
          </div>
        </div>
      </div>
    </footer>
  )
}
