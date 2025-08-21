<template>
  <b-container>
    <div v-if="replied">
      {{ message }}
    </div>

    <b-spinner v-else />

  </b-container>

</template>
<script>
import {resolveArk} from "@/services/api";

export default {
  name: "ArkView",
  data: function () {
    return {
      naan: '',
      arkName: '',
      replied: false,
      message: ''
    }
  },
  components: {},
  props: {},
  mounted() {
    this.naan = this.$route.params.naan;
    this.arkName = this.$route.params.ark_name;
    this.resolveArguments();
  },
  methods: {
    resolveArguments() {
      resolveArk(this.naan, this.arkName).then(
          (response) => {
            if(response.data.success) {
              const data = response.data;
              if(data.success === -1) {
                this.replied = true;
                this.message = "Aucune ressource n'est associé à l'ARK donné."
              } else {
                switch (data.table_name) {
                  case "Author2023":
                    this.$router.replace(`/auteur/lire/${data.id}`);
                    break;
                  case "Enregistrement2023":
                    this.$router.replace(`/enregistrement/lire/${data.id}`);
                    break;
                  case "ReferenceBibliographiqueLivre2023":
                    this.$router.replace(`/reference-livre/lire/${data.id}`);
                    break;
                }
              }
            } else {
              this.replied = true;
              this.message = "Echec de la requête.";
            }
          }).catch((error) => {
            console.log(error);
      });
    },



  }
}

</script>
<style scoped>

</style>