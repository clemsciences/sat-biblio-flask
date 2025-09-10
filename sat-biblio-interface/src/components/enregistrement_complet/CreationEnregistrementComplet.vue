<template>
  <b-container>
    <Title title="Nouvel enregistrement"
           id="id-enregistrement-complet"
           info=""
    />
    <EnregistrementCompletFormulaire
      :record-with-reference="recordWithReference"
      :save="save"
      :disabled="!canModify"
      :message="message"/>


  </b-container>

</template>

<script>

import Title from "../visuel/Title.vue";
import {BookRecordWithReference} from "@/services/objectManager";
import {canContribute, canEdit} from "@/services/rights";
import EnregistrementCompletFormulaire from "./EnregistrementCompletFormulaire.vue";
import {createBookRecordWithReference} from "@/services/api";
import {mapState} from "vuex";

export default {
  name: "CreationEnregistrementComplet",
  components: {EnregistrementCompletFormulaire, Title},
  props: {
    disabled: {
      type: Boolean,
      default: false
    }
  },
  data: function () {
    return {
      message: "",
      recordWithReference: new BookRecordWithReference(),
      authors: [],
    }
  },
  mounted() {

  },
  methods: {
    save() {
      createBookRecordWithReference(this.recordWithReference, this.$store.state.connectionInfo.token).then(
          (response) => {
            if(response.data.success) {
              this.recordWithReference.clear();
              this.message = "Enregistrement effectué."
            } else {
              this.message = "Echec de la sauvegarde"
            }
          }
      )

    }
  },
  computed: {
    ...mapState(["connected", "connectionInfo"]),
    isManager: function() {
      return canContribute(this.$store.getters.getUserRight);
    },
    canModify: function() {
      return this.connected && canEdit(this.connectionInfo.right);
    },
  }

}
</script>

<style scoped>

</style>