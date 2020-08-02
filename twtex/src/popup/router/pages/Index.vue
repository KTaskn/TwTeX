<template>
  <div>
    <h1 id="titleheader">TwTeX</h1>
    <Editor id="editor" @inputs="preview" />
    <Previewer id="previewer" :message="message" />
    <div id="result"></div>
    <button @click="tocanvas">Tweet</button>
    <button @click="login">login</button>
  </div>
</template>

<script>
import html2canvas from 'html2canvas';
import axios from 'axios';

import Previewer from '../components/Previewer.vue';
import Editor from '../components/Editor.vue';

export default {
  components: {
    Editor,
    Previewer,
  },
  data() {
    return {
      message: '',
      oauth_token: '',
      oauth_verifier: '',
    };
  },
  methods: {
    preview: function(message) {
      console.log('function inputs');
      this.message = message;
    },
    tocanvas: function() {
      axios
        .post('http://localhost:8888/tweet', {
          tweet: 'hello!',
          oauth_token: this.oauth_token,
          oauth_verifier: this.oauth_verifier,
        })
        .then(res => {
          console.log(res.data);
        })
        .catch(error => {
          console.log(error);
        });
      // console.log("tocanvas")
      // html2canvas(document.querySelector("#previewer")).then(function(canvas){
      //   console.log("call html2canvas")
      // 	var result = document.querySelector("#result")
      // 	result.innerHTML = ''
      //   result.appendChild(canvas)

      //   canvas.toBlob(blob => {
      //     window.location = URL.createObjectURL(blob)
      //     console.log(blob)
      //     console.log(link.href)
      //   }, 'image/png')
      // })
    },
    login: function() {
      axios
        .get('http://localhost:8888/login')
        .then(res => {
          console.log(res.data);
          if (res.data.redirect) {
            console.log('redirect');

            chrome.identity.launchWebAuthFlow(
              {
                url: res.data.redirect,
                interactive: true,
              },
              responseUrl => {
                let url = new URL(responseUrl);
                this.oauth_token = url.searchParams.get('oauth_token');
                this.oauth_verifier = url.searchParams.get('oauth_verifier');
              }
            );
          } else {
            console.log('not redirect');
          }
        })
        .catch(error => {
          console.log(error);
        });
    },
  },
};
</script>

<style lang="scss" scoped>
#titleheader {
  width: 500px;
}
#editor {
  width: 500px;
}
#previewer {
  width: 500px;
}
</style>
