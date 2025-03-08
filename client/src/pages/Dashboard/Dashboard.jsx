import { useEffect, useState } from 'react';
import { useOutletContext } from 'react-router-dom';
import axios from 'axios';

const Dashboard = () => {
    const { userData } = useOutletContext(); // Dados do usuário vindos do ProtectedRoute
    const [dashboardData, setDashboardData] = useState(null);
    const [loading, setLoading] = useState(true); // Definição do estado 'loading'

    // Busca os dados do dashboard sem necessidade de redirecionamento
    useEffect(() => {
        axios.get('/api/inicio_data')
        .then(res => setDashboardData(res.data))
        .catch(err => console.error('Erro ao buscar dados:', err))
        .finally(() => setLoading(false));
    }, []);

    if (loading) return <div>Carregando...</div>;

    return (
        <div>
        <h1>Bem-vindo, {userData.email}</h1>
        {dashboardData && (
            <div>
            <p>Nome: {dashboardData.nome}</p>
            <p>Último login: {dashboardData.ultimo_login}</p>
            <p>Tarefas concluídas: {dashboardData.tarefas_concluidas}</p>
            <p>{dashboardData.mensagem}</p>
            </div>
        )}
        </div>
    );
};

export default Dashboard;
