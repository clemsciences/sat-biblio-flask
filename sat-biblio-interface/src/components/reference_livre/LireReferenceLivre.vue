<template>
  <BContainer>
    <AppTitle
      title="Référence bibliographique"
      id="id-ref-biblio-lecture"
      info=""/>
    <JsonLdHeader :json-data="reference"/>
    <BCard>
      <BCardTitle title="Fiche"/>
      <BCardBody>
<!--        <ValidEntry v-if="canManage" :approved="reference.valide"/>-->
        <BCardHeader>
          <ReferenceLivrePrettyView :reference="reference"/>
        </BCardHeader>
        <ReferenceLivreFormulaire
            :message="message"
            :on-submit="updateReference"
            :reference="reference"
            :disabled="!canModify"
            @update:selectedAuthors="reference.selectedAuthors = $event"
            @update:authorsForm="reference.authorsForm = $event"
            @update:titre="reference.titre = $event"
            @update:lieu_edition="reference.lieu_edition = $event"
            @update:editeur="reference.editeur = $event"
            @update:annee="reference.annee = $event"
            @update:nb_page="reference.nb_page = $event"
            @update:description="reference.description = $event"
        />
        <BButton class="my-3" v-b-toggle.suppression v-if="canModify" :disabled="!canModify">Supprimer</BButton>
        <BModal id="suppression" title="Suppression de la référence"
          cancel-title="Annuler" ok-title="Supprimer" @ok="deleteReference">
          <p>Êtes-vous sûr de supprimer cette référence ?</p>
        </BModal>
        <ArkInput :ark-name="reference.ark_name"/>
      </BCardBody>
    </BCard>

    <BCard>
        <BCardTitle title="Entrées liées"/>
        <BCardBody>
          <BButton v-b-toggle.collapse-bound class="my-2">Voir les entrées liées</BButton>
          <BCollapse id="collapse-bound" class="my-2">
            <liste-entrees-reference :reference-id="referenceId"/>
          </BCollapse>
        </BCardBody>
      </BCard>
  </BContainer>
</template>

<script>
import axios from "axios";
import {deleteBookReference, retrieveBookReference, updateBookReference} from "@/services/api";
import AppTitle from "@/components/visuel/AppTitle.vue";
import ReferenceLivreFormulaire from "@/components/reference_livre/ReferenceLivreFormulaire.vue";
import {canEdit} from "@/services/rights";
import {mapState} from "vuex";
// import ValidEntry from "@/components/visuel/ValidEntry";
import ListeEntreesReference from "@/components/entrees/ListeEntreesReference.vue";
import ReferenceLivrePrettyView from "@/components/reference_livre/ReferenceLivrePrettyView.vue";
import {BookReference} from "@/services/objectManager.js";
import JsonLdHeader from "@/components/web_semantics/JsonLdHeader.vue";
import ArkInput from "@/components/ark/ArkInput.vue";

export default {
name: "LireReferenceLivre",
  components: {
    JsonLdHeader,
    ArkInput,
    ReferenceLivrePrettyView,
    ListeEntreesReference,
    // ValidEntry,
    ReferenceLivreFormulaire,
    AppTitle},
  data: function () {
    return {
      suggestedAuthors: [],
      reference: new BookReference(),
      message: "",
      selectedAuthorsMessage: "Les auteurs sélectionnés vont s'afficher en dessous.",
      referenceId: parseInt(this.$route.params.id),
    }
  },
  methods: {
    getReference: function() {
        retrieveBookReference(this.$route.params.id)
          .then(
              (response) => {
                if(response.data.success) {
                  // console.log("authors");
                  // console.log(response.data.reference);
                  this.reference.selectedAuthors = response.data.reference.authors;

                  this.reference.titre = response.data.reference.titre;
                  this.reference.lieu_edition = response.data.reference.lieu_edition;
                  this.reference.editeur = response.data.reference.editeur;
                  this.reference.annee = response.data.reference.annee;
                  this.reference.nb_page = response.data.reference.nb_page;
                  this.reference.valide = response.data.reference.valide;
                  this.reference.description = response.data.reference.description;
                  this.reference.ark_name = response.data.reference.ark_name;
                  this.message = "";
                } else {
                  this.message = "Impossible de récupérer la référence."
                }
              }
          )
    },
    updateReference: function() {
      const formData = {
        auteurs: this.reference.selectedAuthors,
        titre: this.reference.titre,
        lieu_edition: this.reference.lieu_edition,
        editeur: this.reference.editeur,
        annee: this.reference.annee,
        nb_page: this.reference.nb_page,
        description: this.reference.description,
      };
      console.log(this.$store.state.connectionInfo.token);
      updateBookReference(this.$route.params.id, formData, this.$store.state.connectionInfo.token)
          .then(
              (response) => {
                if(response.data.success) {
                  this.message ="La référence a été mise à jour."
                  console.log("référence livresque mise à jour");
                } else {
                  this.message = "La référence n'a pas pu être mise à jour."
                }
              }
          )
    },
    deleteReference: function() {
        deleteBookReference(this.$route.params.id, this.$store.state.connectionInfo.token)
          .then(
              (response) => {

                if(response.status === 204) {
                  console.log("référence livresque supprimée");
                  this.$router.push("/reference-livre/liste");
                } else {
                  this.message = "La référence n'a pas pu être supprimée."
                }
              }
          )
    },
    // TODO store
    getSuggestedAuthors: function (query) {
      if (query.length >= 2) {
        axios.get("/api/authors/chercher-proches?auteur=:query".replace(":query", query))
            .then((response) => {
              if (response.data.success) {
                this.suggestedAuthors = response.data.suggestedAuthors;
              }
            }).catch();
      }
    },
    // TODO store
    addAuthor: function(event) {
      this.selectedAuthorId = event;
      this.selectedAuthors.push(event);
      this.author_query = "";
    },
    removeSelectedAuthor: function() {
      this.selectedAuthors = this.selectedAuthors.filter(
          (author) => {
            return author.value !== this.selectedAuthorId;
          }
      );
      this.selectedAuthorId = '';
    }
  },
  mounted() {
    this.getReference();
  },
  watch: {
    author_query: function (newValue) {
      this.getSuggestedAuthors(newValue);
    },
    selectedAuthors: function (newValue) {
      if(newValue.length > 1) {
        this.selectedAuthorsMessage = "Auteurs sélectionnés"
      } else {
        this.selectedAuthorsMessage = "Auteur sélectionné"
      }
    }
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