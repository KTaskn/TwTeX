<template>
  <div>
    <h1 id="titleheader">TwTeX</h1>
    <textarea v-model="tweetmessage" placeholder="What's happening?" />
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
      access_token: '',
      access_token_secret: '',
      tweetmessage: '',
    };
  },
  methods: {
    preview: function(message) {
      console.log('function inputs');
      this.message = message;
    },
    tocanvas: function() {
      console.log('tocanvas');
      html2canvas(document.querySelector('#previewer')).then(canvas => {
        // console.log("call html2canvas")
        // var result = document.querySelector("#result")
        // result.innerHTML = ''
        // result.appendChild(canvas)

        var img_b64 = canvas.toDataURL('image/png');

        axios
          .post('http://localhost:8888/tweet', {
            tweet: this.tweetmessage,
            img_b64: img_b64,
            oauth_token: this.oauth_token,
            oauth_verifier: this.oauth_verifier,
            access_token: this.access_token,
            access_token_secret: this.access_token_secret,
          })
          .then(res => {
            console.log(res.data);
            if (res.data.access_token) {
              this.access_token = res.data.access_token;
            }
            if (res.data.access_token_secret) {
              this.access_token_secret = res.data.access_token_secret;
            }

            this.oauth_token = '';
            this.oauth_verifier = '';
          })
          .catch(error => {
            console.log(error);
          });
      });
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
textarea {
  width: 500px;
}
#titleheader {
  width: 500px;
}
#editor {
  width: 500px;
}
#previewer {
  width: 300px;
}
</style>
