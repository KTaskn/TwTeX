import Vue from 'vue';
import App from './App';
import store from '../store';
import router from './router';
import VueKatex from 'vue-katex';

import 'katex/dist/katex.min.css';

Vue.use(VueKatex, {
  globalOptions: {},
});

global.browser = require('webextension-polyfill');
Vue.prototype.$browser = global.browser;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  render: h => h(App),
});
