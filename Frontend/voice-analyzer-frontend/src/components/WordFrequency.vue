<template>
  <div>
    <HeaderH />
    <h1 class="page-title">Word Frequency</h1>

    <section class="frequency-section">
      <h2>User Frequency</h2>
      <table class="frequency-table">
        <thead>
          <tr>
            <th>Word</th>
            <th>Frequency</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(frequency, word) in userWordFrequency" :key="word">
            <td>{{ word }}</td>
            <td>{{ frequency }}</td>
          </tr>
        </tbody>
      </table>
    </section>

    <section class="frequency-section">
      <h2>Global Frequency</h2>
      <table class="frequency-table">
        <thead>
          <tr>
            <th>Word</th>
            <th>Frequency</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(frequency, word) in globalWordFrequency" :key="word">
            <td>{{ word }}</td>
            <td>{{ frequency }}</td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';
import HeaderH from './header.vue'; // Adjust the path as per your actual file location

export default {
  name: 'WordFrequency',
  components: {
    HeaderH,
  },
  data() {
    return {
      userWordFrequency: {},
      globalWordFrequency: {}
    };
  },
  computed: {
    ...mapState(['token'])
  },
  async created() {
    try {
      const response = await axios.get('http://localhost:5000/word_frequency', {
        headers: { Authorization: `Bearer ${this.token}` }
      });
      this.userWordFrequency = response.data.user_frequency;
      this.globalWordFrequency = response.data.global_frequency;
    } catch (error) {
      console.error('Failed to load word frequency:', error);
      alert('Failed to load word frequency. Please try again.');
    }
  }
};
</script>

<style scoped>
/* Scoped styles for WordFrequency component */

.page-title {
  margin-bottom: 20px;
  color: #333;
}

.frequency-section {
  margin-bottom: 30px;
}

.frequency-table {
  width: 100%;
  border-collapse: collapse;
}

.frequency-table th,
.frequency-table td {
  padding: 10px;
  border: 1px solid #ccc;
  text-align: left;
}

.frequency-table th {
  background-color: #f0f0f0;
  font-weight: bold;
}
</style>
