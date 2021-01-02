<template>
  <div>
    <h2>Liste d'emprunts</h2>
    <b-list-group>
      <b-list-group-item :key="borrow.id" v-for="borrow in borrows">
        {{ borrow.emprunteur }}
        {{ borrow.enregistrement }}
        {{ borrow.commentaire }}
        {{ borrow.gestionnaire }}
        {{ borrow.emprunte }}
        {{ borrow.date_retour_prevu }}
        {{ borrow.date_retour_reel }}
        {{ borrow.rendu }}
      </b-list-group-item>
    </b-list-group>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ListeEmprunt",
  data: function () {
    return {
      borrows: []
    }
  },
  methods: {
    retrieveBorrows: function() {
      axios.get("/api/emprunt/liste")
          .then(
              (response) => {
                if(response.data.success) {
                  this.borrows = response.data.borrows;
                }
              }
          )
          .catch(
          (reason => console.log(reason))
      );
    }
  },
  mounted() {
    this.retrieveBorrows();
  }

}
</script>

<style scoped>

</style>