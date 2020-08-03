<template>
  <div class="preview-container">
    <span v-for="a_row in rows" :key="a_row">
      <p v-html="a_row"></p>
    </span>
  </div>
</template>

<script>
import katex from 'katex';
import PreviewerRow from './PreviewerRow.vue';

export default {
  props: ['message'],
  components: {
    PreviewerRow,
  },
  data() {
    return {
      N_rows: 5,
      rows: [],
    };
  },
  watch: {
    message: function(value, oldValue) {
      // $$の前後の改行は削除する
      value = value.replace(/\n*\$\$\n*/g, '$$$$');
      // $$中の改行は削除する
      const reg = new RegExp(/\$\$[\s\S]+?\$\$/, 'ig');
      value = value.replace(reg, match => {
        // 式１つを１行としたいので先頭末尾には改行を加える
        return '\n' + match.replace('\n', '') + '\n';
      });
      console.log(value);
      this.rows = this.totex(value)
        .split('\n')
        .slice(0, this.N_rows);
      console.log(this.rows);
      console.log('length:', this.rows.length);
    },
  },
  methods: {
    totex: function(value) {
      if (!value) {
        return '';
      } else {
        const searchRegExpDisplay = new RegExp(/\$\$[\s\S]+?\$\$/, 'ig');
        value = value.replace(searchRegExpDisplay, match =>
          katex.renderToString(match.substring(2, match.length - 2), {
            throwOnError: false,
            displayMode: true,
          })
        );
        const searchRegExpInline = new RegExp(/\$.+?\$/, 'ig');
        return value.replace(searchRegExpInline, match =>
          katex.renderToString(match.substring(1, match.length - 1), {
            throwOnError: false,
          })
        );
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import '../../../../node_modules/katex/dist/katex.min.css';
p {
  font-size: 12px;
}
.preview-container {
  height: 120px;
}
</style>
