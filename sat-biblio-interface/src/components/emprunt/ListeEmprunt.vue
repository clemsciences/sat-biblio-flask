<template>
  <b-container>
    <h2>Liste d'emprunts</h2>
    <p>Double-cliquez sur la ligne pour voir les détails sur un emprunt.</p>
<!--    <b-row class="my-1">-->
<!--      <b-col lg="4">-->
<!--        <b-form-group label="Prénom" label-cols-sm="3"-->
<!--          label-align-sm="right" label-size="sm" class="mb-0">-->
<!--          <b-input type="search" v-model="firstNameFiltre"-->
<!--                   placeholder="Filtrer en fonction du prénom"/>-->

<!--        </b-form-group>-->
<!--      </b-col>-->
<!--      <b-col lg="4">-->
<!--        <b-form-group label="Nom de famille" label-cols-sm="3"-->
<!--          label-align-sm="right" label-size="sm" class="mb-0">-->
<!--          <b-input type="search" v-model="familyNameFiltre"-->
<!--                   placeholder="Filtrer en fonction du nom de famille"/>-->
<!--        </b-form-group>-->
<!--      </b-col>-->
<!--    </b-row>-->
    <b-row>
      <b-form-group label="Filtrer par retard" v-slot="{ ariaDescribedby }">
      <b-form-radio-group
        id="radio-group-1"
        v-model="lateStateSelected"
        :options="lateStateOptions"
        :aria-describedby="ariaDescribedby"
      ></b-form-radio-group>
    </b-form-group>

    </b-row>
    <b-row>

    <b-pagination v-model="currentPage"
      :total-rows="borrowingTotalNumber"
      :per-page="perPage"
      aria-controls="my-table"/>
      <filter-count :filtered-item-count="borrowingFilteredNumber" :total-item-count="borrowingTotalNumber"/>

    </b-row>


    <b-table striped bordered hover :items="retrieveBorrowings" :fields="fields"
             primary-key="id" :per-page="perPage" :current-page="currentPage"
             :sort-by="sortBy" @row-dblclicked="goToBorrowing" :filter="onFilter">
      <template #table-caption>La liste des emprunts dans la base.</template>

Object { comment: "Oui", date_emprunt: "2022-01-19", emprunte: true, … }

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

import {getBorrowingsCount, retrieveBorrowings} from "@/services/api";
import FilterCount from "@/components/visuel/FilterCount";

export default {
  name: "ListeEmprunt",
  components: {FilterCount},
  data: function () {
    return {
      borrowings: [],
      currentPage: 1,
      perPage: 10,
      sortBy: "",
      borrowingFilteredNumber: 0,
      borrowingTotalNumber: 0,
      // firstNameFiltre: "",
      // familyNameFiltre: "",
      lateStateSelected: "all",
      lateStateOptions: [
        {text: "En retard", value: "late"},
        {text: "Dans les temps", value: "on_time"},
        {text: "Tous", value: "all"},
      ],
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
    }
  },
  methods: {
    retrieveBorrowings: function(ctx, callback) {
      let params = "?page="+ctx.currentPage+
          "&size="+ctx.perPage+
          "&sortBy="+ctx.sortBy;

      let filterParams = "";
      // if(this.firstNameFiltre.length > 0) {
      //   filterParams = filterParams+"&first_name="+this.firstNameFiltre;
      // }
      // if(this.familyNameFiltre.length > 0) {
      //   filterParams = filterParams+"&family_name="+this.familyNameFiltre;
      // }
      if(this.lateStateSelected === "late") {
        filterParams = filterParams+"&late=true";
      } else if(this.lateStateSelected === "on_time") {
        filterParams = filterParams+"&on_time=true";
      } else if(this.lateStateSelected === "all") {
        filterParams = filterParams+"&all=true";
      }

      if(filterParams.length > 0) {
        params = params + filterParams;
      }
      retrieveBorrowings(params)
          .then(
              (response) => {
                if(response.data.success) {
                  this.currentPage = 1;
                  this.borrowings = response.data.borrowings;
                  this.borrowings = this.borrowings.map((value) => {
                    const a = {
                      ...value,
                      _rowVariant: this.isBorrowingLate(value) ? '' : 'warning'
                    };
                    console.log(a);
                    return a;
                  });
                  callback(this.borrowings);
                }
              }
          ).catch(
          (reason) => {
            console.log(reason)
            callback([]);
          }
      );
      return null;
    },
    getBorrowingsTotalNumber: function() {
      let filterParams = "";
      // if(this.firstNameFiltre.length > 0) {
      //
      //   filterParams = filterParams + "first_name=" + encodeURI(this.firstNameFiltre);
      // }
      // if(this.familyNameFiltre.length > 0) {
      //   if(filterParams.length > 0) {
      //     filterParams = filterParams+"&";
      //   }
      //   filterParams = filterParams + "family_name="+encodeURI(this.familyNameFiltre);
      // }
      if(this.lateStateSelected === "late") {
        if(filterParams.length > 0) {
          filterParams = filterParams+"&";
        }
        filterParams = filterParams+"late=true";
      } else if(this.lateStateSelected === "on_time") {
        if(filterParams.length > 0) {
          filterParams = filterParams+"&";
        }
        filterParams = filterParams+"on_time=true";
      } else if(this.lateStateSelected === "all") {
        if(filterParams.length > 0) {
          filterParams = filterParams+"&";
        }
        filterParams = filterParams+"all=true";
      }
      if(filterParams.length > 0) {
        filterParams = "?" + filterParams;
      }
      getBorrowingsCount(filterParams).then(
          (response) => {
            if(response.data.success) {
              this.borrowingFilteredNumber = response.data.filtered_number;
              this.borrowingTotalNumber = response.data.total;
            }
          }
      )
    },
    goToBorrowing: function(item) {
      console.log(item);
      this.$router.push(`/emprunt/${item.id}`);
    },
    isBorrowingLate(item) {
      if(item.rendu) {
        return true
      }
      const now = new Date();
      const today = `${now.getFullYear()}-${now.getMonth()}-${now.getDay()}`;
      console.log(
          item.date_retour_prevu,
          item.rendu,
          item.date_retour_reel);
      return today < item.date_retour_prevu;
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
  },
  mounted() {
    this.getBorrowingsTotalNumber();
  },
  computed: {
    onFilter: function() {
      return `${this.lateStateSelected}`;
      // return `${this.firstNameFiltre} ${this.familyNameFiltre}-${this.lateStateSelected}`;
    }
  },
  watch: {
    // firstNameFiltre: function() {
    //   this.getBorrowingsTotalNumber();
    //   this.currentPage = 1;
    // },
    // familyNameFiltre: function() {
    //   this.getBorrowingsTotalNumber();
    //   this.currentPage = 1;
    // },
    lateStateSelected: function() {
      this.getBorrowingsTotalNumber();
      this.currentPage = 1;
    }
  }
}
</script>

<style scoped>

</style>