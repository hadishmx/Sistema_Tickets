<template>
  <v-container fluid class="d-flex justify-center align-center fill-height" >
    <v-row justify="center" >
      <v-col cols="12" md="4">
        <div class="Section-father" >
          <v-data-table 
            color="grey-darken-3"
            class="Table"
            :headers="headers"
            :items="Cuentadata"
            :search="search"
            item-key="username"
            :sort-by="[{ key: 'username', order: 'asc' }]"
          >
            <template v-slot:top>
              <v-toolbar flat>
                <v-toolbar-title>Lista de Cuentas</v-toolbar-title>
                <v-divider class="mx-4" inset vertical></v-divider>
                <v-spacer></v-spacer>
                <v-dialog v-model="dialog" max-width="500px">
                  <template v-slot:activator="{ props }">
                    <router-link to="/RegisterUser"><v-btn variant="text" color="secondary">Registrar Cuenta</v-btn></router-link>
                  </template >
                  <v-card>
                    <v-card-title>
                      <span class="text-h5">{{ formTitle }}</span>
                    </v-card-title>

                    <v-card-text>
                      <v-container >
                        <v-row>
                          <v-col cols="12" md="6">
                            <v-card title="Usuario:" :text="editedItem.username || 'no existe usuario'"></v-card>
                          </v-col>
                          <v-col cols="12" md="6">
                            <v-card title="Correo:" :text="editedItem.email || 'no existe correo'"></v-card>
                          </v-col> 
                          <v-col cols="12" md="6">
                            <v-checkbox 
                             
                            v-model="editedItem.is_active" label="Activar Cuenta"></v-checkbox>
                          </v-col>
                          <v-col cols="12" md="6">
                            <v-select
                             
                            v-model="editedItem.grupos[0].name"
                            :items="items"
                            item-text="name"
                            :rules="[v => !!v || 'Este item es requerido']"
                            label="Establecer Rol"
                            required
                          ></v-select>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-card-text>

                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="blue-darken-1" variant="text" @click="close">
                        Cancelar
                      </v-btn>
                      <v-btn color="blue-darken-1" variant="text" @click="save">
                        Guardar
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
                <v-dialog v-model="dialogDelete" max-width="565px">
                  <v-card>
                    <v-card-title class="text-h5">¿Estás seguro de que quieres eliminar la cuenta?</v-card-title>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="blue-darken-1" variant="text" @click="closeDelete">Cancelar</v-btn>
                      <v-btn color="blue-darken-1" variant="text" @click="deleteItemConfirm">OK</v-btn>
                      <v-spacer></v-spacer>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-toolbar>
              <v-text-field
                    v-model="search"
                    label="Buscar cuenta"
                    prepend-inner-icon="mdi-magnify"
                    variant="outlined"
                    hide-details
                    single-line
                    class="Search"
              ></v-text-field>
            </template>
            <template v-slot:item.actions="{ item }">
              <v-btn icon="mdi-pencil" class="me-2" size="small" color="warning" @click="editItem(item)"  >
              </v-btn>
              <v-btn icon="mdi-delete" class="me-2" size="small"  @click="deleteItem(item)"  color="error">
              </v-btn>
            </template>
          </v-data-table>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  name:"AccountsUserList",
  data: () => ({
    search: '',
    dialog: false,
    dialogDelete: false,
    headers: [
      { title: 'Cuenta', align: 'start', key: 'username' },
      { title: 'Correo', key: 'email' },
      { title: 'Estado', key: 'is_active' },
      { title: 'ID Cuenta', key: 'id' },
      { title: 'Actions', key: 'actions', sortable: false },
    ],
    Cuentadata: [],  // Datos obtenidos desde la API
    editedIndex: -1,
    editedItem: {
      username: '',
      email: '',
      is_active: false,
      grupos:[{name:''}]
      
    },
    defaultItem: {
      username: '',
      email: '',
      is_active: false,
      grupos:[{name:''}]
  
    },
    items: [
      'Ejecutivo',
      'Atencion',
      ],
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? 'Nueva Cuenta' : 'Editar Cuenta';
    },
  },

  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
  },

  created() {
    this.ObtenerCuentas();
  },

  methods: {
    obtenerEstado(is_active) {
      return is_active ? 'Activada' : 'Desactivada';
    },
    async ObtenerCuentas() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://localhost:8000/api/Cuenta/', {
          headers: {
            Authorization: `Token ${token}`,
          },
        });
        this.Cuentadata = response.data; // Datos asignados
        console.log(this.Cuentadata)
      } catch (error) {
        console.error('Error al obtener los datos:', error);
      }
    },

    editItem(item) {
      this.editedIndex = this.Cuentadata.indexOf(item);
      this.editedItem = Object.assign({}, item);
      //console.log(this.editedItem);
      this.dialog = true;
    },

    deleteItem(item) {
      this.editedIndex = this.Cuentadata.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      this.Cuentadata.splice(this.editedIndex, 1);
      this.closeDelete();
    },

    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.Cuentadata[this.editedIndex], this.editedItem);

        const userId = this.editedItem.id;
        const is_active = this.editedItem.is_active;
        const grupo = this.editedItem.grupos[0].name;
        console.log('ID:', userId);
        console.log('Estado activo:', is_active);
        console.log('Grupo:', grupo);
        const url = `http://127.0.0.1:8000/group_and_account/${userId}/`;
        const token = localStorage.getItem('access_token');
        axios.put(url, {  // Cambia a POST si es necesario
        is_active: is_active,
        group_name: grupo  
        },{
          headers:{
            'Authorization': `Token ${token}`
          }
        })
        .then(response => {
          console.log('Datos guardados con éxito:', response.data);
          this.dialog = false;
        })
        .catch(error => {
          console.error('Error al guardar los datos:', error);
        });
      } else {
        this.Cuentadata.push(this.editedItem);
        console.log('este es un post')
      }
      this.close();
    },
  },
  
};
</script>


<style scoped>
.Table{
    width: 100%;
    height: auto;
    border-radius: 5px;
    box-shadow: 3px 4px 25px #000;
    border: 3px solid #017bab;
}

.v-btn{
    margin: 5px
  }

.Search{
    padding: 5px;
  }
</style>