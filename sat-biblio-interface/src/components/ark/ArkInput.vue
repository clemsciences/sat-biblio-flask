<script>
import {BInputGroupText} from "bootstrap-vue-next";

export default {
  name: 'ArkInput',
  components: {BInputGroupText},
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
      <BInputGroup>
        <BFormInput id="copy-btn" :value="url"/>
        <input type="hidden" id="rendering" :value="url"/>
        <BTooltip target="copy-btn" placement="bottom" triggers="manual" :show="showingCopyMessage">
          Copié !
        </BTooltip>
        <BInputGroupText>
          <BButton @click="copy">Copier</BButton>
<!--          <BButton variant="outline-success">Button</BButton>-->
<!--          <BButton variant="info">Button</BButton>-->
        </BInputGroupText>

      </BInputGroup>
    </BFormGroup>

  </div>

</template>

<style scoped>

</style>