<template>
  <b-card title="">
    <b-card-body>
      <p v-if="rendering.length > 0" id="copy-btn"><span v-for="i in reference.selectedAuthors" :key="`${i.first_name}-${i.family_name}`">
        {{ i.family_name }} ({{ i.first_name }}),
      </span>
      <span><i>{{ reference.titre }}</i>, {{reference.lieu_edition}}, {{ reference.editeur }}, {{ reference.annee }}</span>
        <span v-if="reference.nb_page >= 0">, {{ reference.nb_page }} p.</span>
      </p>
      <input type="hidden" id="rendering" :value="rendering"/>
      <b-tooltip target="copy-btn" triggers="manual" :show="showingCopyMessage">Copié !</b-tooltip>
      <b-button class="mx-2" @click="copy">Copier</b-button>
    </b-card-body>
  </b-card>

</template>

<script>
// import {BookReference} from "@/services/objectManager";

import {renderReference} from "@/services/renderingManager";
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
    }
  },

  computed: {
    rendering: function() {
      return renderReference(this.reference);
    }
  }
}
</script>

<style scoped>

</style>