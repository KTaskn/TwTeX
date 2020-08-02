<template>
  <textarea v-model="message" @input="inputs" :rows="10" placeholder="What's happening?" />
</template>

<script>
export default {
  data() {
    return {
      message: '',
    };
  },
  methods: {
    inputs: function() {
      this.$emit('inputs', this.message);
    },
  },
};
</script>

<style lang="scss" scoped>
textarea {
  width: 100%;
}
</style>
