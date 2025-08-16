<template>
  <b-container>
    <Title title="Nouvel auteur"
           info="Un auteur est un individu qui a participé à la rédaction d'au moins un ouvrage."
           id="id-auteur"/>
    <AuteurFormulaire
        :auteur="auteur"
        :on-submit="onSubmit"
        :message="message"/>

<!--    <AuthorCheck v-model="auteur" :disabled="false"/>-->

    <div v-if="this.auteur.first_name.trim().length >= 1 || this.auteur.family_name.trim().length >= 1">

      <div v-if="exactMatching">
        <p>L'auteur <b>{{auteur.first_name}}</b> <b>{{auteur.family_name}}</b> existe déjà.</p>
      </div>
      <div v-else-if="this.auteur.first_name.trim().length === 0">
        <p>Un auteur doit obligatoirement avoir un prénom non vide.</p>
      </div>
      <div v-else-if="this.auteur.family_name.trim().length === 0">
        <p>Un auteur doit obligatoirement avoir un nom de famille non vide.</p>
      </div>
      <div v-else>
        <p>C'est un nouvel auteur.</p>
      </div>
      <div v-if="suggested.length > 0">
      <b-table striped bordered hover :items="suggested" :fields="fields"
             primary-key="id" >
        <template #table-caption>Correspondances possibles</template>
      </b-table>
<!--      <div v-for="value in suggested" :key="value.value">-->
<!--        <p>{{ value.first_name }} {{ value.family_name }}</p>-->
<!--      </div>-->

<!--        <p>{{suggested}}</p>-->
      </div>
    </div>






  </b-container>
</template>

<script>
import {createAuthor, searchNearAuthors} from "@/services/api";
import Title from "../visuel/Title";
import AuteurFormulaire from "@/components/auteur/AuteurFormulaire";
import {canManage} from "@/services/rights";
import {Author} from "@/services/objectManager";
// import AuthorCheck from "@/components/auteur/AuthorCheck.vue";

export default {
  name: "Auteur",
  components: {AuteurFormulaire, Title},
  data: function () {
    return {
      auteur: new Author(),
      message: '',
      suggested: [],
      exactMatching: false,
      fields: [
        {
          key: 'first_name',
          label: 'Prénom',
          sortable: false
        },
        {
          key: 'family_name',
          label: 'Nom de famille',
          sortable: false
        }
      ],
    };
  },
  mounted() {
    this.auteur.validated = this.isManager;
  },
  methods: {
    onSubmit: function() {
      if (this.auteur.first_name.trim().length > 0 && this.auteur.family_name.trim().length > 0) {
        createAuthor(this.auteur, this.$store.state.connectionInfo.token).then(
            (response) => {
              if (response.data.success) {
                this.message = `L'auteur ${this.auteur.first_name} ${this.auteur.family_name} a été correctement créé.`;
                this.auteur.clear();
              } else {
                this.message = "Impossible de sauvegarder l'auteur."
              }
            }
        ).catch(
            (reason => {
              if(reason.response.data && reason.response.data.message) {
                this.message = reason.response.data.message
              } else {
                this.message = "Il y a une erreur réseau."
              }
            })
        );
      } else if(this.auteur.first_name.length === 0) {
        this.message = "Le prénom ne peut être vide.";
      } else if (this.auteur.family_name.length === 0) {
        this.message = "Le nom de famille ne peut être vide.";
      }
    },
    checkAuthorExistence() {
      if (this.auteur.first_name.trim().length >= 2 || this.auteur.family_name.trim().length >= 2) {
        searchNearAuthors(`first_name=${encodeURIComponent(this.auteur.first_name.trim())}&family_name=${encodeURIComponent(this.auteur.family_name.trim())}`).then(
            (response) => {
              if (response.data.success) {
                this.suggested = response.data.suggestedAuthors;
                this.exactMatching = response.data.exactMatching;
              } else {
                this.exactMatching = false;
              }
            }
        ).catch(
            (reason => {
              if (reason.response.data && reason.response.data.message) {
                this.message = reason.response.data.message
              } else {
                this.message = "Il y a une erreur réseau."
              }
            })
        );
      } else {
        this.suggested = [];
      }
    }

  },
  computed: {
    isManager: function() {
      return canManage(this.$store.getters.getUserRight);
    },

  },
  watch: {
    auteur: {
      handler() {
        // console.log(newValue);
        // let query = "";
        // console.log("youhou")
        // if(newValue.first_name) {
        //   query = newValue.first_name;
        // }
        // if(newValue.family_name) {
        //   if(query) {
        //     query += " ";
        //   }
        //   query += newValue.family_name;
        // }
        // this.authorQuery = query;
        this.checkAuthorExistence();
      },
      deep: true
    }
  },

}
</script>

<style scoped>

</style>