<template>
  <div>
    <b-form>
      <b-form-group>
        <b-form-input v-model="titre"/>
      </b-form-group>
      <b-form-group>
        <b-form-input v-model="lieu_edition"/>
      </b-form-group>
      <b-form-group>
        <b-form-input v-model="editeur"/>
      </b-form-group>
      <b-form-group>
        <b-form-input v-model="annee"/>
      </b-form-group>
      <b-form-group>
        <b-form-input v-model="nb_pages"/>
      </b-form-group>
    </b-form>
  </div>
</template>

<script>
export default {
name: "LireReferenceLivre",
  data: function () {
    return {
      titre: "",
      lieu_edition: "",
      editeur: "",
      annee: "",
      nb_pages: ""
    }
  },
}
</script>

<style scoped>

</style>