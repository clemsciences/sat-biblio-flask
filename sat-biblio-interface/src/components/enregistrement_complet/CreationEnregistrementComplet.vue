<template>
  <b-container>
    <Title title="Nouvel enregistrement"
           id="id-enregistrement-complet"
           info=""
    />
    <EnregistrementCompletFormulaire
      :record-with-reference="recordWithReference"
      :save="save"
      :disabled="!isManager"
      :message="message"/>


  </b-container>

</template>

<script>

import Title from "../visuel/Title.vue";
import {BookRecordWithReference} from "@/services/objectManager";
import {canManage} from "@/services/rights";
import EnregistrementCompletFormulaire from "./EnregistrementCompletFormulaire.vue";
import {createBookRecordWithReference} from "@/services/api";

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
    isManager: function() {
      return canManage(this.$store.getters.getUserRight);
    }
  }

}
</script>

<style scoped>

</style>