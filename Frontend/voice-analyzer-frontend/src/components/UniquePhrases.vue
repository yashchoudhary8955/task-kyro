<template>
  <div>
    <HeaderH />
    <h1>Unique Phrases</h1>
    <ul v-if="uniquePhrases.length > 0" class="phrase-list">
      <li v-for="phrase in uniquePhrases" :key="phrase" class="phrase-item">
        {{ phrase }}
      </li>
    </ul>
    <p v-else>No unique phrases found.</p>
  </div>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';
import HeaderH from './header.vue'; // Adjust the path as per your actual file location

export default {
  name: 'UniquePhrases',
  components: {
    HeaderH,
  },
  data() {
    return {
      uniquePhrases: []
    };
  },
  computed: {
    ...mapState(['token'])
  },
  async created() {
    try {
      const response = await axios.get('http://localhost:5000/unique_phrases', {
        headers: { Authorization: `Bearer ${this.token}` }
      });
      this.uniquePhrases = response.data.unique_phrases;
    } catch (error) {
      console.error('Failed to load unique phrases:', error);
      alert('Failed to load unique phrases. Please try again.');
    }
  }
};
</script>

<style scoped>
/* Scoped styles for Unique Phrases component */
.phrase-list {
  list-style-type: none;
  padding: 0;
}

.phrase-item {
  margin-bottom: 5px;
  
  font-weight: bold;
}
</style>
