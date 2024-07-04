<template>
  <div>
    <HeaderH />
    <h1 class="page-title">Transcription History</h1>
    <ul class="history-list">
      <li v-for="entry in history" :key="entry.id" class="history-item">
        {{ entry.text }} - {{ entry.transcription }}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';
import HeaderH from './header.vue'; // Adjust the path as per your actual file location

export default {
  name: 'HistoryH',
  components: {
    HeaderH,
  },
  data() {
    return {
      history: []
    };
  },
  computed: {
    ...mapState(['token'])
  },
  async created() {
    try {
      const response = await axios.get('/history', {
        headers: { Authorization: `Bearer ${this.token}` }
      });
      this.history = response.data;
    } catch (error) {
      console.error('Failed to load history:', error);
      alert('Failed to load history. Please try again.');
    }
  }
};
</script>

<style scoped>
/* Scoped styles for HistoryH component */

.page-title {
  margin-bottom: 20px;
  color: #333;
}

.history-list {
  list-style-type: none;
  padding: 0;
}

.history-item {
  margin-bottom: 10px;
  padding: 10px;
  background-color: #f0f0f0;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
