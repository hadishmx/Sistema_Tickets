<template class="Father-template">
    <v-container fluid class="d-flex justify-center align-center fill-height ">
      <v-row justify="center">
        <v-col cols="12" md="4">
          <div class="Section-father">
            
              
  
              <v-data-table
                class="Table"
                :headers="headers"
                :items="ClienteData"
                :search="search"
                item-key="rut"
                :sort-by="[{ key: 'rut', order: 'asc' }]"
              >
                <template v-slot:top>
                  <v-toolbar flat>
                    <v-toolbar-title>Lista de Clientes</v-toolbar-title>
                    <v-divider class="mx-4" inset vertical></v-divider>
                    <v-spacer></v-spacer>
                    <v-dialog v-model="dialog" max-width="500px">
                      <template v-slot:activator="{ props }">
                        <v-btn class="mb-2" color="primary" dark v-bind="props">
                          Nuevo Cliente
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
                                <v-text-field v-model="editedItem.rut" label="Rut" placeholder="12345678-9" @input="formatRut" :counter="10" :rules="rutRules"></v-text-field>
                              </v-col>
                              <v-col cols="12" md="6">
                                <v-text-field v-model="editedItem.nombre" label="Nombre" :rules="nombreRules" :counter="50"></v-text-field>
                              </v-col>
                              <v-col cols="12" md="6">
                                <v-text-field v-model="editedItem.apellido" label="Apellido" :rules="apellidoRules" :counter="50"></v-text-field>
                              </v-col>
                              <v-col cols="12" md="6">
                                <v-text-field 
                                v-model="editedItem.fecha_nacimiento" 
                                label="Fecha de Nacimiento"
                                placeholder="DD-MM-YYYY"
                                maxlength="10"
                                :rules="fechaRules"
                                @input="formatDate"
                                
                                >
                              </v-text-field>
                              </v-col>
                              <v-col cols="12" md="6">
                                <v-text-field v-model="editedItem.telefono" label="Telefono" placeholder="+56XXXXXXXXX" :counter="9" :rules="telefonoRules"></v-text-field>
                              </v-col>
                              <v-col cols="12" md="6">
                                <v-text-field v-model="editedItem.correo" label="Correo Electrónico" :rules="correoRules"></v-text-field>
                              </v-col>
                              <v-col cols="12" md="6">
                                <v-file-input
                                :rules="rulesIMG"
                                  accept="image/png, image/jpeg, image/bmp"
                                  label="Avatar"
                                  placeholder="Pick an avatar"
                                  prepend-icon="mdi-camera"
                                ></v-file-input>
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
                          ¿Estás seguro de que quieres eliminar el cliente?
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
                  <v-btn icon="mdi-delete" class="me-2" size="small" color="error" @click="deleteItem(item)">
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
        
        { title: 'Rut', align: 'start', key: 'rut' },
        { title: 'Nombre', key: 'nombre' },
        { title: 'Telefono', key: 'telefono' },
        { title: 'Correo', key: 'correo' },
        { title: 'Actions', key: 'actions', sortable: false },
      ],
      ClienteData: [],  // Datos obtenidos desde la API
      editedIndex: -1,
      editedItem: {
        rut: '',
        nombre: '',
        apellido: '',
        fecha_nacimiento: '',
        telefono: '',
        correo: '',
        avatar: '',
        
      },
      defaultItem: {
        rut: '',
        nombre: '',
        apellido: '',
        fecha_nacimiento: '',
        telefono: '',
        correo: '',
        avatar: '',
        
      },
      rulesIMG: [
        value => {
          return !value || !value.length || value[0].size < 50000000 || 'Avatar size should be less than 50 MB!'
        },
      ],
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
      apellidoRules: [
        value => {
          // Validar que el valor sea una cadena
          if (typeof value !== 'string') return 'El apellido debe ser una cadena.';

          // Validar que no contenga símbolos ni números, y que sea máximo de 50 caracteres
          const regex = /^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]+$/; // Solo letras (incluyendo acentos, ñ y espacios)

          if (!value) return 'El apellido es requerido.'; // Verificar si está vacío

          if (!regex.test(value)) return 'No debe contener números ni símbolos.';

          if (value.length > 50) return 'Máximo 50 caracteres.';

          return true; // Si pasa todas las validaciones
        }
      ],
      telefonoRules: [
        value => {
          // Validar que el valor esté presente
          if (!value) return 'El número de teléfono es requerido.';
          
          // Verificar que solo contenga dígitos y tenga exactamente 9 caracteres
          const regex = /^\d{9}$/; // Solo permite 9 dígitos
          
          if (!regex.test(value)) return 'El número de teléfono debe contener exactamente 9 dígitos.';

          return true; // Si pasa la validación
        }
      ],
      correoRules: [
        value => {
          // Validar que el valor esté presente
          if (!value) return 'El correo electrónico es requerido.';

          // Expresión regular para validar el formato del correo electrónico
          const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

          if (!regex.test(value)) return 'El correo electrónico no es válido.';

          return true; // Si pasa la validación
        }
      ],
      fechaRules: [
        value => {
          if (!value) return 'La fecha es requerida.';
          // Verifica el formato DD-MM-YYYY
          const regex = /^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-\d{4}$/;
          if (!regex.test(value)) return 'El formato debe ser DD-MM-YYYY.';
          
          // Validar la fecha real (por ejemplo, no permitir el 31 de febrero)
          const [day, month, year] = value.split('-').map(Number);
          const date = new Date(year, month - 1, day); // Mes es 0-11 en JS
          if (date.getFullYear() !== year || date.getMonth() !== month - 1 || date.getDate() !== day) {
            return 'La fecha no es válida.';
          }

          return true; // Si pasa todas las validaciones
        }
      ],

      rutRules: [
        value => {
          // Validar que el valor esté presente
          if (!value) return 'El RUT es requerido.';

          // Expresión regular para validar el formato del RUT
          const regex = /^\d{7,8}-[0-9Kk]$/;

          if (!regex.test(value)) return 'El RUT debe estar en el formato 12345678-K.';

          // Separar el cuerpo y el dígito verificador
          const [body, dv] = value.split('-');
          const bodyWithoutDots = body.replace(/\./g, ''); // Eliminar puntos

          // Validar longitud del cuerpo
          if (bodyWithoutDots.length < 7 || bodyWithoutDots.length > 8) return 'El RUT no es válido.';

          // Calcular el dígito verificador
          let sum = 0;
          let multiplier = 2;

          // Recorremos el cuerpo del RUT desde el último dígito al primero
          for (let i = bodyWithoutDots.length - 1; i >= 0; i--) {
            sum += multiplier * parseInt(bodyWithoutDots[i], 10);
            multiplier = multiplier === 7 ? 2 : multiplier + 1;
          }

          const remainder = 11 - (sum % 11);
          const expectedDv = remainder === 11 ? '0' : remainder === 10 ? 'K' : remainder.toString();

          // Comparar el dígito verificador ingresado con el calculado
          if (dv.toUpperCase() !== expectedDv) return 'El RUT no es válido.';

          return true; // RUT válido
        }
      ],
    }),




  
    computed: {
      formTitle() {
        return this.editedIndex === -1 ? 'Nuevo Cliente' : 'Editar Cliente';
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
      this.ObtenerClientes();
    },
    
    methods: {

      validateFields() {
        const fields = {
            nombre: this.editedItem.nombre,
            apellido: this.editedItem.apellido,
            rut: this.editedItem.rut,
            telefono: this.editedItem.telefono,
            correo: this.editedItem.correo
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

      async ObtenerClientes() {
        try {
          const token = localStorage.getItem('access_token');
          const response = await axios.get('http://localhost:8000/api/Cliente/', {
            headers: {
              Authorization: `Token ${token}`,
            },
          });
          this.ClienteData = response.data; // Datos asignados
          console.log(this.ClienteData)
        } catch (error) {
          console.error('Error al obtener los datos:', error);
        }
      },
  
      editItem(item) {
        this.editedIndex = this.ClienteData.indexOf(item);
        this.editedItem = Object.assign({}, item);
        this.dialog = true;
      },
  
      deleteItem(item) {
        this.editedIndex = this.ClienteData.indexOf(item);
        this.editedItem = Object.assign({}, item);
        this.dialogDelete = true;
      },
  
      deleteItemConfirm() {
        this.ClienteData.splice(this.editedIndex, 1);
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

      formatDate() {
        if (!this.editedItem.fecha_nacimiento) {
          this.editedItem.fecha_nacimiento = "";
        }

        // Solo permitimos números y eliminamos otros caracteres
        let date = this.editedItem.fecha_nacimiento.replace(/\D/g, "");

        // Formateamos la fecha agregando los guiones
        if (date.length > 4) {
          date = date.slice(0, 2) + "-" + date.slice(2, 4) + "-" + date.slice(4, 8);
        } else if (date.length > 2) {
          date = date.slice(0, 2) + "-" + date.slice(2);
        }

        // Limitar la longitud a 10 caracteres (DD-MM-YYYY)
        this.editedItem.fecha_nacimiento = date.slice(0, 10);
      },
      formatRut() {
        if (!this.editedItem.rut) {
          this.editedItem.rut = "";
        }

        // Eliminamos cualquier carácter no permitido (números y 'K'/'k')
        let rut = this.editedItem.rut.replace(/[^0-9kK]/g, "");

        // Formateamos el RUT: mantenemos la parte numérica y el dígito verificador separado por un guion
        let body = rut.slice(0, -1); // Todo menos el último carácter
        let dv = rut.slice(-1).toUpperCase(); // Último carácter (el dígito verificador)

        // Solo agregamos el guion si hay algo en el cuerpo del RUT
        if (body) {
          this.editedItem.rut = `${body}-${dv}`;
        } else {
          this.editedItem.rut = dv;
        }
      },
  
      save() {
        if (this.editedIndex > -1) {
            // Editar un cliente existente
            Object.assign(this.ClienteData[this.editedIndex], this.editedItem);

            const rut = this.editedItem.rut;
            const url = `http://127.0.0.1:8000/api/Cliente/${rut}/`;
            const token = localStorage.getItem('access_token');

            axios.put(url, {
                rut: rut,
                nombre: this.editedItem.nombre,
                apellido: this.editedItem.apellido,
                fecha_nacimiento: this.editedItem.fecha_nacimiento,
                telefono: this.editedItem.telefono,
                correo: this.editedItem.correo,
                avatar: this.editedItem.avatar || null
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
            const existingRuts = this.ClienteData.map(cliente => cliente.rut);
            if (existingRuts.includes(this.editedItem.rut)) {
                alert('El RUT ya existe en el sistema. Por favor, ingrese un RUT diferente.');
                return; // Salir si el RUT ya existe
            }

            const { isValid, errorMessages } = this.validateFields();

            if (isValid) {
                
                const url = `http://127.0.0.1:8000/api/Cliente/`;
                const token = localStorage.getItem('access_token');
                
                axios.post(url, {
                    rut: this.editedItem.rut,
                    nombre: this.editedItem.nombre,
                    apellido: this.editedItem.apellido,
                    fecha_nacimiento: this.editedItem.fecha_nacimiento,
                    telefono: this.editedItem.telefono,
                    correo: this.editedItem.correo,
                    avatar: this.editedItem.avatar || null
                }, {
                    headers: {
                        Authorization: `Token ${token}`
                    }
                })
                .then(response => {
                  console.log('Datos enviados correctamente:', response.data);
                  this.ClienteData.push(response.data); // Agregar el nuevo cliente a la lista
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