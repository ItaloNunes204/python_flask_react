import { useEffect, useState } from 'react';
import axios from 'axios';

const Members = () => {
    // Estado para armazenar os dados dos membros (inicialmente null)
    const [membersData, setMembersData] = useState(null);

    // Estado para indicar se os dados estão sendo carregados (true no início)
    const [loading, setLoading] = useState(true);

    // Estado para armazenar o membro atualmente selecionado
    const [selectedMember, setSelectedMember] = useState(null);

    // Estado para controlar se o usuário está editando um membro
    const [isEditing, setIsEditing] = useState(false);

    // Estado para controlar se um membro está sendo excluído
    const [isDeleting, setIsDeleting] = useState(false);

    // Estado para indicar se um membro está sendo promovido
    const [isPromoting, setIsPromoting] = useState(false);

    // Estado para armazenar os dados do membro que será promovido
    const [memberToPromote, setMemberToPromote] = useState(null);

    // Estado para controlar se um novo membro está sendo adicionado
    const [isAdding, setIsAdding] = useState(false);

    // Estado para armazenar os dados de um novo membro a ser cadastrado
    const [newMember, setNewMember] = useState({
    nome: '',       // Nome do novo membro
    email: '',      // E-mail do novo membro
    subgrupo: ''    // Subgrupo ao qual o novo membro pertence
    });

    // Estado para indicar se um membro está sendo modificado
    const [isModifying, setIsModifying] = useState(false);

    // Estado para armazenar os dados do membro que está sendo modificado
    const [modifyData, setModifyData] = useState({
    email: '',      // Novo e-mail do membro
    senha: '',      // Nova senha do membro
    nome: '',       // Novo nome do membro
    subgrupo: '',   // Novo subgrupo do membro
    senha_conf: ''  // Confirmação da nova senha
    });


    useEffect(() => {
        axios.get('/api/members')
        .then(res => setMembersData(res.data))
        .catch(err => console.error('Erro ao buscar dados:', err))
        .finally(() => setLoading(false));
    }, []);

    const handleEdit = (member) => {
        setSelectedMember(member);
        setIsEditing(true);
    };

    const handleDelete = (member) => {
        setMemberToDelete(member);
        setIsDeleting(true);
    };

    const handleConfirmDelete = () => {
        axios.post('/api/delete_members', memberToDelete)
            .then((res) => {
                if (res.data.success) {
                    setMembersData((prevData) => ({
                        ...prevData,
                        members: prevData.members.filter((member) => member.email !== memberToDelete.email),
                    }));
                    setIsDeleting(false);
                } else {
                    console.error('Erro ao deletar membro');
                }
            })
            .catch((err) => console.error('Erro ao salvar dados:', err));
    };

    const handleCancelDelete = () => {
        setIsDeleting(false);
    };

    const handleSave = () => {
        axios.post('/api/modify_members', selectedMember)
            .then((res) => {
                if (res.data.success) {
                    setMembersData((prevData) => ({
                        ...prevData,
                        members: prevData.members.map((member) =>
                            member.email === selectedMember.email ? selectedMember : member
                        ),
                    }));
                    setIsEditing(false);
                } else {
                    console.error('Erro ao atualizar membro');
                }
            })
            .catch((err) => console.error('Erro ao salvar dados:', err));
    };

    const handleCancel = () => {
        setIsEditing(false);
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setSelectedMember((prevMember) => ({
            ...prevMember,
            [name]: value,
        }));
    };

    const handlepiloto = (member) => {
        setMemberToPromote(member);
        setIsPromoting(true);
    };

    const handleConfirmPromotion = () => {
        axios.post('/api/set_piloto', memberToPromote)
            .then((res) => {
                if (res.data.success) {
                    setIsPromoting(false);
                    alert('Membro promovido com sucesso!');
                } else {
                    alert('Erro ao promover membro.');
                }
            })
            .catch((err) => {
                console.error('Erro ao promover membro:', err);
                alert('Erro ao conectar-se ao servidor.');
            });
    };

    const handleCancelPromotion = () => {
        setIsPromoting(false);
    };

    const handleAdd = () => {
        setIsAdding(true);
    };

    const handleConfirmAdd = () => {
        axios.post('/api/create_members', newMember)
            .then((res) => {
                if (res.data.success) {
                    setMembersData((prevData) => ({
                        ...prevData,
                        members: [...prevData.members, newMember],
                    }));
                    setIsAdding(false);
                    setNewMember({ nome: '', email: '', subgrupo: '' });
                } else {
                    alert('Erro ao adicionar membro.');
                }
            })
            .catch((err) => {
                console.error('Erro ao adicionar membro:', err);
                alert('Erro ao conectar-se ao servidor.');
            });
    };

    const handleCancelAdd = () => {
        setIsAdding(false);
    };

    const handleModify = () => {
        axios.post('/api/data_members')
            .then((res) => {
                if (res.data.success) {
                    setModifyData(res.data.usuario);
                    setIsModifying(true);
                } else {
                    alert('Erro ao buscar informações do usuário.');
                }
            })
            .catch((err) => {
                console.error('Erro ao buscar informações do usuário:', err);
                alert('Erro ao conectar-se ao servidor.');
            });
    };

    const handleCancelModify = () => {
        setIsModifying(false);
    };

    const handleConfirmModify = () => {
        axios.post('/api/modify_user', modifyData)
            .then((res) => {
                if (res.data.success) {
                    alert('Informações modificadas com sucesso!');
                    setIsModifying(false);
                } else {
                    alert('Erro ao modificar informações.');
                }
            })
            .catch((err) => {
                console.error('Erro ao modificar informações:', err);
                alert('Erro ao conectar-se ao servidor.');
            });
    };

    const handleModifyChange = (e) => {
        const { name, value } = e.target;
        setModifyData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };

    if (loading) return <div>Carregando...</div>;

    return (
        <div>
            <h1>Membros</h1>

            {/* Botão para modificar informações */}
            <button onClick={handleModify}>Modificar Minhas Informações</button>
            
            {/* Formulário de modificação */}
            {isModifying && (
                <div>
                    <h2>Modificar Minhas Informações</h2>
                    <form>
                        <div>
                            <label>Email:</label>
                            <input type="email" name="email" value={modifyData.email} onChange={handleModifyChange} />
                        </div>
                        <div>
                            <label>Senha:</label>
                            <input type="password" name="senha" value={modifyData.senha} onChange={handleModifyChange} />
                        </div>
                        <div>
                            <label>Confirmar Senha:</label>
                            <input type="password" name="senha_conf" value={modifyData.senha_conf} onChange={handleModifyChange} />
                        </div>
                        <div>
                            <label>Nome:</label>
                            <input type="text" name="nome" value={modifyData.nome} onChange={handleModifyChange} />
                        </div>
                        <div>
                            <label>Subgrupo:</label>
                            <input type="text" name="subgrupo" value={modifyData.subgrupo} onChange={handleModifyChange} />
                        </div>
                        <div>
                            <button type="button" onClick={handleConfirmModify}>Modificar</button>
                            <button type="button" onClick={handleCancelModify}>Cancelar</button>
                        </div>
                    </form>
                </div>
            )}

            {/* Botão para adicionar membros */}
            {membersData?.adm && (
                <button onClick={handleAdd}>Adicionar Membro</button>
            )}

            {/* Formulário de cadastro */}
            {isAdding && (
                <div>
                    <h2>Adicionar Membro</h2>
                    <form>
                        <div>
                            <label>Nome:</label>
                            <input
                                type="text"
                                name="nome"
                                onChange={(e) => setNewMember({ ...newMember, nome: e.target.value })}
                            />
                        </div>
                        <div>
                            <label>Email:</label>
                            <input
                                type="email"
                                name="email"
                                onChange={(e) => setNewMember({ ...newMember, email: e.target.value })}
                            />
                        </div>
                        <div>
                            <label>Subgrupo:</label>
                            <input
                                type="text"
                                name="subgrupo"
                                onChange={(e) => setNewMember({ ...newMember, subgrupo: e.target.value })}
                            />
                        </div>
                        <div>
                            <button type="button" onClick={handleConfirmAdd}>Confirmar</button>
                            <button type="button" onClick={handleCancelAdd}>Cancelar</button>
                        </div>
                    </form>
                </div>
            )}

            {/* Formulário de edição */}
            {isEditing && selectedMember && (
                <div>
                    <h2>Editar Membro</h2>
                    <form>
                        <div>
                            <label>Nome:</label>
                            <input
                                type="text"
                                name="nome"
                                value={selectedMember.nome}
                                onChange={handleChange}
                            />
                        </div>
                        <div>
                            <label>Email:</label>
                            <input
                                type="email"
                                name="email"
                                value={selectedMember.email}
                                onChange={handleChange}
                            />
                        </div>
                        <div>
                            <label>Subgrupo:</label>
                            <input
                                type="text"
                                name="subgrupo"
                                value={selectedMember.subgrupo}
                                onChange={handleChange}
                            />
                        </div>
                        <div>
                            <button type="button" onClick={handleSave}>Salvar</button>
                            <button type="button" onClick={handleCancel}>Cancelar</button>
                        </div>
                    </form>
                </div>
            )}

            {/* Formulário de confirmação de exclusão */}
            {isDeleting && memberToDelete && (
                <div>
                    <h2>Confirmar Exclusão</h2>
                    <p>Tem certeza de que deseja excluir o membro {memberToDelete.nome}?</p>
                    <button type="button" onClick={handleConfirmDelete}>Confirmar</button>
                    <button type="button" onClick={handleCancelDelete}>Cancelar</button>
                </div>
            )}

            {/* Formulário de promoção para piloto */}
            {isPromoting && memberToPromote && (
                <div>
                    <h2>Promover para Piloto</h2>
                    <p>Tem certeza de que deseja promover o membro {memberToPromote.nome} para piloto?</p>
                    <button type="button" onClick={handleConfirmPromotion}>Confirmar</button>
                    <button type="button" onClick={handleCancelPromotion}>Cancelar</button>
                </div>
            )}

            {/* Tabela de Membros */}
            {membersData && membersData.success && membersData.members && (
                <table>
                    <thead>
                        <tr>
                            <th>Nome</th>
                            <th>Email</th>
                            <th>Subgrupo</th>
                            {membersData.adm && (
                                <>
                                    <th>Editar</th>
                                    <th>Apagar</th>
                                    <th>Promover para piloto</th>
                                </>
                            )}
                        </tr>
                    </thead>
                    <tbody>
                        {membersData.members.map((member, index) => (
                            <tr key={index}>
                                <td>{member.nome}</td>
                                <td>{member.email}</td>
                                <td>{member.subgrupo}</td>
                                {membersData.adm && (
                                    <>
                                        <td>
                                            <button onClick={() => handleEdit(member)}>Editar</button>
                                        </td>
                                        <td>
                                            <button onClick={() => handleDelete(member)}>Apagar</button>
                                        </td>
                                        <td>
                                            <button onClick={() => handlepiloto(member)}>Promover para piloto</button>
                                        </td>
                                    </>
                                )}
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
};

export default Members;
