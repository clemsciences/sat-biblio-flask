<template>
  <div>
    <AppTitle info="Ce formulaire permet d'envoyer un courriel à l'administrateur de cette application web."
           id="id-contact">
      Contacter l'administrateur
    </AppTitle>

    <BForm @submit.prevent="sendMessage">
      <BFormGroup label="Message à envoyer à l'administrateur de SatBiblio">
        <BFormTextarea v-model="textToSend" rows="10"/>
      </BFormGroup>
      <BFormGroup v-if="!connected" label="Donnez votre adresse email pour recevoir une copie de votre message.">
        <BFormInput v-model="emailAddress"/>
      </BFormGroup>
      <!-- Champ piège : invisible pour les humains, rempli par les robots. -->
      <div class="honeypot" aria-hidden="true">
        <label for="contact-website">Site web</label>
        <input id="contact-website" v-model="website" type="text" name="website"
               tabindex="-1" autocomplete="off"/>
      </div>
      <BButton type="submit" :disabled="isIncorrect">Envoyer</BButton>
      <span class="mx-3">{{ message }}</span>
    </BForm>
  </div>
</template>

<script>
import {sendMessageToAdmin} from "@/services/api.js";
import AppTitle from "@/components/visuel/AppTitle.vue";
import {mapState} from "vuex";

export default {
  name: "ContactView",
  components: {AppTitle},
  data: function () {
    return {
      emailAddress: "",
      textToSend: "",
      message: "",
      website: "",
      startedAt: Date.now()
    }
  },
  methods: {
    sendMessage: function () {
      const elapsedSeconds = Math.round((Date.now() - this.startedAt) / 1000);
      sendMessageToAdmin(this.textToSend, this.emailAddress, this.website, elapsedSeconds).then(
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
              this.message = "Le message a été envoyé trop vite. Merci de patienter quelques secondes avant de réessayer."
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
/* Hors écran plutôt que display: none, que certains robots savent ignorer. */
.honeypot {
  position: absolute;
  left: -10000px;
  width: 1px;
  height: 1px;
  overflow: hidden;
}
</style>