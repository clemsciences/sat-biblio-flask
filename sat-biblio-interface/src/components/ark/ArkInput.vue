<script>
export default {
  name: 'ArkInput',
  props: {
    arkName: {
      type: String
    }
  },
  data: function() {
    return {
      showingCopyMessage: false

    }
  },
  methods: {
    copy() {
      navigator.clipboard.writeText(this.url).then(
          (value) => console.log(`copied: ${value}`)

      );
      this.showingCopyMessage = true
      setTimeout(() => {
         this.showingCopyMessage = false;
      }, 3000);
    }
  },
  computed: {
    url() {
      return `${window.location.protocol}//${window.location.host}/ark:/${this.arkName}`;
    }
  }
}

</script>

<template>
  <div class="mt-3">
    <b-form-group label="Permalien (alpha)">
      <b-input-group>
        <b-form-input id="copy-btn" :value="url"/>
        <input type="hidden" id="rendering" :value="url"/>
        <b-tooltip target="copy-btn" placement="bottom" triggers="manual" :show="showingCopyMessage">
          Copié !
        </b-tooltip>
        <b-input-group-append>
          <b-button @click="copy">Copier</b-button>
<!--          <b-button variant="outline-success">Button</b-button>-->
<!--          <b-button variant="info">Button</b-button>-->
        </b-input-group-append>

      </b-input-group>
    </b-form-group>

  </div>

</template>

<style scoped>

</style>