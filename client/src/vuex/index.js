// import Vue from 'vue';
// import Vuex from 'vuex';
// // import appService from '../app.service.js'
// // import postsModule from './posts'

// Vue.use(Vuex);

// const state = {
//   isAuthenticated: false,
// };

// const store = new Vuex.Store({
//   // modules: {
//   //   postsModule
//   // },
//   state,
//   getters: {
//     isAuthenticated: (astate) => {
//       return astate.isAuthenticated;
//     },
//   },
//   actions: {
//     logout(context) {
//       context.commit('logout');
//     },
//     // login (context, credentials) {
//     //   return new Promise((resolve) => {
//     //     appService.login(credentials)
//     //       .then((data) => {
//     //         context.commit('login', data)

//     //         resolve()
//     //       })
//     //       .catch(() => {
//     //         if (typeof window !== 'undefined') { window.alert('Could not login!') }
//     //       })
//     //   })
//     // }
//   },
//   mutations: {
//     logout(astate) {
//       if (typeof window !== 'undefined') {
//         window.localStorage.setItem('token', null);
//         window.localStorage.setItem('tokenExpiration', null);
//       }
//       astate.isAuthenticated = false;
//     },
//     login(astate, token) {
//       if (typeof window !== 'undefined') {
//         window.localStorage.setItem('token', token.token);
//         window.localStorage.setItem('tokenExpiration', token.expiration);
//       }
//       astate.isAuthenticated = true;
//     },
//   },
// });

// if (typeof window !== 'undefined') {
//   document.addEventListener('DOMContentLoaded', function () {
//     const expiration = window.localStorage.getItem('tokenExpiration');
//     let unixTimestamp = new Date().getTime() / 1000;
//     if (expiration !== null && parseInt(expiration) - unixTimestamp > 0) {
//       store.state.isAuthenticated = true;
//     }
//   });
// }

// export default store;
