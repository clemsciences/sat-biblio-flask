<template>
  <div>
    <h2>Nouvel auteur</h2>
    <b-form @submit.prevent="onSubmit">
      <b-form-group label="Prénom">
        <b-form-input type="text" v-model="first_name"></b-form-input>
      </b-form-group>
      <b-form-group label="Nom">
        <b-form-input type="text" v-model="family_name"></b-form-input>
      </b-form-group>
      <b-button type="submit">Valider</b-button>
    </b-form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Auteur",
  data: function () {
    return {
      first_name: '',
      family_name: ''
    };
  },
  methods: {
    onSubmit: function() {
      const form_data = {first_name: this.first_name, family_name: this.family_name};
      axios.post('/api/auteur/creer', form_data).then(
          (response) => {
            if(response.data.success) {
              console.log("ok");
            }
          }
      ).catch(
          (reason => console.log(reason))
      )

    }
  }
}
</script>

<style scoped>

</style>