<template>
  <div>
    <h2>Contacter</h2>

    <b-form @submit.prevent="sendMessage">
      <b-form-group label="Message à envoyer à l'administrateur de SatBiblio">
        <b-form-textarea v-model="message" rows="10"/>
      </b-form-group>
      <b-button type="submit">Envoyer</b-button>
    </b-form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Contact",
  data: function () {
    return {
      message: ""
    }
  },
  methods: {
    sendMessage: function () {
      axios.post('/api/contact/send-message', {
        message: this.message
      }).then(
          (response) => {
            if(response.data.success) {
              console.log("message correctement envoyé");
              this.message = "Le message a été envoyé."
            } else {
              console.log("message non envoyé");
              this.message = "Le message n'a pas pu être envoyé."
            }
          }
      )
    }
  }
}
</script>

<style scoped>

</style>