import {createMemoryHistory, createRouter} from 'vue-router';
import LoginUser from '../components/Login-User.vue';
import RegisterUser from '../components/Register-User.vue';
import AccountUser from '../components/Account-User.vue';
import TiqueList from '../components/Tique-List.vue';
import ClienteList from '../components/Cliente-List.vue';
import AccountsUserList from '../components/AccountsUser-List.vue';
import About from '../components/About.vue';
import Contact from '../components/Contact.vue';

const routes = [ //define las ruta de los componente
    {path: '/About',component:About, name:'About'},
    {path: '/Login',component:LoginUser, name:'Login'}, 
    {path: '/RegisterUser',component:RegisterUser, name:'RegisterUser'},
    {path: '/AccountUser',component:AccountUser, name:'AccountUser'},
    {path: '/TiqueList',component:TiqueList, name:'TiqueList'},
    {path: '/ClienteList',component:ClienteList, name:'ClienteList'},
    {path: '/AccountsUserList',component:AccountsUserList, name:'AccountsUserList'},
    {path: '/Contact',component:Contact, name:'Contact'},
    
  ]
  const router = createRouter({
    history: createMemoryHistory(), //ignora la url del navegador
    routes,
  })
export default router 