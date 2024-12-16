<template>
    
    <div class="Section-father" >
        <div class="Account-Title">
            <h1>Datos Personales</h1>
        </div>
        <v-form @submit.prevent>
        <section class="Display-info" >
            <section class="personal-info" v-for="(Usuariodata,index) in Usuariodata" :key="Usuariodata">

                <v-text-field
                    v-model="Usuariodata.nombre"
                    :counter="50"
                    :rules="nombreRules"
                    label="Nombre"
                    required
                    variant="underlined"
                ></v-text-field>
                <v-text-field
                    v-model="Usuariodata.apellido"
                    :counter="50"
                    :rules="apellidoRules"
                    label="Apellido"
                    required
                    variant="underlined"
                ></v-text-field>
                <v-text-field
                    v-model="Usuariodata.correo"
                    :rules="correoRules"
                    label="Correo"
                    required
                    variant="underlined"
                ></v-text-field>
                <v-text-field
                    v-model="Usuariodata.rut"
                    :rules="rutRules"
                    :counter="10"
                    label="Rut"
                    required
                    variant="underlined"
                    @input="formatRut"
                    maxlength="10"
                ></v-text-field>
                <v-text-field
                    v-model="Usuariodata.telefono"
                    :rules="telefonoRules"
                    :counter="9"
                    maxlength="9"
                    label="Telefono"
                    required
                    variant="underlined"
                ></v-text-field>
                <v-text-field 
                    v-model="Usuariodata.fecha_nacimiento" 
                    label="Fecha de Nacimiento"
                    placeholder="DD-MM-YYYY"
                    maxlength="10"
                    :rules="fechaRules"
                    @input="formatDate"
                    variant="underlined"
                    :counter="10"
                >
                </v-text-field>
                <v-file-input
                    :rules="IMGrules"
                    accept="image/png, image/jpeg"
                    label="Subir perfil"
                    placeholder="Elige Tu Imagen"
                    prepend-icon="mdi-camera"
                    variant="underlined"
                    @change="onFileChange"
                ></v-file-input>
                
            </section>
            <section class="Account-info" >
                <div class="Avatar-info"  >
                    <img v-if="Usuariodata && Usuariodata.length > 0 && Usuariodata[0].avatar"
                        :src="getAvatarUrl(Usuariodata[0].avatar)" 
                        alt="Avatar Usuario" 
                        class="Avatar-user">
                    <img v-else 
                        :src="EjemploEmoji" 
                        alt="Avatar Usuario" 
                        class="Avatar-user">
                    <div v-if="Usuariodata && Usuariodata.length > 0">
                        
                        <v-text-field
                            v-model="Usuariodata[0].user"
                            label="Id Cuenta"
                            prepend-icon="mdi-account"
                            variant="underlined"
                            disabled
                        ></v-text-field>
                        <v-text-field
                        :value="Usuariodata?.[0]?.grupos?.name || 'Sin rol asignado'"
                        readonly
                        prepend-icon="mdi-account-group"
                        variant="underlined"
                        disabled
                        ></v-text-field>
                        
                    </div>
                </div>
            </section>
            <section>
                <div class="Account-data" >
                    <div>
                        <v-btn
                            variant="outlined" 
                            color="warning"
                            prepend-icon="mdi-pencil"
                            type="submit"
                            @click="guardarDatos"
                            >
                            Guardar
                        </v-btn>
                    </div>
                </div>
            </section>
            
        </section>
        </v-form>
    </div>
</template>

<script>
    import EjemploEmoji from '../assets/EjemploEmoji.jpg';
    import axios from 'axios';
    import { watch } from 'vue';
    export default {
        
        name: 'AccountUser',
        data() {
            return {
                EjemploEmoji,
                Usuariodata: [],
                
                Nombre:"",
                Apellido:"",
                Correo:"",
                fecha_nacimiento:"",
                rut:"",
                avatar:null,
                Id:null,
                Grupo:null,
                selectedFile: null,
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
                IMGrules:[null],
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
            };
        },
        mounted() {
           
            this.obtenerDatosUsuario(); // Llamamos la función al montar el componente
        },
        methods: {
            async obtenerDatosUsuario() {
            try {
                const token = localStorage.getItem('access_token'); // Obtenemos el token del local storage
                const response = await axios.get('http://localhost:8000/api/Usuario/', {
                headers: {
                    Authorization: `Token ${token}`, // token a la cabecera
                },
                });
                this.Usuariodata = Array.from(response.data); // Guardamos los datos del usuario
                console.log(this.Usuariodata)
                this.nombre = this.Usuariodata[0].nombre;
                this.apellido = this.Usuariodata[0].apellido;
                this.grupo = this.Usuariodata[0].grupos.name;
                
            } catch (error) {
                console.error('Error al obtener los datos del usuario:', error);
            }
            },
            onFileChange(event) {
            const file = event.target.files[0];
            if (file) {
                this.selectedFile = file; // Guarda el archivo seleccionado
            }
            },
            getAvatarUrl(avatar) {
            // Comprueba si el campo avatar contiene la URL completa o solo el nombre del archivo
            if (avatar) {
                if (avatar.startsWith('http')) {
                return avatar; // Si es una URL completa, la usa directamente
                } else {
                return `http://localhost:8000/profile/${avatar}`; // Construye la URL completa si es relativa
                }
            }
            return ''; // Devuelve una cadena vacía si no hay avatar
            },
            formatDate() {
				if (!this.fecha_nacimiento) {
					this.fecha_nacimiento = "";
				}

				// Solo permitimos números y eliminamos otros caracteres
				let date = this.fecha_nacimiento.replace(/\D/g, "");

				// Formateamos la fecha agregando los guiones
				if (date.length > 4) {
					date = date.slice(0, 2) + "-" + date.slice(2, 4) + "-" + date.slice(4, 8);
				} else if (date.length > 2) {
					date = date.slice(0, 2) + "-" + date.slice(2);
				}

				// Limitar la longitud a 10 caracteres (DD-MM-YYYY)
				this.fecha_nacimiento = date.slice(0, 10);
		    },
            formatRut() {
                if (!this.rut) {
                this.rut = "";
                }

                // Eliminamos cualquier carácter no permitido (números y 'K'/'k')
                let rut = this.rut.replace(/[^0-9kK]/g, "");

                // Formateamos el RUT: mantenemos la parte numérica y el dígito verificador separado por un guion
                let body = rut.slice(0, -1); // Todo menos el último carácter
                let dv = rut.slice(-1).toUpperCase(); // Último carácter (el dígito verificador)

                // Solo agregamos el guion si hay algo en el cuerpo del RUT
                if (body) {
                this.rut = `${body}-${dv}`;
                } else {
                this.rut = dv;
                }
            },
            
            validateFields() {
                const fields = {
                    nombre: this.Usuariodata[0].nombre,
                    apellido: this.Usuariodata[0].apellido,
                    rut: this.Usuariodata[0].rut,
                    telefono: this.Usuariodata[0].telefono,
                    correo: this.Usuariodata[0].correo
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

            async guardarDatos() {
                const token = localStorage.getItem('access_token'); // Obtén el token del local storage
                const usuarioId = this.Usuariodata[0].user;

                // Crear un objeto FormData
                const formData = new FormData();
                formData.append('nombre', this.Usuariodata[0].nombre);
                formData.append('apellido', this.Usuariodata[0].apellido);
                formData.append('correo', this.Usuariodata[0].correo);
                formData.append('fecha_nacimiento', this.Usuariodata[0].fecha_nacimiento);
                formData.append('telefono', this.Usuariodata[0].telefono);
                formData.append('rut', this.Usuariodata[0].rut);

                // Solo agrega el archivo si se seleccionó uno
                if (this.selectedFile) {
                    formData.append('avatar', this.selectedFile); // Archivo seleccionado
                }

                const { isValid, errorMessages } = this.validateFields();
                if (isValid) {
                    try {
                        // Realiza la solicitud PUT al backend
                        const response = await axios.put(`http://localhost:8000/api/Usuario/${usuarioId}/`, formData, {
                            headers: {
                                Authorization: `Token ${token}`, // Añade el token en la cabecera
                                'Content-Type': 'multipart/form-data', // Importante para manejar archivos
                            },
                        });

                        console.log('Datos guardados exitosamente:', response.data);
                        alert('Datos guardados exitosamente.');
                    } catch (error) {
                        console.error('Error al guardar los datos:', error);
                        alert('Hubo un error al guardar los datos.');
                    }
                } else {
                    console.log(errorMessages);
                    alert('Error: debe completar los campos requeridos');
                }
            }

        },
        
    };

</script>
  
  
<style scoped>
.Section-father {
  width: 1000px;
  min-height: 600px; /* Cambia height por min-height */
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
.Account-Title h1{
    text-align: center;
    text-decoration: underline;
    
}


.Display-info {
  display: flex;
  margin: 1rem;
  justify-content: space-between;
  padding: 3px;
  align-items: flex-end; /* Cambia esto de flex-end a flex-start */
}

.personal-info, .Account-info {
  flex: 1; /* Permite que las secciones se ajusten en proporción */
  margin-right: 5rem; /* Espacio entre las dos secciones */
}

.personal-info {
  display: flex;
  flex-direction: column;
  gap: 1rem; /* Añade un espacio entre los campos del formulario */
}

.Account-info {
  display: flex;
  flex-direction: column;
  align-items: center; /* Centra los elementos dentro de la cuenta */
  gap: 1rem; /* Espacio entre los campos de la cuenta */
}

h2{
    padding: 5px;
    font-size: 15px;
}
.Avatar-user{
    width: 300px;
    height: 300px;
    border-radius: 200px
}

.Account-data{
    display: flex;
    margin: 2rem;
    justify-content: space-between;
    padding: 5px;
}
</style>


