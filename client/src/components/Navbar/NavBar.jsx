// src/components/Navbar.jsx
import { Link, useNavigate } from 'react-router-dom'

const Navbar = ({ handleLogout }) => {
    const navigate = useNavigate()

    return (
        <nav style={{ 
        background: '#f0f0f0',
        padding: '1rem',
        display: 'flex',
        gap: '1rem',
        alignItems: 'center'
        }}>
        {/* Links para páginas protegidas */}
        <Link to="/inicio">Início</Link>
        <Link to="/membros">Membros</Link>
        <Link to="/prototipo">Prototipos</Link>
        <Link to="/sensores">Sensores</Link>
        <Link to="/metodologia">Metodologia</Link>
        <Link to="/pilotos">Pilotos</Link>
        <Link to="/circuito">Circuito</Link>
        <Link to="/teste">Teste</Link>
        <Link to="/TRPM">TRPM</Link>
        <Link to="/anexos">Anexos</Link>
        <Link to="/logger">Log</Link>
        {/* Botão de Logout */}
        <button 
            onClick={handleLogout}
            style={{ marginLeft: 'auto' }}
        >
            Sair
        </button>
        </nav>
    )
}

export default Navbar