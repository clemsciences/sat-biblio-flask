<template>
  <b-form @submit.prevent="onSubmit">
    <b-form-group label="Nom du fichier">
      <b-form-input v-model="importItem.filename" :disabled="true"/>
    </b-form-group>
    <b-form-group label="Date de debut">
      <b-form-input v-model="importItem.startDate" :disabled="true"/>
    </b-form-group>
    <b-form-group label="Date de fin">
      <b-form-input v-model="importItem.endDate" :disabled="true"/>
    </b-form-group>
    <b-form-group label="Description">
      <b-form-textarea v-model="importItem.description" :disabled="disabled"/>
    </b-form-group>
    <b-form-group label="Etat">
      <b-form-textarea v-model="importItem.status" :disabled="disabled"/>
    </b-form-group>
    <b-form-group label="Utilisateur">
      <div v-if="importItem.user" >
        <b-form-textarea :value="`${importItem.user.firstName} ${importItem.user.familyName}`" :disabled="true"/>
      </div>
      <div v-else>
        <b-form-textarea v-model="importItem.user" :disabled="true"/>
      </div>
    </b-form-group>
    <b-button type="submit" v-if="!disabled" :disabled="isIncorrect || disabled">Enregistrer</b-button>
    <span class="mx-3">{{ message }}</span>
  </b-form>
</template>

<script>

import {ImportItem} from "@/services/objectManager";

export default {
  name: "ImportItemForm",
  components: {},
  props: {
    importItem: {
      type: ImportItem
    },
    message: {
      type: String,
      default: ''
    },
    onSubmit: Function,
    disabled: {
      Boolean,
      default: false
    }
  },
  computed: {
    isIncorrect() {
      return this.importItem.description.length === 0 ||
          this.importItem.filename.length === 0;
    }
  }
}
</script>

<style scoped>

</style>