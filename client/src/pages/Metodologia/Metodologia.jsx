import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Metodologia = () => {
    const [metodologiasData, setMetodologiasData] = useState(null);
    const [metodologiaData, setMetodologiaData] = useState([]);
    const [editingMetodologia, setEditingMetodologia] = useState(null);
    const [deletingMetodologia, setDeletingMetodologia] = useState(null);
    const [newMetodologia, setNewMetodologia] = useState({
        objetivo: '',
        N_pessoas: '',
        subgrupo: '',
        procedimento: '',
        N_voltas: '',
        temporada: '',
        status: ''
    });

    useEffect(() => {
        axios.get('/api/methodology')
            .then(response => setMetodologiasData(response.data))
            .catch(error => console.error("Erro ao buscar dados das metodologias:", error));
    }, []);

    const handleClick = async (id) => {
        try {
            const response = await axios.post('/api/methodology/prototypes', { id });
            setMetodologiaData(response.data);
        } catch (error) {
            console.error("Erro ao buscar dados da metodologia:", error);
        }
    };

    const handleEdit = (metodologia) => {
        setEditingMetodologia(metodologia);
    };

    const handleDelete = (metodologia) => {
        setDeletingMetodologia(metodologia);
    };

    const handleEditSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('/api/modify_methodology', editingMetodologia);
            setMetodologiaData(metodologiaData.map(metodologia =>
                metodologia.id_metodologia === editingMetodologia.id_metodologia ? editingMetodologia : metodologia
            ));
            setEditingMetodologia(null);
        } catch (error) {
            console.error("Erro ao atualizar metodologia:", error);
        }
    };

    const handleDeleteSubmit = async () => {
        try {
            await axios.post('/api/delete_methodology', { id_metodologia: deletingMetodologia.id_metodologia });
            setMetodologiaData(metodologiaData.filter(metodologia => metodologia.id_metodologia !== deletingMetodologia.id_metodologia));
            setDeletingMetodologia(null);
        } catch (error) {
            console.error("Erro ao deletar metodologia:", error);
        }
    };

    const handleNewMetodologiaSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('/api/create_methodology', newMetodologia);
            setMetodologiaData([...metodologiaData, response.data]);
            setNewMetodologia({
                objetivo: '',
                N_pessoas: '',
                subgrupo: '',
                procedimento: '',
                N_voltas: '',
                temporada: '',
                status: ''
            });
        } catch (error) {
            console.error("Erro ao cadastrar metodologia:", error);
        }
    };

    return (
        <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
            <h1>Gerenciamento de Metodologias</h1>

            {/* Botões para cada metodologia */}
            {metodologiasData?.prototypes.map((prototype) => (
                <button
                    key={prototype.id}
                    onClick={() => handleClick(prototype.id)}
                    style={{
                        margin: '5px',
                        padding: '10px',
                        backgroundColor: '#007bff',
                        color: 'white',
                        border: 'none',
                        borderRadius: '5px',
                        cursor: 'pointer'
                    }}
                >
                    {prototype.nome}
                </button>
            ))}

            {/* Exibir os dados retornados em cards */}
            {metodologiaData.length > 0 && (
                <div>
                    <h2>Dados da Metodologia</h2>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '15px' }}>
                        {metodologiaData.map((metodologia) => (
                            <div
                                key={metodologia.id_metodologia}
                                style={{
                                    border: '1px solid #ddd',
                                    borderRadius: '8px',
                                    padding: '15px',
                                    width: '250px',
                                    boxShadow: '2px 2px 10px rgba(0, 0, 0, 0.1)',
                                    backgroundColor: '#f9f9f9'
                                }}
                            >
                                <h3 style={{ margin: '5px 0' }}>{metodologia.objetivo}</h3>
                                <p><strong>ID Metodologia:</strong> {metodologia.id_metodologia}</p>
                                <p><strong>Numero de pessoas necessarios:</strong> {metodologia.N_pessoas}</p>
                                <p><strong>Subgrupo:</strong> {metodologia.subgrupo}</p>
                                <p><strong>Procedimento:</strong> {metodologia.procedimento}</p>
                                <p><strong>Numero de voltas:</strong> {metodologia.N_voltas}</p>
                                <p><strong>temporada:</strong> {metodologia.temporada}</p>
                                <p><strong>Status:</strong> {metodologia.status}</p>

                                {/* Botões no final do card */}
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '10px' }}>
                                    <button
                                        style={{
                                            padding: '8px',
                                            backgroundColor: '#28a745',
                                            color: 'white',
                                            border: 'none',
                                            borderRadius: '5px',
                                            cursor: 'pointer'
                                        }}
                                        onClick={() => handleEdit(metodologia)}
                                    >
                                        Editar
                                    </button>

                                    <button
                                        style={{
                                            padding: '8px',
                                            backgroundColor: '#dc3545',
                                            color: 'white',
                                            border: 'none',
                                            borderRadius: '5px',
                                            cursor: 'pointer'
                                        }}
                                        onClick={() => handleDelete(metodologia)}
                                    >
                                        Apagar
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Formulário para editar metodologia */}
            {editingMetodologia && (
                <div style={{ marginTop: '20px' }}>
                    <h2>Editar Metodologia</h2>
                    <form onSubmit={handleEditSubmit}>
                        <label>
                            Objetivo:
                            <input
                                type="text"
                                value={editingMetodologia.objetivo}
                                onChange={(e) => setEditingMetodologia({ ...editingMetodologia, objetivo: e.target.value })}
                            />
                        </label>
                        <label>
                            Número de Pessoas:
                            <input
                                type="number"
                                value={editingMetodologia.N_pessoas}
                                onChange={(e) => setEditingMetodologia({ ...editingMetodologia, N_pessoas: e.target.value })}
                            />
                        </label>
                        <label>
                            Subgrupo:
                            <input
                                type="text"
                                value={editingMetodologia.subgrupo}
                                onChange={(e) => setEditingMetodologia({ ...editingMetodologia, subgrupo: e.target.value })}
                            />
                        </label>
                        <label>
                            Procedimento:
                            <input
                                type="text"
                                value={editingMetodologia.procedimento}
                                onChange={(e) => setEditingMetodologia({ ...editingMetodologia, procedimento: e.target.value })}
                            />
                        </label>
                        <label>
                            Número de Voltas:
                            <input
                                type="number"
                                value={editingMetodologia.N_voltas}
                                onChange={(e) => setEditingMetodologia({ ...editingMetodologia, N_voltas: e.target.value })}
                            />
                        </label>
                        <label>
                            Temporada:
                            <input
                                type="text"
                                value={editingMetodologia.temporada}
                                onChange={(e) => setEditingMetodologia({ ...editingMetodologia, temporada: e.target.value })}
                            />
                        </label>
                        <label>
                            Status:
                            <input
                                type="text"
                                value={editingMetodologia.status}
                                onChange={(e) => setEditingMetodologia({ ...editingMetodologia, status: e.target.value })}
                            />
                        </label>
                        <button type="submit">Confirmar</button>
                        <button type="button" onClick={() => setEditingMetodologia(null)}>Fechar</button>
                    </form>
                </div>
            )}

            {/* Formulário para deletar metodologia */}
            {deletingMetodologia && (
                <div style={{ marginTop: '20px' }}>
                    <h2>Deletar Metodologia</h2>
                    <p>Você tem certeza que deseja deletar a metodologia <strong>{deletingMetodologia.objetivo}</strong>?</p>
                    <button onClick={handleDeleteSubmit}>Confirmar</button>
                    <button onClick={() => setDeletingMetodologia(null)}>Fechar</button>
                </div>
            )}

            {/* Formulário para cadastrar nova metodologia */}
            <div style={{ marginTop: '20px' }}>
                <h2>Cadastrar Nova Metodologia</h2>
                <form onSubmit={handleNewMetodologiaSubmit}>
                    <label>
                        Objetivo:
                        <input
                            type="text"
                            value={newMetodologia.objetivo}
                            onChange={(e) => setNewMetodologia({ ...newMetodologia, objetivo: e.target.value })}
                        />
                    </label>
                    <label>
                        Número de Pessoas:
                        <input
                            type="number"
                            value={newMetodologia.N_pessoas}
                            onChange={(e) => setNewMetodologia({ ...newMetodologia, N_pessoas: e.target.value })}
                        />
                    </label>
                    <label>
                        Subgrupo:
                        <input
                            type="text"
                            value={newMetodologia.subgrupo}
                            onChange={(e) => setNewMetodologia({ ...newMetodologia, subgrupo: e.target.value })}
                        />
                    </label>
                    <label>
                        Procedimento:
                        <input
                            type="text"
                            value={newMetodologia.procedimento}
                            onChange={(e) => setNewMetodologia({ ...newMetodologia, procedimento: e.target.value })}
                        />
                    </label>
                    <label>
                        Número de Voltas:
                        <input
                            type="number"
                            value={newMetodologia.N_voltas}
                            onChange={(e) => setNewMetodologia({ ...newMetodologia, N_voltas: e.target.value })}
                        />
                    </label>
                    <label>
                        Temporada:
                        <input
                            type="text"
                            value={newMetodologia.temporada}
                            onChange={(e) => setNewMetodologia({ ...newMetodologia, temporada: e.target.value })}
                        />
                    </label>
                    <label>
                        Status:
                        <input
                            type="text"
                            value={newMetodologia.status}
                            onChange={(e) => setNewMetodologia({ ...newMetodologia, status: e.target.value })}
                        />
                    </label>
                    <button type="submit">Cadastrar</button>
                </form>
            </div>
        </div>
    );
};

export default Metodologia;
