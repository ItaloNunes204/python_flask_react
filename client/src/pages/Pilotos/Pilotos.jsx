import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Piloto = () => {
    // Estado para armazenar os protótipos, pilotos e o estado do formulário
    const [prototipos, setPrototipos] = useState([]);
    const [pilotos, setPilotos] = useState([]);
    const [formData, setFormData] = useState(null); // Armazena os dados do piloto a ser apagado
    const [showForm, setShowForm] = useState(false); // Controla a visibilidade do formulário de confirmação
    
    // Função para carregar os protótipos ao abrir a página
    useEffect(() => {
        axios.post('/api/pilots') // Requisição POST para obter os protótipos
        .then((response) => {
            setPrototipos(response.data.prototypes); // Armazena os protótipos retornados
        })
        .catch((error) => {
            console.error('Erro ao carregar protótipos:', error);
        });
    }, []);

    // Função para carregar os pilotos com base no protótipo selecionado
    const carregarPilotos = (prototipoId) => {
        axios.post('/api/pilots/prototype', { prototipoId }) // Requisição POST para obter os pilotos
        .then((response) => {
            setPilotos(response.data.pilotos); // Armazena os pilotos retornados
        })
        .catch((error) => {
            console.error('Erro ao carregar pilotos:', error);
        });
    };

    // Função para mostrar o formulário de confirmação de exclusão de piloto
    const mostrarFormulario = (piloto) => {
        setFormData(piloto); // Define os dados do piloto a ser apagado
        setShowForm(true); // Exibe o formulário
    };

    // Função para apagar o piloto
    const apagarPiloto = (idPiloto) => {
        console.log('Enviando requisição para apagar piloto com id:', idPiloto);
        axios.post('/api/delete_pilot', { id: idPiloto }) // Requisição POST para apagar o piloto
        .then((response) => {
            console.log('Resposta da requisição de exclusão:', response);
            setPilotos(pilotos.filter((piloto) => piloto.id_piloto !== idPiloto)); // Remove o piloto da lista
            setShowForm(false); // Esconde o formulário
            setFormData(null); // Limpa os dados do formulário
        })
        .catch((error) => {
            console.error('Erro ao apagar piloto:', error);
        });
    };

    return (
        <div>
        <h1>Piloto</h1>
        
        {/* Exibindo os botões para cada protótipo */}
        <div>
            {prototipos.map((prototipo) => (
            <button key={prototipo.id} onClick={() => carregarPilotos(prototipo.id)}>
                {prototipo.nome}
            </button>
            ))}
        </div>
        
        {/* Exibindo a tabela de pilotos */}
        <table>
            <thead>
            <tr>
                <th>ID Piloto</th>
                <th>Temporada</th>
                <th>Nº Testes</th>
                <th>Email</th>
                <th>Kms</th>
                <th>Nome</th>
                <th>Apagar</th>
            </tr>
            </thead>
            <tbody>
            {pilotos.map((piloto) => (
                <tr key={piloto.id}>
                <td>{piloto.id}</td>
                <td>{piloto.temporada}</td>
                <td>{piloto.n_testes}</td>
                <td>{piloto.email}</td>
                <td>{piloto.kms}</td>
                <td>{piloto.nome}</td>
                <td>
                    <button onClick={() => mostrarFormulario(piloto)}>Apagar</button>
                </td>
                </tr>
            ))}
            </tbody>
        </table>

        {/* Formulário de confirmação para apagar piloto */}
        {showForm && formData && (
            <div>
            <h2>Confirmar Exclusão</h2>
            <p>ID Piloto: {formData.id}</p>
            <p>Nome: {formData.nome}</p>
            <button onClick={() => apagarPiloto(formData.id)}>Confirmar</button>
            <button onClick={() => setShowForm(false)}>Cancelar</button>
            </div>
        )}
        </div>
    );
};

export default Piloto;
