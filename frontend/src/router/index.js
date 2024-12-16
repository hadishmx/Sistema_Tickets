import {createMemoryHistory, createRouter, createWebHistory} from 'vue-router';
import LoginUser from '../components/Login-User.vue';
import RegisterUser from '../components/Register-User.vue';
import AccountUser from '../components/Account-User.vue';
import TiqueList from '../components/Tique-List.vue';
import ClienteList from '../components/Cliente-List.vue';
import AccountsUserList from '../components/AccountsUser-List.vue';
import About from '../components/About.vue';
import Contact from '../components/Contact.vue';
import InicioUser from '../components/Inicio-User.vue';
import TipoTiques from '../components/Tipo-Tiques.vue';
import PublicTiqueList from '../components/PublicTique-List.vue';
import Confirmation from '../components/Confirmation.vue';
import Verificar from '../components/Verificar.vue';

const routes = [ //define las ruta de los componente
    {path: '/About',component:About, name:'About'},
    {path: '/Login',component:LoginUser, name:'Login'}, 
    {path: '/RegisterUser',component:RegisterUser, name:'RegisterUser',
      meta:{role: 'Gerente General'},
      beforeEnter: (to, from, next) => {
        const userRole = localStorage.getItem('Grupo');
        if (userRole === 'Gerente General') {
          next();
        } else {
          next('/');
          alert('No tienes Acceso esta Pagina')
        }
      }
    },
    {path: '/confirmation',component:Confirmation, name:'Confirmation',  props: (route) => ({ token_ws: route.query.token_ws })},
    {path: '/Verificar',component:Verificar, name:'Verificar'},
    {path: '/AccountUser',component:AccountUser, name:'AccountUser',
      beforeEnter: (to, from, next) => {
        const userRole = localStorage.getItem('Grupo');
        if (userRole === 'Gerente General' || userRole === 'Ejecutivo Cliente' || userRole === 'Ejecutivo Tecnico') {
          next();
        } else {
          next('/');
          alert('No tienes Acceso esta Pagina')
        }
      }
    },
    {path: '/PublicTiqueList',component:PublicTiqueList, name:'PublicTiqueList'},
    {path: '/TipoTiques',component:TipoTiques, name:'TipoTiques',
      meta:{role: 'Gerente General'},
      beforeEnter: (to, from, next) => {
        const userRole = localStorage.getItem('Grupo');
        if (userRole === 'Gerente General') {
          next();
        } else {
          next('/');
          alert('No tienes Acceso esta Pagina')
        }
      }
    },
    {path: '/InicioUser',component:InicioUser, name:'InicioUser',
      meta:{role: 'Gerente General'},
      beforeEnter: (to, from, next) => {
        const userRole = localStorage.getItem('Grupo');
        if (userRole === 'Gerente General' || userRole === 'Ejecutivo Cliente' || userRole === 'Ejecutivo Tecnico') {
          next();
        } else {
          next('/');
          alert('No tienes Acceso esta Pagina')
        }
      }
    },
    {path: '/TiqueList',component:TiqueList, name:'TiqueList',
      meta:{role: 'Ejecutivo Tecnico'},
      beforeEnter: (to, from, next) => {
        const userRole = localStorage.getItem('Grupo');
        if (userRole === 'Gerente General' || userRole === 'Ejecutivo Cliente' || userRole === 'Ejecutivo Tecnico') {
          next();
        } else {
          next('/');
          alert('No tienes Acceso esta Pagina')
        }
      }
    },
    {path: '/ClienteList',component:ClienteList, name:'ClienteList',
      meta:{role: 'Ejecutivo Cliente'},
      beforeEnter: (to, from, next) => {
        const userRole = localStorage.getItem('Grupo');
        if (userRole === 'Gerente General' || userRole === 'Ejecutivo Cliente') {
          next();
        } else {
          next('/');
          alert('No tienes Acceso esta Pagina')
        }
      }
    },
    {path: '/AccountsUserList',component:AccountsUserList, name:'AccountsUserList',
      meta:{role: 'Gerente General'},
      beforeEnter: (to, from, next) => {
        const userRole = localStorage.getItem('Grupo');
        if (userRole === 'Gerente General') {
          next();
        } else {
          next('/');
          alert('No tienes Acceso esta Pagina')
        }
      }
    },
    {path: '/Contact',component:Contact, name:'Contact'},
    
  ]
  const router = createRouter({
    history: createWebHistory(), //ignora la url del navegador
    routes,
  })
export default router 