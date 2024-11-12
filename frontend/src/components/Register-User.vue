<template >
  <div  >
    <form @submit.prevent="Register">
    <v-card
      class="mx-auto pa-12 pb-8"
      elevation="8"
      max-width="448"
      rounded="lg"
      style="border: 1px solid #017bab;"
    >
      <div class="text-h4 mb-1">Registro</div>

      <v-divider :thickness="2" color="info" class="mb-4 border-opacity-100" ></v-divider>

      <v-text-field
        density="compact"
        placeholder="Nombre Usuario"
        prepend-inner-icon="mdi-account-outline"
        variant="outlined"
        v-model="username"
        class="ma-2"
        :rules="usernameRules"
      ></v-text-field>

      <v-text-field
        :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
        :type="visible ? 'text' : 'password'"
        density="compact"
        placeholder="Contraseña"
        prepend-inner-icon="mdi-lock-outline"
        variant="outlined"
        v-model="password"
        @click:append-inner="visible = !visible"
        class="ma-2"
        :rules="passwordRules"
      ></v-text-field>


      <v-text-field
        density="compact"
        placeholder="Repite Contraseña"
        type="password"
        prepend-inner-icon="mdi-lock-outline"
        variant="outlined"
        v-model="repeatpassword"
        class="ma-2"
        :rules="confirmPasswordRules"
      ></v-text-field>

      <v-text-field
        density="compact"
        placeholder="Email address"
        prepend-inner-icon="mdi-email-outline"
        variant="outlined"
        v-model="correo"
        class="ma-2"
        :rules="correoRules"
      ></v-text-field>

      <v-text-field
        density="compact"
        placeholder="Telefono +56XXXXXXXXXX"
        prepend-inner-icon="mdi-phone-outline"
        variant="outlined"
        v-model="telefono"
        class="ma-2"
        :rules="telefonoRules"
        :counter="9"
      ></v-text-field>

      <v-text-field
        density="compact"
        placeholder="Fecha de nacimiento"
        prepend-inner-icon="mdi-calendar-account-outline"
        variant="outlined"
        v-model="fecha_nacimiento"
        class="ma-2"
        :rules="fechaRules"
      ></v-text-field>
      
      <v-text-field
        density="compact"
        placeholder="Rut"
        prepend-inner-icon="mdi-card-account-details-outline"
        variant="outlined"
        v-model="rut"
        class="ma-2"
        :rules="rutRules"
      ></v-text-field>

      <v-text-field
        density="compact"
        placeholder="Nombre"
        prepend-inner-icon="mdi-badge-account-outline"
        variant="outlined"
        v-model="nombre"
        :rules="nombreRules"
        class="ma-2"
      ></v-text-field>

      <v-text-field
        density="compact"
        placeholder="Apellido"
        prepend-inner-icon="mdi-badge-account-outline"
        variant="outlined"
        v-model="apellido"
        :rules="apellidoRules"
        class="ma-2"
      ></v-text-field>

      <v-card
        class="mb-12"
        color="surface-variant"
        variant="tonal"
      >
        <v-card 
        
        style="border: 1px solid #FFCC80;"
        text="Atención. Al registrar acepta a todas las políticas y condiciones de la empresa. contactar con recursos humanos para conocer de estas." 
        class="text-medium-emphasis text-caption " 
        variant="tonal">  
        </v-card >
      </v-card>

      <v-btn
        class="mb-8"
        color="blue"
        size="large"
        variant="tonal"
        block
        type="submit"
      >
        Registrar
      </v-btn>

    </v-card >
    </form>
  </div >
</template>

<script>
import axios from 'axios';

export default {
  name: 'RegisterUser',
  data: () => ({
    
    username : "",
    password : "",
    repeatpassword : "",
    correo :"",
    nombre : "",
    apellido : "",
    rut : "",
    fecha_nacimiento:"",
    telefono:"",
    visible:false,
    usernameRules: [
        value => {
          

          if (!value) return 'Es requerido el nombre.'; // Verificar si está vacío

          if (value?.length <= 8) return 'minimo 8 caracteres';

          return true; // Si pasa todas las validaciones
        }
    ],
    nombreRules: [
        value => {
          
          const regex = /^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]+$/;
          if (!regex.test(value)) return 'No debe contener números ni símbolos.';

          if (!value) return 'Es requerido el nombre.'; // Verificar si está vacío

          if (value?.length <= 3) return 'minimo 3 caracteres';

          return true; // Si pasa todas las validaciones
        }
    ],
    apellidoRules: [
        value => {
          
          const regex = /^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]+$/;
          if (!regex.test(value)) return 'No debe contener números ni símbolos.';

          if (!value) return 'Es requerido el apellido.'; // Verificar si está vacío

          if (value?.length <= 3) return 'minimo 3 caracteres';

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
  computed:{
    passwordRules() {
      return [
        value => !!value || 'La contraseña es requerida.',
        value => value.length >= 8 || 'La contraseña debe tener al menos 8 caracteres.',
        value => /[a-z]/.test(value) || 'La contraseña debe contener al menos una letra minúscula.',
        value => /[A-Z]/.test(value) || 'La contraseña debe contener al menos una letra mayúscula.',
        value => /[0-9]/.test(value) || 'La contraseña debe contener al menos un número.',
        value => /[!@#$%^&*(),.?":{}|<>]/.test(value) || 'La contraseña debe contener al menos un símbolo.'
      ];
    },
    confirmPasswordRules() {
      return [
        value => !!value || 'La confirmación de la contraseña es requerida.',
        value => value === this.password || 'Las contraseñas no coinciden.'
      ];
  } ,
  },
  
  methods: {
    
    validateFieldsEdited() {
        const fields = {
            username: this.username,
            rut: this.rut,
            nombre: this.nombre,
            apellido: this.apellido,
            fecha_nacimiento: this.fecha_nacimiento,
            telefono: this.telefono,
            correo: this.correo,
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

    async Register(){
      var data = {
        username: this.username,
        password: this.password,
        email: this.correo,
        nombre: this.nombre,
        apellido: this.apellido,
        fecha_nacimiento:this.fecha_nacimiento,
        telefono:this.telefono,
        rut: this.rut,
        

      };
      console.log(data);


      try{

        const response = await this.axios.post('http://localhost:8000/register/', data); //obtiene los datos a travez del back y devuelve en una response
        console.log(response);
        alert('usuario creado');
        

      } catch (error){
        console.log(error)
      }
    },
  }
};
</script>

<style scoped>



.form-register {
  width: 400px;
  height: 640px;
  background: #4e4d4d;
  margin: auto;
  margin-top: 5rem;
  margin-bottom: 5rem;
  box-shadow: 7px 13px 37px #000;
  padding: 20px 30px;
  border-top: 4px solid #017bab;
  color: white;
  border-radius: 5px;
  display: grid;
  place-items: center;
  
}

.form-register h5 {
  margin: 0;
  width: 100%;
  text-align: center;
  height: 40px;
  margin-bottom: 30px;
  border-bottom: 1px solid;
  font-size: 20px;
}

.controls {
  width: 100%;
  border: 1px solid #017bab;
  margin-bottom: 15px;
  padding: 11px 10px;
  background: #252323;
  font-size: 14px;
  font-weight: bold;
  border-radius: 4px;
  color: #017bab;
}

.button-control{
  display: flex;
  justify-content: center;
}



.form-register p{
  height: 40px;
  width: 100%;
  text-align: center;
  border-bottom: 1px solid;
}

.form-register a {
  color: white;
  text-decoration: none;
  font-size: 14px;
}

.form-register a:hover {
  text-decoration: underline;
}
</style>