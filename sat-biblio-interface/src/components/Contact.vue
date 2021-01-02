<template>
  <div>
    <h2>Contacter</h2>
    Message à envoyer à l'administrateur de SatBiblio

    <b-form>
      <b-form-textarea :value="message"></b-form-textarea>
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
            if(response.data.result) {
              console.log("message correctement envoyé");
            } else {
              console.log("message non envoyé");
            }
          }
      )
    }
  }
}
</script>

<style scoped>

</style>