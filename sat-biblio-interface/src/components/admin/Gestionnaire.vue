<template>
  <b-container>
    <Title info="Cette page permet au gestionnaire d'accepter ou de refuser des modifications d'une fiche."
           id="id-gestionnaire">
      Page du gestionnaire
    </Title>
    <div class="accordion" role="tablist">
      <b-row>
        <b-button v-b-toggle.collapse-users>
          Voir les utilisateurs
        </b-button>
      </b-row>
      <b-row class="my-2">
        <b-row role="tab">
          <b-collapse id="collapse-users"
                      accordion="manager-accordion"
                      role="tabpanel">
            <liste-utilisateur/>
          </b-collapse>
        </b-row>
      </b-row>
      <b-row>
        <b-button v-b-toggle.collapse-non-approved-entries >
              Voir les entrées non approuvées
        </b-button>
      </b-row>

      <b-row class="my-2">
        <b-row role="tab">
          <b-collapse id="collapse-non-approved-entries"
                      accordion="manager-accordion"
                      role="tabpanel">
            <liste-auteurs-non-approuves/>
            <liste-references-non-approuvees/>
            <liste-enregistrements-non-approuves/>
        </b-collapse>
        </b-row>

      </b-row>
    </div>

  </b-container>
</template>

<script>
import Title from "../visuel/Title";
import ListeUtilisateur from "@/components/admin/ListeUtilisateur";
import ListeAuteursNonApprouves from "@/components/admin/ListeAuteursNonApprouves";
import ListeReferencesNonApprouvees from "@/components/admin/ListeReferencesNonApprouvees";
import ListeEnregistrementsNonApprouves from "@/components/admin/ListeEnregistrementsNonApprouves";
export default {
name: "Gestionnaire",
  components: {
    ListeEnregistrementsNonApprouves,
    ListeReferencesNonApprouvees,
    ListeAuteursNonApprouves, Title, ListeUtilisateur},
  data: function () {
    return {

    }
  },

}
</script>

<style scoped>

</style>