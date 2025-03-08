import { useState } from "react";

export default function Anexos() {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!file) {
        setMessage("Por favor, selecione um arquivo.");
        return;
        }
        setLoading(true);
        setMessage("");

        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = async () => {
        const base64File = reader.result.split(",")[1]; // Remove o prefixo "data:*/*;base64,"

        const payload = {
            filename: file.name,
            content: base64File,
        };

        try {
            const response = await fetch("/api/anexo", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
            });

            if (!response.ok) {
            throw new Error("Falha ao enviar o arquivo.");
            }

            setMessage("Arquivo enviado com sucesso!");
            setFile(null);
        } catch (error) {
            setMessage(error.message);
        } finally {
            setLoading(false);
        }
        };
    };

    return (
        <div className="p-4 border rounded-lg w-96">
        <h2 className="text-lg font-bold mb-2">Enviar Anexo</h2>
        <form onSubmit={handleSubmit} className="space-y-2">
            <input type="file" onChange={handleFileChange} className="block w-full" />
            <button
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded-md disabled:opacity-50"
            disabled={loading}
            >
            {loading ? "Enviando..." : "Enviar"}
            </button>
        </form>
        {message && <p className="mt-2 text-sm text-gray-700">{message}</p>}
        </div>
    );
}
