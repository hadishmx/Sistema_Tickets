<template>
  <v-container class="d-flex justify-center align-center" fluid>
    <v-row class="d-flex justify-center align-center">
      <v-col cols="12" sm="6" md="4" v-if="userRole === 'Ejecutivo' || userRole === 'Director General' || userRole === 'Atencion'">
        <v-card class="pa-4" outlined>
          <v-card-title class="text-center">
            <h2>Gráfico de Tiques</h2>
          </v-card-title>
          <v-card-text class="d-flex justify-center align-center">
            <DoughnutChart v-if="Tiquesdata" :data="chartData" :options="chartOptions" height="250px" width="250px"/>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Gráfico de líneas -->
      <v-col cols="12" sm="6" md="4" v-if="userRole === 'Ejecutivo' || userRole === 'Director General'">
        <v-card class="pa-4" outlined>
          <v-card-title class="text-center">
            <h2>Ingreso de Clientes</h2>
          </v-card-title>
          <v-card-text class="d-flex justify-center align-center">
            <!-- Cambio aquí: ScatterChart a LineChart -->
            <LineChart v-if="Clientesdata" :data="lineChartData" :options="lineChartOptions" height="250px" width="250px"/>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { Doughnut, Line } from "vue-chartjs";  // Cambié Scatter a Line
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, CategoryScale, LinearScale, PointElement, LineElement, TimeScale } from "chart.js"; 
import axios from "axios";
import 'chartjs-adapter-date-fns';


ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale, LinearScale, PointElement, LineElement, TimeScale); // Agregué LineElement para gráfico de líneas

export default {
  name: "TiqueChart",
  components: {
    DoughnutChart: Doughnut,
    LineChart: Line, 
  },
  data() {
    return {
      Tiquesdata: null,
      Clientesdata: null,
      userRole: localStorage.getItem('Grupo'),
      chartData: {
        labels: [],
        datasets: [
          {
            label: "Estado de Tiques",
            data: [],
            backgroundColor: ["#FF5733", "#33FF57", "#3357FF"],
            hoverOffset: 4,
          },
        ],
      },
      chartOptions: {
        responsive: true,
        plugins: {
          legend: {
            position: "top",
          },
        },
      },
      lineChartData: {
        labels: [],  // Las fechas/meses estarán aquí
        datasets: [
          {
            label: "Clientes Ingresados",
            data: [],  // La cantidad de clientes ingresados por mes
            borderColor: "rgba(75, 192, 192, 1)",  // Color de la línea
            fill: false,  // No llenar debajo de la línea
            tension: 0.1,  // Suavizado de la línea
            pointRadius: 5,  // Tamaño de los puntos en la línea
            pointBackgroundColor: "rgba(75, 192, 192, 1)",  // Color de los puntos
          },
        ],
      },
      lineChartOptions: {
        responsive: true,
        scales: {
          x: {
            type: "time",  // Eje X de tipo tiempo
            time: {
              unit: "month",  // Mostrar los datos por mes
              tooltipFormat: "MMM yyyy",  // Formato del tooltip
              displayFormats:{
                month: "MMM yyyy"
              },
            },
          },
          y: {
            title: {
              display: true,
              text: "Cantidad de Clientes",
            },
            ticks: {
              beginAtZero: true,
              stepSize: 1,
              callback: function(value) {
                return Math.floor(value);  // Mostrar valores enteros
              }
            },
          },
        },
      },
    };
  },
  mounted() {
    this.ObtenerTiques();
    this.ObtenerClientes();
  },
  methods: {
    async ObtenerTiques() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://localhost:8000/api/Tiques/', {
          headers: {
            Authorization: `Token ${token}`,
          },
        });
        this.Tiquesdata = Array.from(response.data);
        this.processChartData(); // Procesar datos para gráfico de tiques
      } catch (error) {
        console.error('Error al obtener los datos:', error);
      }
    },
    
    async ObtenerClientes() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://localhost:8000/api/Cliente/', {
          headers: {
            Authorization: `Token ${token}`,
          },
        });
        this.Clientesdata = Array.from(response.data);
        console.log(this.Clientesdata);
        this.processLineChartData(); // Procesar datos para gráfico de líneas
      } catch (error) {
        console.error('Error al obtener los datos de clientes:', error);
      }
    },

    processChartData() {
      const estadoCounts = {
        "Abierto": 0,
        "Espera": 0,
        "Cerrado": 0,
      };

      this.Tiquesdata.forEach(tique => {
        if (tique.estado === "Abierto") estadoCounts["Abierto"]++;
        if (tique.estado === "Espera") estadoCounts["Espera"]++;
        if (tique.estado === "Cerrado") estadoCounts["Cerrado"]++;
      });

      this.chartData.labels = Object.keys(estadoCounts);
      this.chartData.datasets[0].data = Object.values(estadoCounts);
    },

    processLineChartData() {
      // Paso 1: Agrupamos los datos mensualmente
      const monthlyCounts = this.Clientesdata.reduce((acc, cliente) => {
        const fecha = new Date(cliente.fecha_creacion);
        const mesAño = `${fecha.getFullYear()}-${fecha.getMonth() + 1}`;

        // Contamos la cantidad de clientes por mes
        if (!acc[mesAño]) {
          acc[mesAño] = 0;
        }
        acc[mesAño] += 1;
        return acc;
      }, {});

      // Paso 2: Convertimos los datos en un formato adecuado para el gráfico y aplicamos la suma acumulativa
      let acumulado = 0;
      const clienteIngresos = Object.keys(monthlyCounts)
        .sort((a, b) => new Date(a) - new Date(b)) // Ordenamos por fecha
        .map(mesAño => {
          const [year, month] = mesAño.split("-");
          acumulado += monthlyCounts[mesAño]; // Acumulamos la cantidad de clientes

          return {
            x: new Date(year, month - 1), // Usamos solo año y mes para la fecha en el gráfico
            y: acumulado, // Total acumulado de clientes
          };
        });

      // Paso 3: Agregamos la fecha actual al gráfico si no existe
      const fechaActual = new Date();
      const fechaActualMes = `${fechaActual.getFullYear()}-${fechaActual.getMonth() + 1}`;
      if (!monthlyCounts[fechaActualMes]) {
        clienteIngresos.push({
          x: new Date(fechaActual.getFullYear(), fechaActual.getMonth()), // Fecha actual
          y: acumulado, // Total acumulado hasta el mes actual
        });
      }

      // Paso 4: Actualizamos los datos del gráfico
      this.lineChartData.datasets[0].data = clienteIngresos;
      this.lineChartData.labels = clienteIngresos.map(item => item.x); // Etiquetas de fecha
    },

    convertToMonth(fecha) {
      if (!fecha) {
        console.error("Fecha no válida:", fecha);
        return null;
      }

      const [day, month, year] = fecha.split("-"); // Suponiendo que la fecha está en formato DD-MM-YYYY
      return new Date(year, month - 1, 1); // Creamos una fecha usando solo el año y mes (el día es arbitrario, lo fijamos en 1)
    }
  },
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  max-width: 800px;
  margin: auto;
  padding: 20px;
}

v-card {
  border-radius: 10px;
  background-color: #f5f5f5;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

v-card-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}

v-card-subtitle {
  font-size: 1rem;
  color: #555;
}

v-divider {
  background-color: #FF5733;
  height: 2px;
}

v-col {
  padding: 10px;
}
</style>
