// src/components/ProtectedRoute.jsx
import { useEffect, useState } from 'react';
import { Navigate, Outlet, useNavigate } from 'react-router-dom';
import axios from 'axios';
import Navbar from './Navbar/NavBar';

const ProtectedRoute = () => {
    const [userData, setUserData] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    // Função de logout (compartilhada com a Navbar)
    const handleLogout = async () => {
        try {
        await axios.post('/api/logout'); // Chama a API de logout
        navigate('/login'); // Redireciona para o login
        } catch (error) {
        console.error('Erro ao fazer logout:', error);
        }
    };

  // Verifica autenticação ao carregar
    useEffect(() => {
        axios.get('/api/check-auth')
        .then(res => {
            if (res.data.loggedIn) {
            setUserData(res.data); // Guarda os dados do usuário
            } else {
            setUserData(null);
            }
        })
        .catch(() => setUserData(null))
        .finally(() => setLoading(false));
    }, []);

    // Estado de carregamento
    if (loading) return <div>Carregando...</div>;

    // Se não autenticado, redireciona
    if (!userData) return <Navigate to="/login" replace />;

    // Se autenticado, mostra o layout com Navbar + Páginas
    return (
        <div>
        <Navbar handleLogout={handleLogout} />
        <Outlet context={{ userData }} /> {/* Renderiza as páginas aqui */}
        </div>
    );
};

export default ProtectedRoute;