import React, { useEffect, useState } from "react";

const Circuito = ({ circuito, onEdit, onDelete }) => {
    return (
        <div style={{ width: "320px", boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)", borderRadius: "16px", overflow: "hidden", border: "1px solid #ddd", margin: "10px" }}>
            <img src={circuito.imagem} alt={circuito.nome} style={{ width: "100%", height: "192px", objectFit: "cover" }} />
            <div style={{ padding: "16px" }}>
                <h2 style={{ fontSize: "20px", fontWeight: "bold", marginBottom: "8px" }}>{circuito.nome}</h2>
                <p style={{ color: "#555" }}>Local: {circuito.local}</p>
                <p style={{ color: "#555" }}>KM: {circuito.KM}</p>
                <p style={{ color: "#555" }}>Curvas: {circuito.curvas}</p>
                <p style={{ color: "#555" }}>Cones: {circuito.cones}</p>
                <p style={{ color: "#555" }}>Setores: {circuito.n_setores}</p>
                <p style={{ color: "#555" }}>Tempo Deslocamento: {circuito.tempo_deslocamento}</p>
                <p style={{ color: "#555" }}>Data Criação: {circuito.data_criacao}</p>
                <button onClick={() => onEdit(circuito)} style={{ marginRight: "10px", backgroundColor: "#ffc107", border: "none", padding: "8px", cursor: "pointer" }}>Editar</button>
                <button onClick={() => onDelete(circuito)} style={{ backgroundColor: "#dc3545", border: "none", padding: "8px", cursor: "pointer" }}>Apagar</button>
            </div>
        </div>
    );
};

const CircuitosLista = () => {
    const [circuitos, setCircuitos] = useState([]);
    const [formulario, setFormulario] = useState(null);
    const [modal, setModal] = useState(null);

    useEffect(() => {
        fetch("/api/circuits")
        .then(response => response.json())
        .then(data => setCircuitos(data.circuits))
        .catch(error => console.error("Erro ao buscar circuitos:", error));
    }, []);

    const handleCreate = () => {
        setFormulario({ nome: "", tempo_deslocamento: "", KM: "", curvas: "", cones: "", n_setores: "", local: "", data_criacao: "", imagem: null });
        setModal("criar");
    };

    const handleEdit = (circuito) => {
        setFormulario(circuito);
        setModal("editar");
    };

    const handleDelete = (circuito) => {
        setFormulario(circuito);
        setModal("apagar");
    };

    const handleInputChange = (e) => {
        setFormulario({ ...formulario, [e.target.name]: e.target.value });
    };

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setFormulario({ ...formulario, imagem: reader.result });
            };
            reader.readAsDataURL(file);
        }
    };

    const handleConfirmCreate = () => {
        fetch("/api/create_circuit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formulario)
        }).then(() => {
            setFormulario(null);
            setModal(null);
        });
    };

    const handleConfirmEdit = () => {
        fetch("/api/modify_circuit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formulario)
        }).then(() => {
            setFormulario(null);
            setModal(null);
        });
    };

    const handleConfirmDelete = () => {
        fetch("/api/delete_circuit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formulario)
        }).then(() => {
            setFormulario(null);
            setModal(null);
        });
    };

    return (
        <div>
            <button onClick={handleCreate} style={{ marginBottom: "20px", padding: "10px", backgroundColor: "#28a745", color: "white", border: "none", cursor: "pointer" }}>Criar Novo Circuito</button>
            <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center" }}>
                {circuitos.map(circuito => (
                    <Circuito key={circuito.id_circuito} circuito={circuito} onEdit={handleEdit} onDelete={handleDelete} />
                ))}
            </div>

            {/* Formulário de Criação */}
            {modal === "criar" && (
                <div style={modalStyle}>
                    <h3>Criar Novo Circuito</h3>
                    <input type="text" name="nome" placeholder="Nome" onChange={handleInputChange} />
                    <input type="text" name="tempo_deslocamento" placeholder="Tempo Deslocamento" onChange={handleInputChange} />
                    <input type="text" name="KM" placeholder="KM" onChange={handleInputChange} />
                    <input type="text" name="curvas" placeholder="Curvas" onChange={handleInputChange} />
                    <input type="text" name="cones" placeholder="Cones" onChange={handleInputChange} />
                    <input type="text" name="n_setores" placeholder="N_setores" onChange={handleInputChange} />
                    <input type="text" name="local" placeholder="Local" onChange={handleInputChange} />
                    <input type="file" onChange={handleFileChange} />
                    <button onClick={handleConfirmCreate}>Criar</button>
                    <button onClick={() => setModal(null)}>Cancelar</button>
                </div>
            )}

            {/* Formulário de Edição */}
            {modal === "editar" && (
                <div style={modalStyle}>
                    <h3>Editar Circuito</h3>
                    <label htmlFor="id">id</label>
                    <br />
                    <input type="text" name="id" value={formulario.id_circuito} onChange={handleInputChange} />
                    <br />
                    <label htmlFor="nome">nome</label>
                    <br />
                    <input type="text" name="nome" value={formulario.nome} onChange={handleInputChange} />
                    <br />
                    <label htmlFor="tempo_deslocamento">tempo_deslocamento</label>
                    <br />
                    <input type="text" name="tempo_deslocamento" value={formulario.tempo_deslocamento} onChange={handleInputChange} />
                    <br />
                    <label htmlFor="KM">KM</label>
                    <br />
                    <input type="text" name="KM" value={formulario.KM} onChange={handleInputChange} />
                    <br />
                    <label htmlFor="curvas">curvas</label>
                    <br />
                    <input type="text" name="curvas" value={formulario.curvas} onChange={handleInputChange} />
                    <br />
                    <label htmlFor="cones">cones</label>
                    <br />
                    <input type="text" name="cones" value={formulario.cones} onChange={handleInputChange} />
                    <br />
                    <label htmlFor="n_setores">n_setores</label>
                    <br />
                    <input type="text" name="n_setores" value={formulario.n_setores} onChange={handleInputChange} />
                    <br />
                    <label htmlFor="local">local</label>
                    <br />
                    <input type="text" name="local" value={formulario.local} onChange={handleInputChange} />
                    <input type="file" onChange={handleFileChange} />
                    <button onClick={handleConfirmEdit}>Salvar</button>
                    <button onClick={() => setModal(null)}>Cancelar</button>
                </div>
            )}

            {/* Confirmação de Exclusão */}
            {modal === "apagar" && (
                <div style={modalStyle}>
                    <h3>Confirmar Exclusão</h3>
                    <p>Tem certeza que deseja excluir o circuito <strong>{formulario.nome}</strong>?</p>
                    <button onClick={handleConfirmDelete} style={{ backgroundColor: "red" }}>Apagar</button>
                    <button onClick={() => setModal(null)}>Cancelar</button>
                </div>
            )}
        </div>
    );
};

const modalStyle = {
    position: "fixed",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    background: "white",
    padding: "20px",
    boxShadow: "0px 0px 10px rgba(0,0,0,0.3)"
};

export default CircuitosLista;
