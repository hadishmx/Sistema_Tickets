<template class="Father-template">
    <v-container fluid class="d-flex justify-center align-center fill-height ">
      <v-row justify="center">
        <v-col cols="12" md="5">
          <div class="Section-father">
            
              
  
              <v-data-table
                class="Table"
                :headers="headers"
                :items="TiposTiqueData"
                :search="search"
                item-key="nombre"
                :sort-by="[{ key: 'nombre', order: 'asc' }]"
              >
                <template v-slot:top>
                  <v-toolbar flat>
                    <v-toolbar-title>Lista de Tipos de Tiques</v-toolbar-title>
                    <v-divider class="mx-4" inset vertical></v-divider>
                    <v-spacer></v-spacer>
                    <v-dialog v-model="dialog" max-width="500px">
                      <template v-slot:activator="{ props }">
                        <v-btn class="mb-2" color="primary" dark v-bind="props">
                          Nuevo Tipo
                        </v-btn>
                      </template>
  
                      <v-card>
                        <v-card-title>
                          <span class="text-h5">{{ formTitle }}</span>
                        </v-card-title>
  
                        <v-card-text>
                          <v-container>
                            <v-row>
                              <v-col cols="12" md="6">
                                <v-text-field v-model="editedItem.nombre" label="Nombre" :rules="nombreRules" :counter="50"></v-text-field>
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
                        <v-card-title class="text-h5">
                          ¿Estás seguro de que quieres eliminar este tipo de tique?
                        </v-card-title>
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
                    label="Buscar cliente"
                    prepend-inner-icon="mdi-magnify"
                    variant="outlined"
                    hide-details
                    single-line
                    class="Search"
                    ></v-text-field>
                  
                </template>
                
  
                <template v-slot:item.actions="{ item }">
                  <v-btn icon="mdi-pencil" class="me-2" size="small" color="warning" @click="editItem(item)">
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
    name:"ClientesList",
    data: () => ({
      search: '',
      dialog: false,
      dialogDelete: false,
      headers: [
        
      { title: 'Id', key: 'id' },
        { title: 'Nombre', key: 'nombre' },
        { title: 'Actions', key: 'actions', sortable: false },
        
      ],
      TiposTiqueData: [],  // Datos obtenidos desde la API
      editedIndex: -1,
      editedItem: {
        id:'',
        nombre: '',

        
      },
      defaultItem: {
        id:'',
        nombre: '',

        
      },
      
      nombreRules: [
        value => {
          // Validar que no contenga símbolos ni números, y que sea máximo de 50 caracteres
          const regex = /^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]+$/; // Solo letras (incluyendo acentos, ñ y espacios)
          
          if (!value) return 'El nombre es requerido.'; // Verificar si está vacío
          
          if (!regex.test(value)) return 'No debe contener números ni símbolos.';
          
          if (value.length > 50) return 'Maximo 50 caracteres.';
          
          return true; // Si pasa todas las validaciones
        }
      ],
    }),




  
    computed: {
      formTitle() {
        return this.editedIndex === -1 ? 'Nuevo Tipo de Tique' : 'Editar Tipo de Tique';
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
      this.ObtenerTiposTiques();
    },
    
    methods: {

      validateFields() {
        const fields = {
            nombre: this.editedItem.nombre,
        };

        let isValid = true; // Variable para saber si todos los campos son válidos
        let errorMessages = {}; // Objeto para almacenar mensajes de error

        // Validación de cada campo
        for (const field in fields) {
            const value = fields[field];
            const rules = this[`${field}Rules`]; // Accede a las reglas dinámicamente

            // Asegúrate de que las reglas sean un array
            if (!Array.isArray(rules)) {
                console.error(`Las reglas para ${field} no son un array:`, rules);
                continue; // Salir de este bucle si las reglas no son un array
            }

            for (const rule of rules) {
                const result = rule(value);
                if (result !== true) {
                    isValid = false;
                    errorMessages[field] = result; // Guarda el mensaje de error
                    break; // Sale del bucle al encontrar un error
                }
            }

            // Manejo de resultados de validación
            if (errorMessages[field]) {
                console.log(`Error en ${field}:`, errorMessages[field]);
            } else {
                console.log(`${field.charAt(0).toUpperCase() + field.slice(1)} es correcto`);
            }
        }

        // Retorna el estado de la validación y los mensajes de error
        return { isValid, errorMessages };
      },

      async ObtenerTiposTiques() {
        try {
          const token = localStorage.getItem('access_token');
          const response = await axios.get('http://localhost:8000/api/TipoTique/', {
            headers: {
              Authorization: `Token ${token}`,
            },
          });
          this.TiposTiqueData = response.data; // Datos asignados
          console.log(this.TiposTiqueData)
        } catch (error) {
          console.error('Error al obtener los datos:', error);
        }
      },
  
      editItem(item) {
        this.editedIndex = this.TiposTiqueData.indexOf(item);
        this.editedItem = Object.assign({}, item);
        this.dialog = true;
      },
  
      deleteItem(item) {
        this.editedIndex = this.TiposTiqueData.indexOf(item);
        this.editedItem = Object.assign({}, item);
        this.dialogDelete = true;
      },
  
      deleteItemConfirm() {
        this.TiposTiqueData.splice(this.editedIndex, 1);
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
            // Editar un cliente existente
            Object.assign(this.TiposTiqueData[this.editedIndex], this.editedItem);

            const id = this.editedItem.id;
            const url = `http://127.0.0.1:8000/api/TipoTique/${id}/`;
            const token = localStorage.getItem('access_token');

            axios.put(url, {
                nombre: this.editedItem.nombre,

            }, {
                headers: {
                    Authorization: `Token ${token}`
                }
            })
            .then(response => {
                
                this.dialog = false; // Cierra el diálogo
            })
            .catch(error => {
                console.error('Error al guardar los datos:', error);
                alert('Error al guardar los datos. Por favor, inténtalo de nuevo.'); // Manejo de error
            });

        } else {
            // Crear un nuevo cliente
            
            const { isValid, errorMessages } = this.validateFields();

            if (isValid) {
                
                const url = `http://127.0.0.1:8000/api/TipoTique/`;
                const token = localStorage.getItem('access_token');
                
                axios.post(url, {
                    nombre: this.editedItem.nombre,

                }, {
                    headers: {
                        Authorization: `Token ${token}`
                    }
                })
                .then(response => {
                  console.log('Datos enviados correctamente:', response.data);
                  this.TiposTiqueData.push(response.data); // Agregar el nuevo cliente a la lista
                  this.ObtenerTiposTiques();
                  this.dialog = false; // Cierra el diálogo
                })
                .catch(error => {
                  console.error('Error al enviar los datos:', error);
                  alert('Error al enviar los datos. Por favor, inténtalo de nuevo.'); // Manejo de error
                });
            } else {
                // Manejo de errores, podrías mostrar alertas o mensajes en la UI
                alert('Error: debe completar los campos requeridos')
            }
            
        }
        
    }
      
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