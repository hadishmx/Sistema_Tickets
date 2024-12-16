<template>
      <LineChart v-if="chartData" :data="chartData" :options="chartOptions" />
      <p v-else>Cargando datos o sin datos disponibles...</p>
  </template>
  
  <script>
  import axios from "axios";
  import { defineComponent } from "vue";
  import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, LinearScale, CategoryScale, PointElement } from "chart.js";
  import { Line } from "vue-chartjs";
  
  ChartJS.register(Title, Tooltip, Legend, LineElement, LinearScale, CategoryScale, PointElement);
  
  export default defineComponent({
    name: "GraficoVentas",
    components: {
      LineChart: Line,
    },
    props: {
      apiEndpoint: {
        type: String,
        required: true,
      },
    },
    data() {
      return {
        tiques: [], // Datos de la API
        chartData: {
            labels: [],  // Las fechas/meses estarán aquí
            datasets: [
            {
                label: "Ventas",
                data: [],  // La cantidad de ventas registradas en el mes
                borderColor: "rgba(75, 192, 192, 1)",  // Color de la línea
                fill: false,  // No llenar debajo de la línea
                tension: 0.1,  // Suavizado de la línea
                pointRadius: 5,  // Tamaño de los puntos en la línea
                pointBackgroundColor: "rgba(75, 192, 192, 1)",  // Color de los puntos
            },
            ],
        },
        chartOptions: {
          responsive: true,
          plugins: {
            legend: {
              display: true,
              position: "top",
            },
            title: {
              display: true,
              text: "Ventas Totales por Mes",
            },
          },
          scales: {
            x: {
              title: {
                display: true,
                text: "Mes",
              },
            },
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: "Ventas Totales ($)",
              },
            },
          },
        },
      };
    },
    mounted() {
      this.fetchTiques();
    },
    methods: {
      async fetchTiques() {
        try {
          const token = localStorage.getItem('access_token');
          const response = await axios.get(this.apiEndpoint,{
          headers: {
            Authorization: `Token ${token}`,
          },
        });
          this.tiques = response.data;
  
          // Generar los datos del gráfico
          this.generateChartData();
        } catch (error) {
          console.error("Error al cargar los datos:", error);
        }
      },
      generateChartData() {
        if (!this.tiques || this.tiques.length === 0) {
          console.warn("No hay datos de tiques disponibles.");
          this.chartData = {
            labels: [],
            datasets: [],
          };
          return;
        }
  
        // Procesar y agrupar los datos
        const ventasPorMes = {};
        this.tiques.forEach((tique) => {
          if (tique.estadopago) {
            const fecha = new Date(tique.fecha_pago);
            const mes = fecha.toISOString().slice(0, 7); // Año-Mes (YYYY-MM)
            if (!ventasPorMes[mes]) {
              ventasPorMes[mes] = 0;
            }
            ventasPorMes[mes] += parseFloat(tique.costo || 0); // Sumar el costo si está definido
          }
        });
  
        if (Object.keys(ventasPorMes).length === 0) {
          console.warn("No hay datos de ventas confirmadas para mostrar en el gráfico.");
          this.chartData = {
            labels: [],
            datasets: [],
          };
          return;
        }
  
        // Configurar los datos del gráfico
        this.chartData = {
          labels: Object.keys(ventasPorMes), // Meses (eje X)
          datasets: [
            {
              label: "Ventas Totales",
              data: Object.values(ventasPorMes), // Ventas Totales (eje Y)
              borderColor: "rgba(75, 192, 192, 1)",
              backgroundColor: "rgba(75, 192, 192, 0.2)",
              borderWidth: 2,
              tension: 0.4,
              pointBackgroundColor: "rgba(75, 192, 192, 1)",
            },
          ],
        };
      },
    },
  });
  </script>
  
  <style scoped>
  /* Estilos opcionales */
  </style>
  