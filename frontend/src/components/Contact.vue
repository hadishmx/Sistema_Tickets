<template>
    <v-container class="contact-section" max-width="800">
      <v-card class="pa-5" elevation="3">
        <v-card-title class="headline text-center">
          Contáctanos
        </v-card-title>
        
        <v-divider class="my-4"></v-divider>
        
        <v-form ref="contactForm" v-model="valid" lazy-validation>
          <v-row dense>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="name"
                label="Nombre y Apellido"
                :rules="[rules.required]"
                outlined
                required
              ></v-text-field>
            </v-col>
            
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="email"
                label="Correo Electrónico"
                :rules="[rules.required, rules.email]"
                outlined
                required
              ></v-text-field>
            </v-col>
            
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="subject"
                label="Asunto"
                :rules="[rules.required]"
                outlined
                required
              ></v-text-field>
            </v-col>

            <v-col cols="12" sm="6">
              <v-text-field
                v-model="phone"
                label="Telefono"
                placeholder="+56XXXXXXXXXX"
                :rules="[rules.required, rules.phone]"
                outlined
                :counter="9"
                required
              ></v-text-field>
            </v-col>
            
            <v-col cols="12">
              <v-textarea
                v-model="message"
                label="Mensaje"
                :rules="[rules.required]"
                rows="5"
                outlined
                required
              ></v-textarea>
            </v-col>
          </v-row>
          
          <v-card-actions class="justify-center">
            <v-btn color="primary" :disabled="!valid" @click="submitForm">
              Enviar Mensaje
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </v-container>
  </template>
  
  <script>
  export default {
    name: 'Contact',
    data() {
      return {
        valid: false,
        name: '',
        email: '',
        subject: '',
        message: '',
        phone:'',
        rules: {
          required: (value) => !!value || 'Este campo es requerido',
          email: (value) =>
            /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(value) ||
            'Correo electrónico inválido',
          phone:(value)=> 
            /^\d{9}$/.test(value) || 'Numero Invalido',
        
        },
      };
    },
    methods: {
      submitForm() {
        if (this.$refs.contactForm.validate()) {
          
          alert('Mensaje enviado con éxito!, Pronto nos contactaremos contigo');
          this.resetForm();
        }
      },
      resetForm() {
        this.name = '';
        this.email = '';
        this.subject = '';
        this.message = '';
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