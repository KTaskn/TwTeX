<template>
  <div>
    <katex-element :expression="row" display-mode />
  </div>
</template>

<script>
export default {
  props: ['row', 'is_tex'],
  mounted() {
    //   if (this.is_tex === false) {
    //     this.row = this.row.replace("$", "\\(").replace("$", "\\)")
    //     console.log("PR false:", this.row)
    //   } else {
    //     console.log("PR true:", this.row)
    //   }
  },
  data() {
    return {};
  },
};
</script>

<style lang="scss" scoped>
@import '../../../../node_modules/katex/dist/katex.min.css';
</style>
