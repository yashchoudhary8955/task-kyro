<template>
  <div class="similar-users-container">
    <HeaderH />
    <h1 class="page-title">Similar Users</h1>
    <ul class="user-list" v-if="similarUsers.length > 0">
      <li v-for="(user, index) in similarUsers" :key="index" class="user-item">
        {{ user }}
      </li>
    </ul>
    <p v-else class="no-users-message">No similar users found.</p>
  </div>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';
import HeaderH from './header.vue'; // Adjust the path as per your actual file location

export default {
  name: 'SimilarUsers',
  components: {
    HeaderH,
  },
  data() {
    return {
      similarUsers: []
    };
  },
  computed: {
    ...mapState(['token'])
  },
  async created() {
    try {
      const response = await axios.get('/similar_users', {
        headers: { Authorization: `Bearer ${this.token}` }
      });
      this.similarUsers = response.data.most_similar_users; // Assuming `most_similar_users` is the key in your response data
    } catch (error) {
      console.error('Failed to load similar users:', error);
      alert('Failed to load similar users');
    }
  }
};
</script>

<style scoped>
/* Scoped styles for SimilarUsers component */
.similar-users-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

.user-list {
  list-style-type: none;
  padding: 0;
}

.user-item {
  background-color: #f0f0f0;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
}

.no-users-message {
  font-style: italic;
  color: #666;
}

@media (max-width: 600px) {
  .similar-users-container {
    padding: 10px;
  }

  .page-title {
    font-size: 20px;
  }

  .user-item {
    padding: 8px;
  }
}
</style>
