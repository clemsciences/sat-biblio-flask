<template>
  <BContainer>
    <BButton @click="search" id="bnf-search-button">BNF {{ labelPrefix }}</BButton>

    <BTooltip target="bnf-search-button" triggers="hover" style="text-justify: auto;">
      Chercher dans le catalogue de la BNF
    </BTooltip>
  </BContainer>

</template>

<script>
export default {
  name: "BNFSearchBadge",
  props: {
    labelPrefix: {
      type: String,
      default: ""
    },
    author: {
      type: String,
      default: ""
    },
    title: {
      type: String,
      default: ""
    },
    isbn: {
      type: String,
      default: ""
    },
    publisher: {
      type: String,
      default: ""
    }

  },
  data: function() {
    return {

    };
  },
  methods: {
    search() {
      this.$router.push({name: "dublin-core",
        query: {
          author: encodeURIComponent(this.author),
          title: encodeURIComponent(this.title),
          isbn: encodeURIComponent(this.isbn),
          publisher: encodeURIComponent(this.publisher)
      }});
    }
  }
}
</script>

<style scoped>

</style>