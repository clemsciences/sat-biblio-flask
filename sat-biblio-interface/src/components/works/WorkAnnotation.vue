<template>
  <BContainer>
    <h2>Annotation des ouvrages publiés</h2>
    <BFormGroup label="Titre">
      <BFormInput type="text" v-model="updatedData.title" />
    </BFormGroup>
    <BFormGroup label="Lien">
      <BFormInput type="url" v-model="updatedData.link"/>
    </BFormGroup>
    <BFormGroup label="Type de publication">
      <BFormInput type="text" v-model="updatedData.publicationType"/>
    </BFormGroup>
    <BFormGroup label="Année ou numéro">
      <BFormInput type="text" v-model="updatedData.yearOrNumber"/>
    </BFormGroup>
<!--    <b-textarea v-model="text" rows="10" max-rows="30"/>-->

    <BButton type="save" @click="save" :disabled="isEqual">Sauver</BButton>
  </BContainer>
</template>

<script>
import {getPublishedWork, updatePublishedWork} from "@/services/api";
import {mapState} from "vuex";

export default {
  name: "WorkAnnotationView",
  data: function() {
    return {
      savedData: {
        link: '',
        title: '',
        text: '',
        publicationType: '',
        yearOrNumber: '',
        workId: parseInt(this.$route.params.id)
      },
      updatedData: {
        link: '',
        title: '',
        text: '',
        publicationType: '',
        yearOrNumber: '',
        workId: parseInt(this.$route.params.id)

      }

    };
  },
  mounted() {
    this.get();
  },
  methods: {
    get() {
      getPublishedWork(parseInt(this.$route.params.id), "").then(
          (value) => {
            let data = value.data;
            if(data.success) {
              console.log(data.result);
              this.savedData.title = data.result.title;
              this.savedData.publicationType = data.result.publication_type;
              this.savedData.yearOrNumber = data.result.year;
              // this.text =;
              // this.link =;

              this.updatedData.title = data.result.title;
              this.updatedData.publicationType = data.result.publication_type;
              this.updatedData.yearOrNumber = data.result.year;
            } else {
              console.error("error while retrieving data");
            }
          }
      );
    },
    save() {
      let publishedWork = {
        year: this.updatedData.yearOrNumber,
        id_: this.updatedData.workId,
        title: this.updatedData.title,
        publication_type: this.updatedData.publicationType
      };

      updatePublishedWork(this.updatedData.workId, publishedWork, this.$store.state.connectionInfo.token, "").then(
          (value) => {
            if(value.data.success) {
              console.log("success");
              console.log(value);
            } else {
              console.error(value);
            }

          }
      );

    }
  },
  computed: {
    ...mapState(["connected", "connectionInfo"]),
    isEqual: function() {
      return this.updatedData.title === this.savedData.title &&
          this.updatedData.yearOrNumber === this.savedData.yearOrNumber &&
          this.updatedData.text === this.savedData.text &&
          this.updatedData.link === this.savedData.link &&
          this.updatedData.publicationType === this.savedData.publicationType;
    }
  }

}
</script>

<style scoped>

</style>