import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

axios.defaults.withCredentials = true; // Adicione esta linha
const Login = () => {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const navigate = useNavigate()

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('/api/login', { email, password });
    
            if (response.data.success) {
                navigate('/inicio');
            } else {
                alert(response.data.error); // Exibir mensagem de erro do servidor
            }
        } catch (error) {
            if (error.response) {
                // O servidor respondeu com um status diferente de 2xx
                alert(error.response.data.message || 'Erro ao processar o login.');
            } else if (error.request) {
                // A requisição foi feita, mas não houve resposta
                alert('Sem resposta do servidor. Verifique sua conexão.');
            } else {
                // Erro na configuração da requisição
                alert('Erro desconhecido ao tentar logar.');
            }
        }
    };
    

    return (
        <div>
        <h1>Login</h1>
        <form onSubmit={handleSubmit}>
            <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            />
            <input
            type="password"
            placeholder="Senha"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            />
            <button type="submit">Entrar</button>
        </form>
        </div>
    )
}

export default Login