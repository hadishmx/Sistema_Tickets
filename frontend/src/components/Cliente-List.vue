<template >
    <div class="Section-father">
        <div class="Title">
            <h1>Lista de Clientes</h1>
        </div>
        <div class="Table">
            <v-card
            title="Busqueda"
            flat
            >
            <template v-slot:text>
                <v-text-field
                v-model="search"
                label="Search"
                prepend-inner-icon="mdi-magnify"
                variant="outlined"
                hide-details
                single-line
                ></v-text-field>
            </template>
        
            <v-data-table
                :headers="headers"
                :items="Clientedata"
                :search="search"
                density="compact"
                item-key="id"
            ></v-data-table>
            </v-card>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: 'ClientesList',
    data() {
        return {
            search: '',
            Clientedata: [],
            headers: [
          { title: 'Nombre Cliente', align: 'start', key: 'nombre' },
          { title: 'Apellido Cliente', align: 'end', key: 'apellido' },
          { title: 'Telefono', align: 'end', key: 'telefono' },
          { title: 'Correo', align: 'end', key: 'correo' },
        ],
      }
        
      
    },
    mounted() {
    this.ObtenerClientes(); // Llamamos la función al montar el componente
    },
    methods: {
        async ObtenerClientes() {
        try {
            const token = localStorage.getItem('access_token');
            const response = await axios.get('http://localhost:8000/api/Cliente/', {
                headers: {
                Authorization: `Token ${token}`, // token a la cabecera
            },
            });
            this.Clientedata = response.data; // Asigna directamente los datos recibidos
            console.log(this.Clientedata)
        } catch (error) {
            console.error('Error al obtener los datos:', error);}
        },
        
    },
};
</script>


<style scoped>
.Section-father {
  width: 1000px;
  height: 600px;
  background: #4e4d4d;
  margin: auto;
  margin-top: 5rem;
  margin-bottom: 5rem;
  box-shadow: 7px 13px 37px #000;
  padding: 20px 30px;
  border-top: 4px solid #017bab;
  color: white;
  border-radius: 5px;
}
.Title h1{
    text-align: center;
    text-decoration: underline;
    
}


.Table{
    margin-top: 3rem;
    border-radius: 5px;
    box-shadow: 3px 4px 25px #000;
    border: 3px solid #017bab;
}



</style>