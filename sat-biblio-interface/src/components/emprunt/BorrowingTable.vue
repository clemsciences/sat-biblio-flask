<template>
  <b-container>
    <b-row>
    <b-pagination v-model="currentPage"
      :total-rows="borrowings.length"
      :per-page="perPage"
      aria-controls="my-table"/>
    </b-row>
    <b-table striped bordered hover :items="borrowings" :fields="fields"
             primary-key="id" :per-page="perPage" :current-page="currentPage"
             @row-dblclicked="goToBorrowing">
      <template #table-caption>La liste des emprunts dans la base.</template>

      <template #cell(emprunteur)="data">
        {{ data.item.emprunteur.first_name }} {{ data.item.emprunteur.family_name }}
      </template>

      <template #cell(enregistrement)="data">
        {{ data.item.enregistrement.reference.titre }} ({{ data.item.enregistrement.cote}})
      </template>
      <template #cell(gestionnaire)="data">
        {{ data.item.gestionnaire.first_name }} {{ data.item.gestionnaire.family_name}}
      </template>
      <template #cell(rendu)="data">
        <div v-if="data.item.rendu">Oui</div><div v-else>Non</div>
      </template>
      <template #cell(emprunte)="data">
        <div v-if="data.item.emprunte">Oui</div><div v-else>Non</div>
      </template>
      <template #cell(date_emprunt)="data">
        {{ fromISOtoFrenchDateFormat(data.item.date_emprunt) }}
      </template>
      <template #cell(date_retour_prevu)="data">
        {{ fromISOtoFrenchDateFormat(data.item.date_retour_prevu) }}
      </template>
      <template #cell(date_retour_reel)="data">
        {{ fromISOtoFrenchDateFormat(data.item.date_retour_reel) }}
      </template>
    </b-table>
  </b-container>
</template>

<script>
export default {
  name: "BorrowingTable",
  props: {
    perPage: {
      type: Number,
      default: 10,
    },
    borrowings: {
      type: Array
    },
  },
  data: function() {
    return {
      currentPage: 0,
      fields: [
        {
          key: "enregistrement",
          label: "Livre",
          sortable: false
        },
        {
          key: "date_emprunt",
          label: "Date d'emprunt",
          sortable: false
        },{
          key: "emprunte",
          label: "Emprunté ?",
          sortable: false
        },{
          key: "rendu",
          label: "Rendu ?",
          sortable: false
        },
          {
          key: "date_retour_prevu",
          label: "Date de retour prévu",
          sortable: false
        },{
          key: "date_retour_reel",
          label: "Date de retour réel",
          sortable: false
        },
        {
          key: "emprunteur",
          label: "Emprunteur",
          sortable: false
        },{
          key: "gestionnaire",
          label: "Gestionnaire",
          sortable: false
        },
        {
          key: "comment",
          label: "Commentaire",
          sortable: false
        },
      ]
    };
  },
  methods: {
    goToBorrowing(item) {
      this.$router.push(`/emprunt/${item.id}`);
    },
    fromISOtoFrenchDateFormat(isoDate) {
      if(typeof isoDate !== "undefined") {
        const l = isoDate.split("-");
        if(l.length === 3) {
          return `${l[2]}/${l[1]}/${l[0]}`;
        }
      }
      return "";
    }
  }
}
</script>

<style scoped>

</style>