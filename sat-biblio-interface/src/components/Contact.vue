<template>
  <div>
    <Title info="Ce formulaire permet d'envoyer un courriel à l'administrateur de cette application web."
           id="id-contact">
      Contacter l'administrateur
    </Title>

    <b-form @submit.prevent="sendMessage">
      <b-form-group label="Message à envoyer à l'administrateur de SatBiblio">
        <b-form-textarea v-model="textToSend" rows="10"/>
      </b-form-group>
      <b-button type="submit" :disabled="isIncorrect">Envoyer</b-button>
      <span class="mx-3">{{ message }}</span>
    </b-form>
  </div>
</template>

<script>
import {sendMessageToAdmin} from "../services/api";
import Title from "./visuel/Title";

export default {
  name: "Contact",
  components: {Title},
  data: function () {
    return {
      textToSend: "",
      message: ""
    }
  },
  methods: {
    sendMessage: function () {
      sendMessageToAdmin(this.textToSend).then(
        (response) => {
          if(response.data.success) {
            console.log("message correctement envoyé");
            this.textToSend = "";
            this.message = "Le message a été envoyé. Vous recevrez aussi une copie du message que vous avez envoyé."
          } else {
            console.log("message non envoyé");
            this.message = "Le message n'a pas pu être envoyé."
          }
        });
    }
  },
  computed: {
    isIncorrect: function () {
      return this.textToSend.length === 0;
    }
  }
}
</script>

<style scoped>

</style>