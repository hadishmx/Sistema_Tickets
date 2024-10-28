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
    {path: '/TiqueList',component:TiqueList, name:'TiqueList',
      meta:{role: 'Atencion'},
      beforeEnter: (to, from, next) => {
        const userRole = localStorage.getItem('Grupo');
        if (userRole === 'Director General' || userRole === 'Ejecutivo' || userRole === 'Atencion') {
          next();
        } else {
          next('/AccountUser');
          alert('No tienes Acceso esta Pagina')
        }
      }
    },
    {path: '/ClienteList',component:ClienteList, name:'ClienteList',
      meta:{role: 'Ejecutivo'},
      beforeEnter: (to, from, next) => {
        const userRole = localStorage.getItem('Grupo');
        if (userRole === 'Director General' || userRole === 'Ejecutivo') {
          next();
        } else {
          next('/AccountUser');
          alert('No tienes Acceso esta Pagina')
        }
      }
    },
    {path: '/AccountsUserList',component:AccountsUserList, name:'AccountsUserList',
      meta:{role: 'Director General'},
      beforeEnter: (to, from, next) => {
        const userRole = localStorage.getItem('Grupo');
        if (userRole === 'Director General') {
          next();
        } else {
          next('/AccountUser');
          alert('No tienes Acceso esta Pagina')
        }
      }
    },
    {path: '/Contact',component:Contact, name:'Contact'},
    
  ]
  const router = createRouter({
    history: createMemoryHistory(), //ignora la url del navegador
    routes,
  })
export default router 