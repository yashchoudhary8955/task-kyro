import { createApp } from 'vue';  // Import createApp from Vue 3 instead of Vue
import App from './App.vue';      // Ensure correct path to your App.vue file
import router from './router';    // Ensure correct path to your router setup file
import store from './store';      // Ensure correct path to your Vuex store setup file
import axios from 'axios';

const app = createApp(App);  // Create the Vue app instance using createApp

// Configure Axios globally
axios.defaults.baseURL = 'http://localhost:5000';
app.config.globalProperties.$http = axios;

// Use Vue plugins if needed (for example, Vuex and Vue Router)
app.use(router);  // Install Vue Router
app.use(store);   // Install Vuex store

// Add some debugging output to check router and store status
console.log('Router is:', router); // Check if router is correctly defined
console.log('Store is:', store);   // Check if store is correctly defined

// Mount the Vue app to the #app element in index.html
app.mount('#app')
  .$nextTick(() => console.log('App mounted successfully'))  // Check if app mounted successfully
  .$catch(error => console.error('App mount error:', error));  // Handle any mounting errors
