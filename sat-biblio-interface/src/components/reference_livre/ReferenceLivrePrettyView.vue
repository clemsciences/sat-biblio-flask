<template>
  <b-card title="">
    <b-card-body>
      <p v-if="rendering.length > 0" id="copy-btn" class="mx-1">
        <span v-if="reference.authorsForm && reference.authorsForm.length > 0">
          {{ reference.authorsForm }}
        </span>
        <span v-else v-for="i in reference.selectedAuthors" :key="`${i.first_name}-${i.family_name}`">
          {{ renderAuthor(i) }},&nbsp;
        </span>
        <span v-if="reference.selectedAuthors.length === 0">
          [anonyme],&nbsp;
        </span>
      <span><i>{{renderTitle(reference)}}</i>, {{ renderEditor(reference)}}, {{ renderYear(reference) }}</span>
        <span>{{renderPages(reference)}}</span>
      </p>
      <input type="hidden" id="rendering" :value="rendering"/>
      <b-tooltip target="copy-btn" placement="topleft" triggers="manual" :show="showingCopyMessage">
        Copié !
      </b-tooltip>
      <b-button class="my-2" @click="copy">Copier</b-button>
    </b-card-body>
  </b-card>

</template>

<script>

import {
  renderAuthor,
  renderEditor,
  renderPages,
  renderReference,
  renderTitle,
  renderYear
} from "@/services/renderingManager";
import {BookReference} from "@/services/objectManager";

export default {
  name: "ReferenceLivrePrettyView",
  props: {
    reference: {
      type: BookReference
    },
    mode: {
      type: String,
      default: "sat"
    }
  },
  data: function() {
    return {
      showingCopyMessage: false,
    }
  },
  methods: {
    renderYear,
    renderEditor,
    renderPages,
    renderTitle,
    renderAuthor,
    copy() {
      let copiedTextInput = document.querySelector("#rendering");
      copiedTextInput.setAttribute("type", "text");
      copiedTextInput.select();
      try {
        document.execCommand("copy");
      } catch (err) {
        console.log("copy failed");
      }
      copiedTextInput.setAttribute('type', 'hidden');
      window.getSelection().removeAllRanges();
      this.showingCopyMessage = true
      setTimeout(() => {
         this.showingCopyMessage = false;
      }, 3000);
    },
  },

  computed: {
    rendering: function() {
      console.log(this.reference);
      return renderReference(this.reference);
    }
  }
}
</script>

<style scoped>

</style>