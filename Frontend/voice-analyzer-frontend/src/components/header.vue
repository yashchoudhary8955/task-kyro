<template>
    <header>
      <nav>
        <ul>
          <li><router-link to="/history">History</router-link></li>
          <li><router-link to="/unique-phrases">Unique Phrases</router-link></li>
          <li><router-link to="/transcribe">Transcribe</router-link></li>
          <li><router-link to="/word-frequency">Word Frequency</router-link></li>
          <li><router-link to="/similar-users">Similar User</router-link></li>
          <li><button @click="logout" :disabled="loggingOut">Logout</button></li>
        </ul>
      </nav>
    </header>
  </template>
  
  <script>
  import axios from 'axios';
  import { mapActions, mapState } from 'vuex';
  
  export default {
    name: 'HeaderH',
    data() {
      return {
        loggingOut: false // Flag to track if logout request is in progress
      };
    },
    methods: {
      ...mapActions(['logout']),
      async logout() {
        if (this.loggingOut) return; // Prevent multiple clicks
        this.loggingOut = true; // Set flag to indicate logout in progress
  
        try {
          // Send logout request with Authorization header
          await axios.post('http://localhost:5000/logout', null, {
            headers: { Authorization: `Bearer ${this.token}` }
          });
          
          // Clear user session data in Vuex and redirect to home page
          this.logout();
          this.$router.push('/');
        } catch (error) {
          console.error('Logout failed:', error);
          alert('Failed to logout. Please try again.');
        } finally {
          this.loggingOut = false; // Reset flag after request completes
        }
      },
    },
    computed: {
      ...mapState(['token'])
    }
  };
  </script>
  
  <style scoped>
  /* Scoped styles for header */
  header {
    background-color: #f0f0f0;
    padding: 10px;
  }
  
  nav ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
  }
  
  nav ul li {
    display: inline;
    margin-right: 10px;
  }
  
  nav ul li button {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 14px;
    font-weight: bold;
    color: #333;
  }
  
  nav ul li button:hover {
    color: #555;
  }
  
  nav ul li a {
    text-decoration: none;
    color: #333;
    font-weight: bold;
  }
  
  nav ul li a:hover {
    color: #555;
  }
  </style>
  