<template>
  <div class="form-container">
    <h1>Login</h1>
    <form @submit.prevent="login" class="form">
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required>
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <button type="submit" class="btn">Login</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
import { mapActions } from 'vuex'

export default {
  name: 'LoginL',
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    ...mapActions(['setToken', 'setUser']),
    async login() {
      try {
        const response = await axios.post('http://localhost:5000/login', {
          username: this.username,
          password: this.password
        })
        this.setToken(response.data.access_token)
        const userResponse = await axios.get('http://localhost:5000/user', {
          headers: { Authorization: `Bearer ${response.data.access_token}` }
        })
        this.setUser(userResponse.data)
        // Redirect to /transcribe route after successful login
        this.$router.push('/transcribe')
      } catch (error) {
        alert('Login failed')
      }
    }
  }
}
</script>

<style scoped>
.form-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 10px;
}

label {
  font-weight: bold;
}

input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.btn {
  padding: 10px;
  font-size: 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn:hover {
  background-color: #0056b3;
}
</style>
