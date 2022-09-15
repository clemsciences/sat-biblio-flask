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
      <b-form-group v-if="!connected" label="Donnez votre adresse email pour recevoir une copie de votre message.">
        <b-form-input v-model="emailAddress"/>
      </b-form-group>
      <b-form-group label="Quelle est la somme de sept et de trois ? Donnez le résultat en chiffre.">
        <b-form-input v-model="theSum"/>
      </b-form-group>
      <b-button type="submit" :disabled="isIncorrect">Envoyer</b-button>
      <span class="mx-3">{{ message }}</span>
    </b-form>
  </div>
</template>

<script>
import {sendMessageToAdmin} from "@/services/api";
import Title from "./visuel/Title";
import {mapState} from "vuex";

export default {
  name: "Contact",
  components: {Title},
  data: function () {
    return {
      emailAddress: "",
      textToSend: "",
      message: "",
      theSum: 0
    }
  },
  methods: {
    sendMessage: function () {
      sendMessageToAdmin(this.textToSend, this.theSum, this.emailAddress).then(
        (response) => {
          if(response.data.success) {
            console.log("message correctement envoyé");
            this.textToSend = "";
            if(this.connected || this.emailAddress.length > 0) {
              this.message = "Le message a été envoyé. Vous recevrez aussi une copie du message que vous avez envoyé."
            } else {
              this.message = "Le message a été envoyé."
            }
          } else {
            if(response.data.mistake) {
              this.message = "Le résultat du calcul est incorrect. Veuillez corriger le résultat pour envoyer le message."
            } else {
              console.log("message non envoyé");
              this.message = "Le message n'a pas pu être envoyé. L'administrateur du site corrigera l'erreur."
            }
          }
        });
    }
  },
  computed: {
    ...mapState(["connected", "connectionInfo"]),
    isIncorrect: function () {
      return this.textToSend.length === 0;
    },
  }
}
</script>

<style scoped>

</style>