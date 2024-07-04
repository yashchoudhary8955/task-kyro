<template>
    <div>
      <p>Logging out...</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { mapActions } from 'vuex';
  
  export default {
    name: 'Logout',
    methods: {
      ...mapActions(['logout']),
      async logout() {
        try {
          await axios.post('http://localhost:5000/logout');
          this.logout(); // Assuming this action clears the token and user state in Vuex
          this.$router.push('/'); // Redirect to the home page after logout
        } catch (error) {
          console.error('Logout failed:', error);
        }
      },
    },
  };
  </script>
  