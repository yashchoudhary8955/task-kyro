<template>
  <div class="home-page">
    <h1 class="title">Welcome to Voice Analyzer</h1>
    <div class="auth-links">
      <router-link to="/register" class="auth-link">Register</router-link> |
      <router-link to="/login" class="auth-link">Login</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeH'
}
</script>

<style scoped>
.home-page {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
  padding: 20px;
}

.title {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 20px;
}

.auth-links {
  font-size: 1.2rem;
  color: #555;
}

.auth-link {
  text-decoration: none;
  color: #555;
  transition: color 0.3s ease;
}

.auth-link:hover {
  color: #007bff; /* Change to your preferred hover color */
}
</style>
