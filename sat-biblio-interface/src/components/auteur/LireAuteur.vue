<template>
  <b-container>
    <Title id="id-lecture-auteur"
           info="Fiche d'un auteur. Attention, les homonymes ne sont pas gérés."
           title="Auteur"/>
    <JsonLdHeader :json-data="auteur"/>
    <b-card>
      <b-card-title title="Fiche"/>
      <b-card-body>
        <ValidEntry v-if="canManage" :approved="auteur.valide"/>
        <b-card-header>
          <AuteurPrettyView :author="auteur" mode="sat"/>
        </b-card-header>
        <AuteurFormulaire
            :on-submit="updateAuthor"
            :auteur="auteur"
            :message="message"
            :disabled="!canModify"
        />
      <ArkInput :ark-name="auteur.ark_name"/>
      <b-button class="my-3" v-if="canModify" v-b-modal.suppression :disabled="!canModify">Supprimer</b-button>

      <b-modal id="suppression" title="Suppression de l'auteur"
        cancel-title="Annuler" ok-title="Supprimer" @ok="deleteAuthor">
        <p>Êtes-vous sûr de supprimer cet auteur ?</p>
      </b-modal>
      </b-card-body>
    </b-card>

    <b-card>
      <b-card-title title="Entrées liées"/>
      <b-card-body>
        <b-button v-b-toggle.collapse-bound class="my-2">Voir les entrées liées</b-button>
        <b-collapse id="collapse-bound" class="my-2">
          <ListeEntreesAuteur :author-id="authorId"/>
        </b-collapse>
      </b-card-body>
    </b-card>

  </b-container>
</template>

<script>
import {deleteAuthor, retrieveAuthor, updateAuthor} from "@/services/api";
import Title from "@/components/visuel/Title";
import AuteurFormulaire from "@/components/auteur/AuteurFormulaire";
import {mapState} from "vuex";
import {canEdit} from "@/services/rights";
import ValidEntry from "@/components/visuel/ValidEntry";
import ListeEntreesAuteur from "@/components/entrees/ListeEntreesAuteur";
import AuteurPrettyView from "@/components/auteur/AuteurPrettyView.vue";
import {Author} from "@/services/objectManager";
import JsonLdHeader from "@/components/web_semantics/JsonLdHeader.vue";
import ArkInput from "@/components/ark/ArkInput.vue";

export default {
  name: "LireAuteur",
  components: {JsonLdHeader,
    ArkInput,
    AuteurPrettyView,
    ValidEntry,
    AuteurFormulaire,
    Title,
    ListeEntreesAuteur},
  data: function () {
    return {
      auteur: new Author(),
      message: '',
      authorId: parseInt(this.$route.params.id),
    }
  },
  methods: {
    getAuthor: function() {
      retrieveAuthor(this.$route.params.id).then(
        (response) => {
          if(response.data.success) {
            this.auteur.first_name = response.data.author.first_name;
            this.auteur.family_name = response.data.author.family_name;
            this.auteur.valide = response.data.author.valide;
            this.auteur.ark_name = response.data.author.ark_name;
          } else {
            console.log("erreur de récupération de l'auteur");
          }
        }
      );
    },
    updateAuthor: function() {
      // const formData = {first_name: this.first_name, family_name: this.family_name};
      updateAuthor(this.$route.params.id, this.auteur, this.$store.state.connectionInfo.token).then(
        (response) => {
          if(response.data.success) {
            console.log("modifications enregistrées");
            this.$router.push("/auteur/liste");
          } else {
            console.log("échec de la modification");
          }
        }
      );
    },
    deleteAuthor: function() {
      deleteAuthor(this.$route.params.id, this.$store.state.connectionInfo.token).then(
        (response) => {
          if(response.status === 204) {
            console.log("la suppression a fonctionné");
            this.$router.replace("/auteur/liste");
          } else {
            this.message = "Impossible de supprimer l'auteur";
          }
        }
      );
    }
  },
  mounted() {
    this.auteur.valide = false;
    this.getAuthor();
  },
  computed: {
    ...mapState(["connected", "connectionInfo"]),
    canManage() {
      return this.$store.getters.canManage;
    },
    canModify: function() {
      return this.connected && canEdit(this.connectionInfo.right);
    }
  }
}
</script>

<style scoped>

</style>