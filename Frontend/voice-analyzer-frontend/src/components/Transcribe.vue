<template>
  <div class="page-container">
    <HeaderH />
    <h1>Transcribe Speech</h1>
    <form @submit.prevent="transcribe" class="form">
      <div class="form-group">
        <label>Speech Text:</label>
        <textarea v-model="text" required></textarea>
      </div>
      <!-- <div class="form-group">
        <label>Language:</label>
        <input type="text" v-model="language" class="input-language">
      </div> -->
      <button type="button" @click="startSpeechRecognition" class="btn-recognize">Start Speech Recognition</button>
      <!-- <button type="submit" class="btn-submit">Transcribe</button> -->
    </form>
    <div v-if="transcription" class="transcription-container">
      <h2>Transcription</h2>
      <p>{{ transcription }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'
import HeaderH from './header.vue'; // Adjust the path as per your actual file location

export default {
  name: 'TranscribeT',
  components: {
    HeaderH,
  },
  data() {
    return {
      text: '',
      language: '',
      transcription: null
    }
  },
  computed: {
    ...mapState(['token'])
  },
  methods: {
    async transcribe() {
      try {
        const response = await axios.post('/transcribe', {
          text: this.text,
          language: this.language
        }, {
          headers: { Authorization: `Bearer ${this.token}` }
        })
        this.transcription = response.data.transcription
      } catch (error) {
        alert('Transcription failed')
      }
    },
    startSpeechRecognition() {
      const recognition = new window.webkitSpeechRecognition() || new window.SpeechRecognition()
      recognition.lang = this.language || 'en-US' // Set language for recognition
      recognition.start()

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript
        this.text = transcript
        this.transcribe() // Automatically transcribe speech
      }

      recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error)
        alert('Speech recognition encountered an error. Please try again.')
      }
    }
  }
}
</script>

<style scoped>
.page-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

label {
  font-weight: bold;
}

textarea, .input-language {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.btn-recognize, .btn-submit {
  padding: 10px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 10px; /* Standard spacing between buttons */
}

.btn-recognize {
  background-color: #28a745;
  color: white;
}

.btn-recognize:hover {
  background-color: #218838;
}

.btn-submit {
  background-color: #007bff;
  color: white;
}

.btn-submit:hover {
  background-color: #0056b3;
}

.transcription-container {
  margin-top: 20px;
}

h1, h2, h3 {
  color: #007bff; /* Primary color for headings */
}
</style>
