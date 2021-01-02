<template>
  <div>
    <label>Description</label>
      <b-form-textarea :value="description"/>
      <label>Cote</label>
      <b-form-input :value="cote"/>
      <label>Année</label>
      <b-form-input :value="annee"/>
      <label>Nombre d'exemplaires supplémentaires</label>
      <b-form-input :value="nb_exemplaire_supp"/>
      <label>Provenance</label>
      <b-form-input :value="provenance"/>
      <label>Mots-clef</label>
      <b-form-input :value="mots_clef"/>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LireEnregistrement",
  props: ["id"],
  data: function () {
    return {
      description: "",
      cote: "",
      annee: "",
      nb_exemplaire_supp: 0,
      provenance: "",
      mots_clef: "",
      validated: false
    }
  },
  methods: {
    load: function() {
      axios.get('/api/enregistrement/lire/'+this.id).then(
          (value) => {
            if(value.data.result) {
              this.description = value.data.description;
              this.cote = value.data.cote;
              this.annee = value.data.annee;
              this.nb_exemplaire_supp = value.data.nb_exemplaire_supp;
              this.provenance = value.data.provenance;
              this.mots_clef = value.data.mots_clef;
              this.validated = value.data.validated;
            }
          }
      )
    }
  }
}
</script>

<style scoped>

</style>