<template>
  <v-container fluid class="d-flex justify-center align-center fill-height">
    <v-row justify="center">
      <v-col cols="12" md="6">
        <div class="Section-father">



          <v-data-table class="Table" :headers="headers" :items="TiquesData" :search="search" item-key="rut"
            :sort-by="[{ key: 'rut', order: 'asc' }]">
            <template v-slot:top>
              <v-toolbar flat>
                <v-toolbar-title>Lista de Tiques</v-toolbar-title>
                <v-divider class="mx-4" inset vertical></v-divider>
                <v-spacer></v-spacer>
                <v-dialog v-model="dialog" max-width="1000px">


                  <v-card>
                    <v-card-title>
                      <span class="text-h5">{{ formTitle }}</span>
                    </v-card-title>

                    <v-card-text fluid class="d-flex justify-center align-center fill-height">
                      <v-container>
                        <v-row>
                          <v-col cols="12" md="6">
                            <v-card title="Problema" :text="editedItem.problema || 'no existe de momento'"
                              style="border: 1px solid #017bab;"></v-card>
                          </v-col>
                          <v-col cols="12" md="6">
                            <v-card title="Rut del cliente" :text="editedItem.cliente || 'no existe de momento'"
                              style="border: 1px solid #017bab;"></v-card>
                          </v-col>
                          <v-col cols="12" md="6">
                            <v-card title="Tipo de servicio" :text="editedItem.servicio || 'no existe de momento'"
                              style="border: 1px solid #017bab;"></v-card>
                          </v-col>
                          <v-col cols="12" md="6">
                            <v-card title="Observaciones" :text="editedItem.observacion || 'no existe de momento'"
                              style="border: 1px solid #017bab;"></v-card>
                          </v-col>
                          <v-col cols="12" md="6">
                            <v-card title="Area de atencion" :text="editedItem.area || 'no existe de momento'"
                              style="border: 1px solid #017bab;"></v-card>
                          </v-col>
                          <v-col cols="12" md="6">
                            <v-card title="Tipo de servicio" :text="editedItem.tipo || 'no existe de momento'"
                              style="border: 1px solid #017bab;"></v-card>
                          </v-col>
                          <v-col cols="12" md="6">
                            <v-card title="Estado del servicio" :text="editedItem.estado || 'no existe de momento'"
                              style="border: 1px solid #017bab;"></v-card>
                          </v-col>
                          <v-col cols="12" md="6">
                            <v-card title="Criticidad del servicio"
                              :text="editedItem.criticidad || 'no existe de momento'"
                              style="border: 1px solid #017bab;"></v-card>
                          </v-col>
                          <v-col cols="12" md="6">
                            <v-card title="Precio" :text="editedItem.costo || 'no existe de momento'"
                              style="border: 1px solid #017bab;"></v-card>
                          </v-col>
                          <v-col cols="12" md="6"></v-col>
                          <v-col cols="12" md="6">
                            <v-card title="Creado Por:" :text="editedItem.name_crea || 'no existe de momento'"
                              style="border: 1px solid #017bab;"></v-card>
                          </v-col>
                          <v-col cols="12" md="6">
                            <v-card title="Cerrado Por:" :text="editedItem.name_cierre || 'no existe de momento'"
                              style="border: 1px solid #017bab;"></v-card>
                          </v-col>
                          <v-col cols="12" md="6">
                            <v-card title="Fecha de creacion:"
                              :text="editedItem.fecha_creacion || 'no existe fecha de momento'"
                              style="border: 1px solid #017bab;"></v-card>
                          </v-col>
                          <v-col cols="12" md="6">
                            <v-card title="Fecha de cierre:"
                              :text="editedItem.fecha_cierre || 'no existe fecha de momento'"
                              style="border: 1px solid #017bab;"></v-card>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-card-text>

                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="blue-darken-1" variant="text" @click="close">
                        Cerrar
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-toolbar>
              <v-text-field v-model="search" label="Buscar cliente" prepend-inner-icon="mdi-magnify" variant="outlined"
                hide-details single-line class="Search"></v-text-field>

            </template>


            <template v-slot:item.actions="{ item }">
              <v-btn icon="mdi-eye" class="me-2" size="small" color="primary" @click="editItem(item)">
              </v-btn>
              <v-btn icon="mdi-cash" class="me-2" size="small" color="success" @click="iniciarTransaccion(item)">
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
import transbankAPI from '../Services/Axios';

export default {
  name: "PublicTique",
  data: () => ({
    search: '',
    dialog: false,
    dialogDelete: false,
    clientRUTs: [],  // Lista para almacenar los RUTs de los clientes
    loading: false,  // Estado de carga
    userRole: localStorage.getItem('Grupo'),
    headers: [
      { title: 'Cliente', align: 'start', key: 'cliente' },
      { title: 'Problema', key: 'problema' },
      { title: 'Servicio', key: 'servicio' },
      { title: 'Criticidad', key: 'criticidad' },
      { title: 'Actions', key: 'actions', sortable: false },
    ],
    TiquesData: [],  // Datos obtenidos desde la API
    itemsTipo: [],
    editedIndex: -1,
    editedItem: {

      cliente: '',
      problema: '',
      servicio: '',
      criticidad: '',
      observacion: '',
      area: '',
      tipo: null,
      estado: 'A Resolucion',
      criticidad: '',
      fecha_creacion: '',
      fecha_cierre: '',
      usuario_crea: '',
      usuario_cierra: '',
      costo: '',

    },
    defaultItem: {

      cliente: '',
      problema: '',
      servicio: '',
      criticidad: '',
      observacion: '',
      area: '',
      tipo: '',
      estado: 'A Resolucion',
      criticidad: '',
      fecha_creacion: '',
      fecha_cierre: '',
      usuario_crea: '',
      usuario_cierra: '',
      costo: '',

    },
    itemsArea: [
      'Presencial',
      'Virtual',
    ],

    itemsEstado: [
      'A resolucion',
      'No Aplicable',
      'Resuelto',
    ],
    itemsCriticidad: [
      'Muy Baja',
      'Baja',
      'Media',
      'Alta',
      'Muy Alta',
    ],




  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? 'Nuevo Tique' : 'Tique';
    },
  },

  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
    updateTipo(value) {
      console.log("Nuevo tipo seleccionado:", value);  // Debería mostrar el id del tipo
      this.editedItem.tipo = value;
    },
  },

  created() {
    this.ObtenerTiques();
    this.fetchClientRUTs();
    this.fetchTipoTique();
  },



  methods: {

    async ObtenerTiques() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://127.0.0.1:8000/api/public/tiques/', {
        });
        this.TiquesData = response.data; // Datos asignados
        console.log(this.TiquesData)
      } catch (error) {
        console.error('Error al obtener los datos:', error);
      }
    },
    async fetchClientRUTs() {
      this.loading = true;  // Activar el indicador de carga
      try {
        const token = localStorage.getItem('access_token'); // Obtener el token
        const response = await axios.get('http://localhost:8000/api/Cliente/', {
          headers: {
            Authorization: `Token ${token}`,
          },
        });
        // Asumimos que la respuesta contiene un array de objetos de cliente
        // y que cada objeto tiene una propiedad 'rut'
        this.clientRUTs = response.data.map(cliente => cliente.rut);  // Extraer los RUTs
        console.log(this.clientRUTs);
      } catch (error) {
        console.error('Error al obtener los RUTs de los clientes:', error);
      } finally {
        this.loading = false;  // Desactivar el indicador de carga
      }
    },
    async fetchTipoTique() {
      this.loading = true;  // Activar el indicador de carga
      try {
        const token = localStorage.getItem('access_token'); // Obtener el token
        const response = await axios.get('http://localhost:8000/api/TipoTique/', {
          headers: {
            Authorization: `Token ${token}`,
          },
        });
        this.itemsTipo = response.data.map(TipoTiques => (
          TipoTiques.nombre
        ));
        console.log(this.itemsTipo);
      } catch (error) {
        console.error('Error al obtener los tipos de tiques:', error);
      } finally {
        this.loading = false;  // Desactivar el indicador de carga
      }
    },

    async iniciarTransaccion(item) {
      console.log(item.id);
      try {
        const response = await axios.post('http://localhost:8000/iniciar-transaccion/', {
          // Si necesitas enviar datos adicionales, agrégalos aquí
          id: item.id,
        });
        const { token, url } = response.data;
        // Redirige al usuario a la página de Webpay
        window.location.href = `${url}?token_ws=${token}`;
      } catch (error) {
        console.error('Error al iniciar la transacción:', error.response?.data || error.message);
      }
    },




    editItem(item) {
      this.editedIndex = this.TiquesData.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
      this.ObtenerTiques();
      console.log("ID del tique:", this.editedItem.id);
    },

    deleteItemConfirm() {
      this.TiquesData.splice(this.editedIndex, 1);
      this.closeDelete();
    },

    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
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
    validateFieldsEdited() {
      const fields = {
        problema: this.editedItem.problema,
        servicio: this.editedItem.servicio,
        observacion: this.editedItem.observacion,
        area: this.editedItem.area,
        tipo: this.editedItem.tipo,
        estado: this.editedItem.estado,
        criticidad: this.editedItem.criticidad,
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

    validateFields() {
      const fields = {
        problema: this.editedItem.problema,
        servicio: this.editedItem.servicio,
        area: this.editedItem.area,
        tipo: this.editedItem.tipo,
        estado: this.editedItem.estado,
        criticidad: this.editedItem.criticidad,
        costo: this.editedItem.costo,
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

    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.TiquesData[this.editedIndex], this.editedItem);

        const existingRuts = this.clientRUTs;
        const extracName = localStorage.getItem('Nombre');
        const extractApellido = localStorage.getItem('Apellido');
        const extracId = localStorage.getItem('ID_Account');
        const nombreCompleto = `${extracName} ${extractApellido}`;
        const Tiqueid = this.editedItem.id;
        console.log(Tiqueid);
        if (existingRuts.includes(this.editedItem.cliente)) {
          console.log('El RUT existe, Subiendo datos...');
          console.log(this.editItem);
          const { isValid, errorMessages } = this.validateFieldsEdited();
          if (isValid) {
            const url = `http://127.0.0.1:8000/api/Tiques/${Tiqueid}/`;
            const token = localStorage.getItem('access_token');

            axios.put(url, {
              problema: this.editedItem.problema,
              cliente: this.editedItem.cliente,
              servicio: this.editedItem.servicio,
              observacion: this.editedItem.observacion,
              area: this.editedItem.area,
              tipo: this.editedItem.tipo,
              estado: this.editedItem.estado,
              criticidad: this.editedItem.criticidad,
              costo: this.editedItem.costo,
              usuario_cierra: extracId,
              name_cierre: nombreCompleto,
              fecha_cierre: this.getTodayDate()
            }, {
              headers: {
                Authorization: `Token ${token}`
              }
            })
              .then(response => {
                console.log('Datos enviados correctamente:', response.data);
                this.TiquesData[this.editedIndex] = response.data;
                this.dialog = false; // Cierra el diálogo
              })
              .catch(error => {
                console.error('Error al enviar los datos:', error);
                alert('Error al enviar los datos. Por favor, inténtalo de nuevo.'); // Manejo de error
              });
          } else {
            // Manejo de errores, podrías mostrar alertas o mensajes en la UI
            alert('Erro: Debe Completar el formulario correctamente');
          }
          return;
        } else {
          alert('El rut no existe en la base de datos');
          return
        }
      } else {

        console.log(this.editedItem.tipo.nombre);
        const existingRuts = this.clientRUTs;
        const extracName = localStorage.getItem('Nombre');
        const extractApellido = localStorage.getItem('Apellido');
        const extracId = localStorage.getItem('ID_Account');

        this.editedItem.fecha_creacion = this.getTodayDate();

        const nombreCompleto = `${extracName} ${extractApellido}`;
        this.editedItem.name_crea = nombreCompleto;
        if (existingRuts.includes(this.editedItem.cliente)) {
          console.log('El RUT existe, Subiendo datos...');
          console.log(this.editItem);
          const { isValid, errorMessages } = this.validateFields();
          if (isValid) {
            const url = `http://127.0.0.1:8000/api/Tiques/`;
            const token = localStorage.getItem('access_token');

            axios.post(url, {
              problema: this.editedItem.problema,
              cliente: this.editedItem.cliente,
              servicio: this.editedItem.servicio,
              observacion: this.editedItem.observacion,
              area: this.editedItem.area,
              tipo: this.editedItem.tipo,
              estado: this.editedItem.estado,
              criticidad: this.editedItem.criticidad,
              usuario_crea: extracId,
              name_crea: nombreCompleto,
              costo: this.editedItem.costo
            }, {
              headers: {
                Authorization: `Token ${token}`
              }
            })
              .then(response => {
                console.log('Datos enviados correctamente:', response.data);
                this.TiquesData.push(this.editedItem); // Agregar el nuevo Tique a la lista
                this.ObtenerTiques();
                this.dialog = false; // Cierra el diálogo
              })
              .catch(error => {
                console.error('Error al enviar los datos:', error);
                alert('Error al enviar los datos. Por favor, inténtalo de nuevo.'); // Manejo de error
              });
          } else {
            // Manejo de errores, podrías mostrar alertas o mensajes en la UI
            alert('Erro: Debe Completar el formulario correctamente');
          }
          return;
        } else {
          alert('El rut no existe en la base de datos');
          return
        }
      }
      this.close();
    },
  },

};
</script>


<style scoped>
.Table {
  width: 100%;
  height: auto;
  border-radius: 5px;
  box-shadow: 3px 4px 25px #000;
  border: 3px solid #017bab;
}

.v-btn {
  margin: 5px
}

.Search {
  padding: 5px;
}
</style>
