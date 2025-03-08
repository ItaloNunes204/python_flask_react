import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Sensores = () => {
    const [prototypesData, setPrototypesData] = useState(null);
    const [sensorData, setSensorData] = useState([]);
    const [editingSensor, setEditingSensor] = useState(null);
    const [deletingSensor, setDeletingSensor] = useState(null);
    const [newSensor, setNewSensor] = useState({ nome: '', informacao: '', id_prototipo: '' });

    useEffect(() => {
        axios.get('/api/sensors')
            .then(response => setPrototypesData(response.data))
            .catch(error => console.error("Erro ao buscar dados dos protótipos:", error));
    }, []);

    const handleClick = async (id) => {
        try {
            const response = await axios.post('/api/sensors/prototypes', { id });
            setSensorData(response.data);
        } catch (error) {
            console.error("Erro ao buscar dados do sensor:", error);
        }
    };

    const handleEdit = (sensor) => {
        setEditingSensor(sensor);
    };

    const handleDelete = (sensor) => {
        setDeletingSensor(sensor);
    };

    const handleEditSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('/api/modify_sensors', editingSensor);
            setSensorData(sensorData.map(sensor =>
                sensor.id_sensor === editingSensor.id_sensor ? editingSensor : sensor
            ));
            setEditingSensor(null);
        } catch (error) {
            console.error("Erro ao atualizar sensor:", error);
        }
    };

    const handleDeleteSubmit = async () => {
        try {
            await axios.post('/api/delete_sensors', { id_sensor: deletingSensor.id_sensor });
            setSensorData(sensorData.filter(sensor => sensor.id_sensor !== deletingSensor.id_sensor));
            setDeletingSensor(null);
        } catch (error) {
            console.error("Erro ao deletar sensor:", error);
        }
    };

    const handleNewSensorSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('/api/create_sensors', newSensor);
            setSensorData([...sensorData, response.data]);
            setNewSensor({ nome: '', informacao: '', id_prototipo: '' });
        } catch (error) {
            console.error("Erro ao cadastrar sensor:", error);
        }
    };

    return (
        <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
            <h1>Gerenciamento de Sensores</h1>

            {/* Botões para cada protótipo */}
            {prototypesData?.prototypes.map((prototype) => (
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
            {sensorData.length > 0 && (
                <div>
                    <h2>Dados do Sensor</h2>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '15px' }}>
                        {sensorData.map((sensor) => (
                            <div
                                key={sensor.id_sensor}
                                style={{
                                    border: '1px solid #ddd',
                                    borderRadius: '8px',
                                    padding: '15px',
                                    width: '250px',
                                    boxShadow: '2px 2px 10px rgba(0, 0, 0, 0.1)',
                                    backgroundColor: '#f9f9f9'
                                }}
                            >
                                <h3 style={{ margin: '5px 0' }}>{sensor.nome}</h3>
                                <p><strong>ID Sensor:</strong> {sensor.id_sensor}</p>
                                <p><strong>Informação:</strong> {sensor.informacao}</p>

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
                                        onClick={() => handleEdit(sensor)}
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
                                        onClick={() => handleDelete(sensor)}
                                    >
                                        Apagar
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Formulário para editar sensor */}
            {editingSensor && (
                <div style={{ marginTop: '20px' }}>
                    <h2>Editar Sensor</h2>
                    <form onSubmit={handleEditSubmit}>
                        <label>
                            Nome:
                            <input
                                type="text"
                                value={editingSensor.nome}
                                onChange={(e) => setEditingSensor({ ...editingSensor, nome: e.target.value })}
                            />
                        </label>
                        <label>
                            Informação:
                            <input
                                type="text"
                                value={editingSensor.informacao}
                                onChange={(e) => setEditingSensor({ ...editingSensor, informacao: e.target.value })}
                            />
                        </label>
                        <button type="submit">Confirmar</button>
                        <button type="button" onClick={() => setEditingSensor(null)}>Fechar</button>
                    </form>
                </div>
            )}

            {/* Formulário para deletar sensor */}
            {deletingSensor && (
                <div style={{ marginTop: '20px' }}>
                    <h2>Deletar Sensor</h2>
                    <p>Você tem certeza que deseja deletar o sensor <strong>{deletingSensor.nome}</strong>?</p>
                    <button onClick={handleDeleteSubmit}>Confirmar</button>
                    <button onClick={() => setDeletingSensor(null)}>Fechar</button>
                </div>
            )}

            {/* Formulário para cadastrar novo sensor */}
            <div style={{ marginTop: '20px' }}>
                <h2>Cadastrar Novo Sensor</h2>
                <form onSubmit={handleNewSensorSubmit}>
                    <label>
                        Nome:
                        <input
                            type="text"
                            value={newSensor.nome}
                            onChange={(e) => setNewSensor({ ...newSensor, nome: e.target.value })}
                        />
                    </label>
                    <label>
                        Informação:
                        <input
                            type="text"
                            value={newSensor.informacao}
                            onChange={(e) => setNewSensor({ ...newSensor, informacao: e.target.value })}
                        />
                    </label>

                    {/* Select para escolher o protótipo */}
                    <label>
                        Protótipo:
                        <select
                            value={newSensor.id_prototipo}
                            onChange={(e) => setNewSensor({ ...newSensor, id_prototipo: e.target.value })}
                        >
                            <option value="">Selecione um Protótipo</option>
                            {prototypesData?.prototypes.map((prototype) => (
                                <option key={prototype.id} value={prototype.id}>
                                    {prototype.nome}
                                </option>
                            ))}
                        </select>
                    </label>

                    <button type="submit">Cadastrar</button>
                </form>
            </div>
        </div>
    );
};

export default Sensores;
