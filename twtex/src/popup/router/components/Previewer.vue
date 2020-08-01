<template>
  <div>
    <p>Previewer</p>
    <p>{{ message }}</p>
  </div>
</template>

<script>
export default {
  props: ['message'],
  data() {
    return {};
  },
};
</script>

<style lang="scss" scoped>
p {
  font-size: 20px;
}
</style>
