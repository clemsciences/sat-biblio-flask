<script>
export default {
  name: 'ArkInput',
  props: {
    arkName: {
      type: String,
      default: ""
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
    <BFormGroup label="Permalien (alpha)">
      <b-input-group>
        <BFormInput id="copy-btn" :value="url"/>
        <input type="hidden" id="rendering" :value="url"/>
        <BTooltip target="copy-btn" placement="bottom" triggers="manual" :show="showingCopyMessage">
          Copié !
        </BTooltip>
        <b-input-group-append>
          <BButton @click="copy">Copier</BButton>
<!--          <BButton variant="outline-success">Button</BButton>-->
<!--          <BButton variant="info">Button</BButton>-->
        </b-input-group-append>

      </b-input-group>
    </BFormGroup>

  </div>

</template>

<style scoped>

</style>