import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Teste = () => {
    const [metodologiasData, setMetodologiasData] = useState(null);
    const [metodologiaData, setMetodologiaData] = useState([]);
    const [prototipoSelecionado, setPrototipoSelecionado] = useState(null);
    const [mostrarDados, setMostrarDados] = useState(false);
    const [opcoesTeste, setOpcoesTeste] = useState([]);
    const [testeSelecionado, setTesteSelecionado] = useState(['']);
    const [opcoesPiloto, setOpcoesPiloto] = useState([]);
    const [pilotoSelecionado, setPilotoSelecionado] = useState(['']); // Para armazenar os pilotos selecionados
    const [opcoesCircuito, setOpcoesCircuito] = useState([]); // Novo estado para os circuitos
    const [circuitoSelecionado, setCircuitoSelecionado] = useState(''); // Para armazenar o circuito selecionado
    const [imagemCircuito, setImagemCircuito] = useState(''); // Para armazenar a imagem correspondente
    const [horaInicio, setHoraInicio] = useState('');
    const [horaFim, setHoraFim] = useState('');
    const [almoco, setAlmoco] = useState(false);
    const [dataTeste, setDataTeste] = useState('');
    const [nome, setnome] = useState('');
    const [cardConfirmacao, setCardConfirmacao] = useState({mostrar: false,idTeste: null,});
    const [mostrarFormularioEdicao, setMostrarFormularioEdicao] = useState(false);

    useEffect(() => {
        axios.get('/api/test')
            .then(response => setMetodologiasData(response.data))
            .catch(error => console.error("Erro ao buscar dados das metodologias:", error));
    }, []);

    const handleClick = async (id) => {
        try {
            const response = await axios.post('/api/test/prototypes', { id });
            setMetodologiaData(response.data.teste);
            const prototipo = metodologiasData.prototypes.find(p => p.id === id);
            setPrototipoSelecionado(prototipo);
        } catch (error) {
            console.error("Erro ao buscar dados da metodologia:", error);
        }
    };

    const handleCadastroTeste = async () => {
        if (!prototipoSelecionado) {
            console.error("Nenhum protótipo selecionado.");
            return;
        }

        try {
            const response = await axios.post('/api/teste/get_objetivos', {id: prototipoSelecionado.id }, {
                headers: { 'Content-Type': 'application/json' }
            });
            setOpcoesTeste(response.data.objetivos);
            setOpcoesPiloto(response.data.piloto);
            setOpcoesCircuito(response.data.circuito);
            setMostrarDados(true);
        } catch (error) {
            console.error("Erro ao buscar opções de teste:", error);
        }
    };

    const handleChangeTeste = (event, index) => {
        const newTesteSelecionado = [...testeSelecionado];
        newTesteSelecionado[index] = event.target.value;
        setTesteSelecionado(newTesteSelecionado);
    };

    const handleChangePiloto = (event, index) => {
        const newPilotoSelecionado = [...pilotoSelecionado];
        newPilotoSelecionado[index] = event.target.value;
        setPilotoSelecionado(newPilotoSelecionado);
    };

    const handleChangeCircuito = (event) => {
        setCircuitoSelecionado(event.target.value);
        // Exibe a imagem correspondente ao circuito selecionado
        const circuito = opcoesCircuito.find(circuito => circuito.id === event.target.value);
        if (circuito) {
            setImagemCircuito(circuito.imagem); // Supondo que a resposta tenha uma propriedade 'imagem'
        }
    };

    const handleAddSelect = () => {
        setTesteSelecionado([...testeSelecionado, ""]);
    };

    const handleRemoveSelect = (index) => {
        if (testeSelecionado.length > 1) {
            const newTesteSelecionado = testeSelecionado.filter((_, i) => i !== index);
            setTesteSelecionado(newTesteSelecionado);
        }
    };

    const handleAddPilotoSelect = () => {
        setPilotoSelecionado(prev => [...prev, ""]);
    };

    const handleRemovePilotoSelect = (index) => {
        if (pilotoSelecionado.length > 1) {
            const newPilotoSelecionado = pilotoSelecionado.filter((_, i) => i !== index);
            setPilotoSelecionado(newPilotoSelecionado);
        }
    };

    const handleAddCircuitoSelect = () => {
        setCircuitoSelecionado('');
        setImagemCircuito('');
    };

    // Função para abrir o PDF em uma nova aba
    const openPDF = (pdfUrl) => {
        window.open(pdfUrl, '_blank');
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        // Montar os dados a serem enviados
        const data = {
            nome: nome,
            prototipo: prototipoSelecionado.id,
            objetivos: testeSelecionado,
            pilotos: pilotoSelecionado,
            circuito: circuitoSelecionado,
            horaInicio: horaInicio,
            horaFim: horaFim,
            almoco: almoco,
            dataTeste: dataTeste,
        };

        try {
            const response = await axios.post('/api/create_test', data, {
                headers: { 'Content-Type': 'application/json' }
            });
            console.log('Teste cadastrado com sucesso:', response.data);
            // Aqui você pode tratar a resposta, como redirecionar o usuário ou exibir uma mensagem de sucesso
        } catch (error) {
            console.error('Erro ao enviar os dados do teste:', error);
        }
    };

    const lidarComApagar = (idTeste) => {
        setCardConfirmacao({ mostrar: true, idTeste });
    };

    const confirmarApagar = async () => {
        try {
            await axios.post('/api/delete_test', { id: cardConfirmacao.idTeste });
            console.log('Teste apagado com sucesso');
            // Aqui você pode atualizar a lista de testes ou fazer outras ações necessárias
        } catch (error) {
            console.error('Erro ao apagar o teste:', error);
        } finally {
            setCardConfirmacao({ mostrar: false, idTeste: null });
        }
    };

    const cancelarApagar = () => {
        setCardConfirmacao({ mostrar: false, idTeste: null });
    };

    const CardConfirmacao = ({ mostrar, onConfirmar, onCancelar }) => {
        if (!mostrar) return null;

        return (
            <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0, 0, 0, 0.5)', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '5px' }}>
                    <p>Tem certeza que deseja apagar este teste?</p>
                    <button onClick={onConfirmar} style={{ backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '5px', padding: '10px', margin: '5px', cursor: 'pointer' }}>Confirmar</button>
                    <button onClick={onCancelar} style={{ backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '5px', padding: '10px', margin: '5px', cursor: 'pointer' }}>Cancelar</button>
                </div>
            </div>
        );
    }

    const handleEditarTeste = async (teste) => {
        setMostrarFormularioEdicao(true); // Exibir o formulário de edição
    };

    return (
        <div style={{ padding: '20px' }}>
            <h1>Teste</h1>
            
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

            {/* Botão Cadastrar Teste */}
            <button
                style={{
                    margin: '10px 0',
                    padding: '10px',
                    backgroundColor: '#00FF00',
                    color: 'white',
                    border: 'none',
                    borderRadius: '5px',
                    cursor: 'pointer'
                }}
                onClick={handleCadastroTeste}
            >
                Cadastrar Teste
            </button>

            {mostrarDados && prototipoSelecionado && (
                <form onSubmit={handleSubmit} style={{ marginTop: '20px', padding: '10px', border: '1px solid #ddd', borderRadius: '5px' }}>
                    <h2>Informações do Protótipo</h2>
                    <p><strong>ID:</strong> {prototipoSelecionado.id}</p>
                    <p><strong>Nome:</strong> {prototipoSelecionado.nome}</p>
                    <label>Selecione um teste:</label>
                    
                    {/* Renderizando múltiplos selects para Testes */}
                    {Array.isArray(testeSelecionado) && testeSelecionado.map((selectValue, index) => (
                        <div key={index} style={{ marginBottom: '10px' }}>
                            <select style={{ marginLeft: '10px' }} value={selectValue} onChange={(e) => handleChangeTeste(e, index)}>
                                <option value="">Selecionar</option>
                                {Array.isArray(opcoesTeste) && opcoesTeste.map((teste, index) => (
                                    <option key={index} value={teste.id_metodologia}>{teste.objetivo}</option>
                                ))}
                            </select>
                            {/* Botão para remover o select */}
                            <button
                                type="button"
                                style={{
                                    marginLeft: '10px',
                                    padding: '5px 10px',
                                    backgroundColor: '#dc3545',
                                    color: 'white',
                                    border: 'none',
                                    borderRadius: '5px',
                                    cursor: 'pointer'
                                }}
                                onClick={() => handleRemoveSelect(index)}
                            >
                                Apagar
                            </button>
                        </div>
                    ))}

                    {/* Botão para adicionar um novo select de Teste */}
                    <button
                        type="button"
                        style={{
                            margin: '10px 0',
                            padding: '10px',
                            backgroundColor: '#007bff',
                            color: 'white',
                            border: 'none',
                            borderRadius: '5px',
                            cursor: 'pointer'
                        }}
                        onClick={handleAddSelect}
                    >
                        Adicionar Select de Teste
                    </button>

                    <label>Selecione um Piloto:</label>
                    
                    {/* Renderizando múltiplos selects para Pilotos */}
                    {Array.isArray(pilotoSelecionado) && pilotoSelecionado.map((selectValue, index) => (
                        <div key={index} style={{ marginBottom: '10px' }}>
                            <select style={{ marginLeft: '10px' }} value={selectValue} onChange={(e) => handleChangePiloto(e, index)}>
                                <option value="">Selecionar</option>
                                {Array.isArray(opcoesPiloto) && opcoesPiloto.map((piloto, index) => (
                                    <option key={index} value={piloto.id}>{piloto.nome}</option>
                                ))}
                            </select>
                            {/* Botão para remover o select */}
                            <button
                                type="button"
                                style={{
                                    marginLeft: '10px',
                                    padding: '5px 10px',
                                    backgroundColor: '#dc3545',
                                    color: 'white',
                                    border: 'none',
                                    borderRadius: '5px',
                                    cursor: 'pointer'
                                }}
                                onClick={() => handleRemovePilotoSelect(index)}
                            >
                                Apagar
                            </button>
                        </div>
                    ))}

                    {/* Botão para adicionar um novo select de Piloto */}
                    <button
                        type="button"
                        style={{
                            margin: '10px 0',
                            padding: '10px',
                            backgroundColor: '#007bff',
                            color: 'white',
                            border: 'none',
                            borderRadius: '5px',
                            cursor: 'pointer'
                        }}
                        onClick={handleAddPilotoSelect}
                    >
                        Adicionar Select de Piloto
                    </button>

                    <label>Selecione o Circuito:</label>
                    <select value={circuitoSelecionado} onChange={handleChangeCircuito} style={{ marginLeft: '10px' }}>
                        <option value="">Selecionar</option>
                        {Array.isArray(opcoesCircuito) && opcoesCircuito.map((circuito, index) => (
                            <option key={index} value={circuito.id_circuito}>{circuito.nome}</option>
                        ))}
                    </select>

                    {imagemCircuito && (
                        <div style={{ marginTop: '10px' }}>
                            <img src={imagemCircuito} alt="Imagem do Circuito" style={{ maxWidth: '100%', height: 'auto' }} />
                        </div>
                    )}

                    <div>
                        <label>Nome</label>
                        <input type="text" value={nome} onChange={(e) => setnome(e.target.value)}/>
                    </div>
                    {/* Campos de Hora e Data */}
                    <div>
                        <label>Hora de Início:</label>
                        <input type="time" value={horaInicio} onChange={(e) => setHoraInicio(e.target.value)} />
                    </div>

                    <div>
                        <label>Hora de Fim:</label>
                        <input type="time" value={horaFim} onChange={(e) => setHoraFim(e.target.value)} />
                    </div>

                    <div>
                        <label>Almoço:</label>
                        <input type="checkbox" checked={almoco} onChange={() => setAlmoco(!almoco)} />
                    </div>

                    <div>
                        <label>Data do Teste:</label>
                        <input type="date" value={dataTeste} onChange={(e) => setDataTeste(e.target.value)} />
                    </div>

                    {/* Botão para enviar os dados */}
                    <button
                        style={{
                            marginTop: '20px',
                            padding: '10px',
                            backgroundColor: '#28a745',
                            color: 'white',
                            border: 'none',
                            borderRadius: '5px',
                            cursor: 'pointer'
                        }}
                    >
                        Enviar Dados
                    </button>
                </form>
            )}

            {metodologiaData.length > 0 && (
                <div style={{ marginTop: '20px' }}>
                    {metodologiaData.map((data, index) => (
                        <div key={index}>
                            <table style={{ width: '100%', borderCollapse: 'collapse', marginBottom: '20px' }}>
                                <thead>
                                    <tr style={{ backgroundColor: '#f2f2f2', textAlign: 'left' }}>
                                        <th style={{ padding: '10px', border: '1px solid #ddd' }}>Informação</th>
                                        <th style={{ padding: '10px', border: '1px solid #ddd' }}>Valor</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td style={{ padding: '10px', border: '1px solid #ddd', fontWeight: 'bold' }}>ID</td>
                                        <td style={{ padding: '10px', border: '1px solid #ddd' }}>{data.id}</td>
                                    </tr>
                                    <tr>
                                        <td style={{ padding: '10px', border: '1px solid #ddd', fontWeight: 'bold' }}>Nome</td>
                                        <td style={{ padding: '10px', border: '1px solid #ddd' }}>{data.nome}</td>
                                    </tr>
                                    <tr>
                                        <td style={{ padding: '10px', border: '1px solid #ddd', fontWeight: 'bold' }}>Pilotos</td>
                                        <td style={{ padding: '10px', border: '1px solid #ddd' }}>{data.pilotos}</td>
                                    </tr>
                                    <tr>
                                        <td style={{ padding: '10px', border: '1px solid #ddd', fontWeight: 'bold' }}>Objetivos</td>
                                        <td style={{ padding: '10px', border: '1px solid #ddd' }}>{data.id_objetivos}</td>
                                    </tr>
                                    <tr>
                                        <td style={{ padding: '10px', border: '1px solid #ddd', fontWeight: 'bold' }}>Número de Voltas</td>
                                        <td style={{ padding: '10px', border: '1px solid #ddd' }}>{data.N_voltas}</td>
                                    </tr>
                                    <tr>
                                        <td style={{ padding: '10px', border: '1px solid #ddd', fontWeight: 'bold' }}>Início</td>
                                        <td style={{ padding: '10px', border: '1px solid #ddd' }}>{data.inicio}</td>
                                    </tr>
                                    <tr>
                                        <td style={{ padding: '10px', border: '1px solid #ddd', fontWeight: 'bold' }}>Fim</td>
                                        <td style={{ padding: '10px', border: '1px solid #ddd' }}>{data.fim}</td>
                                    </tr>
                                    <tr>
                                        <td style={{ padding: '10px', border: '1px solid #ddd', fontWeight: 'bold' }}>Almoço</td>
                                        <td style={{ padding: '10px', border: '1px solid #ddd' }}>{data.almoco}</td>
                                    </tr>
                                    <tr>
                                        <td style={{ padding: '10px', border: '1px solid #ddd', fontWeight: 'bold' }}>Data</td>
                                        <td style={{ padding: '10px', border: '1px solid #ddd' }}>{data.data}</td>
                                    </tr>
                                    <tr>
                                        <td style={{ padding: '10px', border: '1px solid #ddd', fontWeight: 'bold' }}>Protótipo</td>
                                        <td style={{ padding: '10px', border: '1px solid #ddd' }}>{data.id_prototipo}</td>
                                    </tr>
                                    <tr>
                                        <td style={{ padding: '10px', border: '1px solid #ddd', fontWeight: 'bold' }}>Circuito</td>
                                        <td style={{ padding: '10px', border: '1px solid #ddd' }}>{data.id_circuito}</td>
                                    </tr>
                                    <tr>
                                        <td style={{ padding: '10px', border: '1px solid #ddd', fontWeight: 'bold' }}>Status</td>
                                        <td style={{ padding: '10px', border: '1px solid #ddd' }}>{data.status}</td>
                                    </tr>
                                    <tr>
                                        <td style={{ padding: '10px', border: '1px solid #ddd', fontWeight: 'bold' }}>Observação</td>
                                        <td style={{ padding: '10px', border: '1px solid #ddd' }}>{data.observacao}</td>
                                    </tr>
                                    {/* Verificação de briefing */}
                                    <tr>
                                        <td style={{ padding: '10px', border: '1px solid #ddd', fontWeight: 'bold' }}>Briefing</td>
                                        <td style={{ padding: '10px', border: '1px solid #ddd' }}>
                                            {data.briefing ? (
                                                <button 
                                                    onClick={() => openPDF(data.URL_briefing)} 
                                                    style={{
                                                        margin: '5px', 
                                                        padding: '10px', 
                                                        backgroundColor: '#28a745', 
                                                        color: 'white', 
                                                        border: 'none', 
                                                        borderRadius: '5px', 
                                                        cursor: 'pointer'
                                                    }}
                                                >
                                                    Ver Documento
                                                </button>
                                            ) : (
                                                <span>O teste deve ocorrer para que o documento seja gerado</span>
                                            )}
                                        </td>
                                    </tr>
                                    {/* Verificação de debriefing */}
                                    <tr>
                                        <td style={{ padding: '10px', border: '1px solid #ddd', fontWeight: 'bold' }}>Debriefing</td>
                                        <td style={{ padding: '10px', border: '1px solid #ddd' }}>
                                            {data.debriefing ? (
                                                <button 
                                                    onClick={() => openPDF(data.URL_debriefing)} 
                                                    style={{
                                                        margin: '5px', 
                                                        padding: '10px', 
                                                        backgroundColor: '#28a745', 
                                                        color: 'white', 
                                                        border: 'none', 
                                                        borderRadius: '5px', 
                                                        cursor: 'pointer'
                                                    }}
                                                >
                                                    Ver Documento
                                                </button>
                                            ) : (
                                                <span>O teste deve ocorrer para que o documento seja gerado</span>
                                            )}
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <div>
                                <button
                                    onClick={() => handleEditarTeste(data)}
                                    style={{ margin: '5px', padding: '10px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>
                                    Editar
                                </button>

                                <button
                                    onClick={() => lidarComApagar(data.id)}
                                    style={{ margin: '5px', padding: '10px', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>
                                    Apagar
                                </button>
                            </div>
                            <CardConfirmacao
                                mostrar={cardConfirmacao.mostrar}
                                onConfirmar={confirmarApagar}
                                onCancelar={cancelarApagar}
                            />
                        </div>
                    ))}
                </div>
            )}

            {mostrarFormularioEdicao && (
                <form onSubmit={handleSubmit} style={{ marginTop: '20px', padding: '10px', border: '1px solid #ddd', borderRadius: '5px' }}>
                    <h2>Editar Teste</h2>
                    {/* Campos do formulário de edição */}
                    <label>Nome</label>
                    <input type="text" value={nome} onChange={(e) => setnome(e.target.value)} />

                    <label>Selecione um teste:</label>
                    {/* Renderizando múltiplos selects para Testes */}
                    {Array.isArray(testeSelecionado) && testeSelecionado.map((selectValue, index) => (
                        <div key={index} style={{ marginBottom: '10px' }}>
                            <select style={{ marginLeft: '10px' }} value={selectValue} onChange={(e) => handleChangeTeste(e, index)}>
                                <option value="">Selecionar</option>
                                {Array.isArray(opcoesTeste) && opcoesTeste.map((teste, index) => (
                                    <option key={index} value={teste.id_metodologia}>{teste.objetivo}</option>
                                ))}
                            </select>
                        </div>
                    ))}
                    {/* Botão para adicionar um novo select de Teste */}
                    <button type="button" onClick={handleAddSelect}>Adicionar Select de Teste</button>

                    <label>Selecione um Piloto:</label>
                    {/* Renderizando múltiplos selects para Pilotos */}
                    {Array.isArray(pilotoSelecionado) && pilotoSelecionado.map((selectValue, index) => (
                        <div key={index} style={{ marginBottom: '10px' }}>
                            <select style={{ marginLeft: '10px' }} value={selectValue} onChange={(e) => handleChangePiloto(e, index)}>
                                <option value="">Selecionar</option>
                                {Array.isArray(opcoesPiloto) && opcoesPiloto.map((piloto, index) => (
                                    <option key={index} value={piloto.id}>{piloto.nome}</option>
                                ))}
                            </select>
                        </div>
                    ))}
                    {/* Botão para adicionar um novo select de Piloto */}
                    <button type="button" onClick={handleAddPilotoSelect}>Adicionar Select de Piloto</button>

                    <label>Selecione o Circuito:</label>
                    <select value={circuitoSelecionado} onChange={handleChangeCircuito} style={{ marginLeft: '10px' }}>
                        <option value="">Selecionar</option>
                        {Array.isArray(opcoesCircuito) && opcoesCircuito.map((circuito, index) => (
                            <option key={index} value={circuito.id_circuito}>{circuito.nome}</option>
                        ))}
                    </select>

                    {imagemCircuito && (
                        <div style={{ marginTop: '10px' }}>
                            <img src={imagemCircuito} alt="Imagem do Circuito" style={{ maxWidth: '100%', height: 'auto' }} />
                        </div>
                    )}

                    <div>
                        <label>Hora de Início:</label>
                        <input type="time" value={horaInicio} onChange={(e) => setHoraInicio(e.target.value)} />
                    </div>

                    <div>
                        <label>Hora de Fim:</label>
                        <input type="time" value={horaFim} onChange={(e) => setHoraFim(e.target.value)} />
                    </div>

                    <div>
                        <label>Almoço:</label>
                        <input type="checkbox" checked={almoco} onChange={() => setAlmoco(!almoco)} />
                    </div>

                    <div>
                        <label>Data do Teste:</label>
                        <input type="date" value={dataTeste} onChange={(e) => setDataTeste(e.target.value)} />
                    </div>

                    <button type="submit">Salvar Edição</button>
                </form>
            )}

        </div>
    );
};

export default Teste;
