<template>
  <div>
    <p>{{ message }}</p>
  </div>
</template>

<script>
import axios from "axios";
import localStorageManager from "@/services/localstorageManager";
export default {
  name: "Deconnexion",
  data: function() {
    return {
      message: "",
    }
  },
  mounted() {
    localStorageManager.removeSessionInfo();
    axios.get("/api/user/disconnect").then(
      (response) => {
        if(response.data.success) {
          this.message = "Vous êtes correctement déconnecté."
        } else {
          this.message = "La déconnexion a échoué."
        }
      }
    );
  }
}
</script>

<style scoped>

</style>