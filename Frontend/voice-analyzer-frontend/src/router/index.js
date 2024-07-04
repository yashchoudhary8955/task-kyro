import { createRouter, createWebHistory } from 'vue-router';
import HomeH from '../components/Home.vue';
import HistoryH from '../components/History.vue';
import RegisterR from '../components/Register.vue';
import LoginL from '../components/Login.vue';
import TranscribeT from '../components/Transcribe.vue';
import WordFrequency from '../components/WordFrequency.vue';
import UniquePhrases from '../components/UniquePhrases.vue';
import SimilarUsers from '../components/SimilarUsers.vue';

const routes = [
  { path: '/', component: HomeH },
  { path: '/history', component: HistoryH },
  { path: '/register', component: RegisterR },
  { path: '/login', component: LoginL },
  { path: '/transcribe', component: TranscribeT },
  { path: '/word-frequency', component: WordFrequency },
  { path: '/unique-phrases', component: UniquePhrases },
  { path: '/similar-users', component: SimilarUsers },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});
// Example debugging
console.log('Router is:', router); // Check if router is correctly defined
console.log('Routes are:', routes); // Check if routes are correctly defined


export default router;
