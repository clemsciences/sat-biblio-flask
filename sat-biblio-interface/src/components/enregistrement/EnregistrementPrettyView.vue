<template>
  <b-card>
    <b-card-body>
      <p v-if="rendering.length > 0" id="copy-btn">
        <span>{{ renderReference(record.reference)}}</span>
<!--        <span>{{ renderReference(record.se)}}</span>-->
<!--        <span>{{ record. }}</span>-->
      </p>
      <input type="hidden" id="rendering" :value="rendering"/>
      <b-tooltip target="copy-btn" triggers="manual" :show="showingCopyMessage">Copié !</b-tooltip>
      <b-button class="mx-2" @click="copy">Copier</b-button>
    </b-card-body>
  </b-card>
</template>

<script>
import {Record} from "@/services/objectManager";
import {renderRecord, renderReference} from "@/services/renderingManager";

export default {
  name: "EnregistrementPrettyView",
  props: {
    record: {
      type: Record
    },
  },
  data: function() {
    return {
      showingCopyMessage: false,
    };
  },
  methods: {
    renderReference,
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
      return renderRecord(this.record);
    },
  }

}
</script>

<style scoped>

</style>