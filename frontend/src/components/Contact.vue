<template>
  <v-container class="contact-section" max-width="800">
    <v-card class="pa-5" elevation="3">
      <v-card-title class="headline text-center">
        Contáctanos
      </v-card-title>

      <v-divider class="my-4"></v-divider>

      <v-form
        @submit.prevent="submitForm"
        ref="contactForm"
        v-model="valid"
        lazy-validation
      >
        <v-row dense>
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="datos.name"
              label="Nombre y Apellido"
              :rules="[rules.required]"
              outlined
              required
            ></v-text-field>
          </v-col>

          <v-col cols="12" sm="6">
            <v-text-field
              v-model="datos.email"
              label="Correo Electrónico"
              :rules="[rules.required, rules.email]"
              outlined
              required
            ></v-text-field>
          </v-col>

          <v-col cols="12" sm="6">
            <v-text-field
              v-model="datos.asunto"
              label="Asunto"
              :rules="[rules.required]"
              outlined
              required
            ></v-text-field>
          </v-col>

          <v-col cols="12" sm="6">
            <v-text-field
              v-model="datos.phone"
              label="Teléfono"
              placeholder="+56XXXXXXXXX"
              :rules="[rules.required, rules.phone]"
              outlined
              required
            ></v-text-field>
          </v-col>

          <v-col cols="12">
            <v-textarea
              v-model="datos.message"
              label="Mensaje"
              :rules="[rules.required]"
              rows="5"
              outlined
              required
            ></v-textarea>
          </v-col>
        </v-row>

        <v-card-actions class="justify-center">
          <v-btn color="primary" :disabled="!valid" type="submit">
            Enviar Mensaje
          </v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "Contact",
  data() {
    return {
      valid: false,
      datos: {
        name: "",
        email: "",
        asunto: "",
        message: "",
        phone: "",
      },
      rules: {
        required: (value) => !!value || "Este campo es requerido",
        email: (value) =>
          /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(value) ||
          "Correo electrónico inválido",
        phone: (value) =>
          /^\d{9}$/.test(value) || "Número de teléfono inválido",
      },
    };
  },
  methods: {
    async submitForm() {
      // Validar el formulario antes de enviar
      if (this.$refs.contactForm.validate()) {
        try {
          // Hacer el POST al backend
          const apiUrl = 'http://localhost:8000/contact/';
          const response = await axios.post(apiUrl, {
            nombre: this.datos.name,
            email: this.datos.email,
            TituloAsunto: this.datos.asunto,
            mensaje: this.datos.message,
            telefono: this.datos.phone,
          });

          // Mostrar mensaje de éxito
          alert(response.data.message);

          // Limpiar el formulario
          this.resetForm();
        } catch (error) {
          // Manejo de errores
          console.error("Error:", error);
          alert("Error al enviar el mensaje. Inténtalo más tarde.");
        }
      }
    },
    resetForm() {
      // Restablecer los datos del formulario
      this.datos = {
        name: "",
        email: "",
        asunto: "",
        message: "",
        phone: "",
      };
      this.$refs.contactForm.reset();
    },
  },
};
</script>

  
  <style scoped>
  .contact-section {
    margin-top: 5rem;
    margin-bottom: 5rem;
  }
  
  .v-card-title {
    color: #017bab;
  }
  
  .v-btn {
    font-weight: bold;
  }
  </style>