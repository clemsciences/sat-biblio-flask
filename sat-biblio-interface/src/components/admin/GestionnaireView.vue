<template>
  <BContainer>
    <AppTitle info="Cette page permet au gestionnaire d'accepter ou de refuser des modifications d'une fiche."
           id="id-gestionnaire">
      Page du gestionnaire
    </AppTitle>
    <div class="accordion" role="tablist">
      <BRow>
        <BButton v-b-toggle.collapse-users>
          Voir les utilisateurs
        </BButton>
      </BRow>
      <BRow class="my-2">
        <BRow role="tab">
          <BCollapse id="collapse-users"
                      visible
                      accordion="manager-accordion"
                      role="tabpanel">
            <ListeUtilisateurs/>
          </BCollapse>
        </BRow>
      </BRow>
      <BRow>
        <BButton v-b-toggle.collapse-non-approved-entries>
              Voir les entrées non approuvées
        </BButton>
      </BRow>

      <BRow class="my-2">
        <BRow role="tab">
          <BCollapse id="collapse-non-approved-entries"
                      accordion="manager-accordion"
                      role="tabpanel">
            <ListeAuteursNonApprouves/>
            <ListeReferencesNonApprouvees/>
            <ListeEnregistrementsNonApprouves/>
        </BCollapse>
        </BRow>

      </BRow>
    </div>

  </BContainer>
</template>

<script>
import AppTitle from "@/components/visuel/AppTitle.vue";
import ListeAuteursNonApprouves from "@/components/admin/ListeAuteursNonApprouves.vue";
import ListeReferencesNonApprouvees from "@/components/admin/ListeReferencesNonApprouvees.vue";
import ListeEnregistrementsNonApprouves from "@/components/admin/ListeEnregistrementsNonApprouves.vue";
export default {
name: "GestionnaireView",
  components: {
    ListeEnregistrementsNonApprouves,
    ListeReferencesNonApprouvees,
    ListeAuteursNonApprouves, AppTitle},
  data: function () {
    return {

    }
  },

}
</script>

<style scoped>

</style>