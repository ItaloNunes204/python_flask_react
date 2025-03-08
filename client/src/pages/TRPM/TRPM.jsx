import React from "react";
import Plot from "react-plotly.js";

const TRPM = () => {
  return (
    <div>
      <h2>Gráficos TRPM</h2>

      <div style={{ width: "50%" }}>
        <h3>Gráfico de Barras</h3>
        <Plot
          data={[{
            type: "bar",
            x: ["Jan", "Feb", "Mar", "Apr", "May"],
            y: [12, 19, 3, 5, 2],
          }]}
          layout={{ title: "Vendas" }}
        />
      </div>

      <div style={{ width: "50%" }}>
        <h3>Gráfico de Linhas</h3>
        <Plot
          data={[{
            type: "scatter",
            mode: "lines",
            x: ["Jan", "Feb", "Mar", "Apr", "May"],
            y: [3, 10, 8, 7, 5],
          }]}
          layout={{ title: "Crescimento" }}
        />
      </div>

      <div style={{ width: "50%" }}>
        <h3>Gráfico de Radar</h3>
        <Plot
          data={[{
            type: "scatterpolar",
            r: [65, 59, 90, 81, 56],
            theta: ["Força", "Velocidade", "Resistência", "Agilidade", "Precisão"],
            fill: "toself"
          }]}
          layout={{ title: "Desempenho do Atleta" }}
        />
      </div>

      <div style={{ width: "50%" }}>
        <h3>Gráfico de Pontos</h3>
        <Plot
          data={[{
            type: "scatter",
            mode: "markers",
            x: [10, 15, 20],
            y: [20, 10, 30],
          }]}
          layout={{ title: "Pontos Dispersos" }}
        />
      </div>

      <div style={{ width: "50%" }}>
        <h3>Gráfico 3D de Pontos</h3>
        <Plot
          data={[{
            type: "scatter3d",
            mode: "markers",
            x: [1, 2, 3, 4, 5],
            y: [5, 4, 3, 2, 1],
            z: [10, 20, 30, 40, 50],
            marker: { size: 5, color: "red" }
          }]}
          layout={{ title: "Pontos 3D" }}
        />
      </div>

      <div style={{ width: "50%" }}>
        <h3>Gráfico 3D de Pontos com Plano</h3>
        <Plot
          data={[
            {
              type: "scatter3d",
              mode: "markers",
              x: [1, 2, 3, 4, 5],
              y: [5, 4, 3, 2, 1],
              z: [10, 20, 30, 40, 50],
              marker: { size: 5, color: "blue" }
            },
            {
              type: "surface",
              z: [[10, 20, 30], [20, 30, 40], [30, 40, 50]],
            }
          ]}
          layout={{ title: "Pontos 3D com Plano" }}
        />
      </div>
    </div>
  );
};

export default TRPM;