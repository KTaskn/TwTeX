<template>
  <div>
    <Editor @inputs="preview" />
    <Previewer :message="message" />
  </div>
</template>

<script>
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
    };
  },
  methods: {
    preview: function(message) {
      this.message = message;
    },
  },
};
</script>

<style lang="scss" scoped>
p {
  font-size: 20px;
}
</style>
