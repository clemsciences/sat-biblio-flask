<template>
  <BForm @submit.prevent="onSubmit">
    <BFormGroup label="Nom du fichier">
      <BFormInput v-model="filename" :disabled="true"/>
    </BFormGroup>
    <BFormGroup label="Date de debut">
      <BFormInput v-model="startDate" :disabled="true"/>
    </BFormGroup>
    <BFormGroup label="Date de fin">
      <BFormInput v-model="endDate" :disabled="true"/>
    </BFormGroup>
    <BFormGroup label="Description">
      <BFormTextarea v-model="description" :disabled="disabled"/>
    </BFormGroup>
    <BFormGroup label="Etat">
      <BFormTextarea v-model="status" :disabled="disabled"/>
    </BFormGroup>
    <BFormGroup label="Utilisateur">
      <div v-if="importItem.user" >
        <BFormTextarea :value="`${importItem.user.firstName} ${importItem.user.familyName}`" :disabled="true"/>
      </div>
      <div v-else>
        <BFormTextarea v-model="user" :disabled="true"/>
      </div>
    </BFormGroup>
    <BButton type="submit" v-if="!disabled" :disabled="isIncorrect || disabled">Enregistrer</BButton>
    <span class="mx-3">{{ message }}</span>
  </BForm>
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
      type: Boolean,
      default: false
    }
  },
  computed: {
    filename: {
      get() {
        return this.importItem.filename;
      },
      set(value) {
        this.$emit('update:filename', value);
      }
    },
    startDate: {
      get() {
        return this.importItem.startDate;
      },
      set(value) {
        this.$emit('update:startDate', value);
      }
    },
    endDate: {
      get() {
        return this.importItem.endDate;
      },
      set(value) {
        this.$emit('update:endDate', value);
      }
    },
    description: {
      get() {
        return this.importItem.description;
      },
      set(value) {
        this.$emit('update:description', value);
      }
    },
    status: {
      get() {
        return this.importItem.status;
      },
      set(value) {
        this.$emit('update:status', value);
      }
    },
    user: {
      get() {
        return this.importItem.user;
      },
      set(value) {
        this.$emit('update:user', value);
      }
    },
    isIncorrect() {
      return this.importItem.description.length === 0 ||
          this.importItem.filename.length === 0;
    }
  }
}
</script>

<style scoped>

</style>