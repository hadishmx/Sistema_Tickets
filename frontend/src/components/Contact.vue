<template>
    <div class="Section-father">
        <div class="Title">
            <h1>Contacto</h1>
        </div>
        <template>
    <v-btn color="primary">Botón de Vuetify</v-btn>
</template>

    </div>
</template>

<script>

export default {
    name: 'Contacto',
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


.Display-info{
    display: flex;
    margin: 2rem;
    justify-content: space-between;
    padding: 5px;
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