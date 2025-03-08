import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PrototypesManagement = () => {
    const [prototypesData, setPrototypesData] = useState(null);
    const [isEditing, setIsEditing] = useState(false);
    const [isDeleting, setIsDeleting] = useState(false);
    const [selectedPrototype, setSelectedPrototype] = useState(null);
    const [prototypeToDelete, setPrototypeToDelete] = useState(null);
    const [newPrototype, setNewPrototype] = useState({
        id: '', nome: '', ano_fabricacao: '', status: '', peso: '', temporada: '', n_teste: '',
    });

    useEffect(() => {
        axios.get('/api/prototypes')
            .then(response => setPrototypesData(response.data))
            .catch(error => console.error("Erro ao buscar dados dos protótipos:", error));
    }, []);

    const handleEdit = (prototype) => {
        setSelectedPrototype(prototype);
        setIsEditing(true);
    };

    const handleDelete = (prototype) => {
        setPrototypeToDelete(prototype);
        setIsDeleting(true);
    };

    const confirmDelete = () => {
        axios.post('/api/delete_prototypes', { id: prototypeToDelete.id })
            .then(() => {
                setPrototypesData((prevData) => ({
                    ...prevData,
                    prototypes: prevData.prototypes.filter((p) => p.id !== prototypeToDelete.id),
                }));
                setIsDeleting(false);
                setPrototypeToDelete(null);
            })
            .catch(error => console.error("Erro ao deletar protótipo:", error));
    };

    const handleSaveEdit = () => {
        axios.post('/api/modify_prototypes', selectedPrototype)
            .then(() => {
                setPrototypesData((prevData) => ({
                    ...prevData,
                    prototypes: prevData.prototypes.map((p) =>
                        p.id === selectedPrototype.id ? selectedPrototype : p
                    ),
                }));
                setIsEditing(false);
                setSelectedPrototype(null);
            })
            .catch(error => console.error("Erro ao modificar protótipo:", error));
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setSelectedPrototype((prevPrototype) => ({
            ...prevPrototype,
            [name]: value,
        }));
    };

    const handleNewPrototypeChange = (e) => {
        const { name, value } = e.target;
        setNewPrototype((prevPrototype) => ({
            ...prevPrototype,
            [name]: value,
        }));
    };

    const handleAddPrototype = () => {
        axios.post('/api/create_prototypes', newPrototype)
            .then(response => {
                setPrototypesData((prevData) => ({
                    ...prevData,
                    prototypes: prevData?.prototypes 
                        ? [...prevData.prototypes, response.data] 
                        : [response.data], // Caso seja a primeira entrada
                }));
                setNewPrototype({ id: '', nome: '', ano_fabricacao: '', status: '', peso: '', temporada: '', n_teste: '' });
            })
            .catch(error => console.error("Erro ao adicionar protótipo:", error));
    };

    return (
        <div>
            <h1>Gerenciamento de Protótipos</h1>
            {prototypesData?.prototypes && (
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nome</th>
                            <th>Ano</th>
                            <th>Status</th>
                            <th>Peso</th>
                            <th>Temporada</th>
                            <th>Nº Teste</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {prototypesData.prototypes.map((prototype) => (
                            <tr key={prototype.id}>
                                <td>{prototype.id}</td>
                                <td>{prototype.nome}</td>
                                <td>{prototype.ano_fabricacao}</td>
                                <td>{prototype.status}</td>
                                <td>{prototype.peso}</td>
                                <td>{prototype.temporada}</td>
                                <td>{prototype.n_teste}</td>
                                <td>
                                    <button onClick={() => handleEdit(prototype)}>Editar</button>
                                    <button onClick={() => handleDelete(prototype)}>Excluir</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}

            {isEditing && selectedPrototype && (
                <div>
                    <h2>Editar Protótipo</h2>
                    <input name="nome" value={selectedPrototype.nome} onChange={handleChange} />
                    <input name="Ano" value={selectedPrototype.ano_fabricacao} onChange={handleChange} />
                    <input name="Status" value={selectedPrototype.status} onChange={handleChange} />
                    <input name="Peso" value={selectedPrototype.peso} onChange={handleChange} />
                    <input name="Temporada" value={selectedPrototype.temporada} onChange={handleChange} />

                    <button onClick={handleSaveEdit}>Salvar</button>
                    <button onClick={() => setIsEditing(false)}>Cancelar</button>
                </div>
            )}

            {isDeleting && prototypeToDelete && (
                <div>
                    <p>Tem certeza que deseja excluir {prototypeToDelete.nome}?</p>
                    <button onClick={confirmDelete}>Confirmar</button>
                    <button onClick={() => setIsDeleting(false)}>Cancelar</button>
                </div>
            )}

            <h2>Adicionar Novo Protótipo</h2>
            <input name="nome" value={newPrototype.nome} onChange={handleNewPrototypeChange} placeholder="Nome" />
            <input name="ano_fabricacao" value={newPrototype.ano_fabricacao} onChange={handleNewPrototypeChange} placeholder="Ano de Fabricação" />
            <input name="status" value={newPrototype.status} onChange={handleNewPrototypeChange} placeholder="Status" />
            <input name="peso" value={newPrototype.peso} onChange={handleNewPrototypeChange} placeholder="Peso" />
            <input name="temporada" value={newPrototype.temporada} onChange={handleNewPrototypeChange} placeholder="Temporada" />
            <input name="n_teste" value={newPrototype.n_teste} onChange={handleNewPrototypeChange} placeholder="Nº Teste" />
            <button onClick={handleAddPrototype}>Adicionar</button>
        </div>
    );
};

export default PrototypesManagement;
