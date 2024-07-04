<template>
  <div class="register-page">
    <h1>Register</h1>
    <form @submit.prevent="register" class="register-form">
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required>
      </div>
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required>
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <button type="submit" class="btn-register">Register</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RegisterR',
  data() {
    return {
      username: '',
      email: '',
      password: ''
    };
  },
  methods: {
    async register() {
      try {
        const response = await axios.post('/register', {
          username: this.username,
          email: this.email,
          password: this.password
        });
        alert(response.data.message);
        this.$router.push('/login');
      } catch (error) {
        console.error('Registration failed:', error);
        alert('Registration failed. Please try again.');
      }
    }
  }
};
</script>

<style scoped>
.register-page {
  max-width: 400px;
  margin: 0 auto;
  text-align: center;
  padding: 20px;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 20px;
  color: #333; /* Dark gray */
}

.register-form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
  width: 100%;
}

label {
  font-weight: bold;
  color: #555;
}

input[type="text"],
input[type="email"],
input[type="password"] {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

button.btn-register {
  background-color: #4CAF50; /* Green */
  color: #fff;
  padding: 10px 20px;
  font-size: 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button.btn-register:hover {
  background-color: #45a049; /* Darker green */
}
</style>
