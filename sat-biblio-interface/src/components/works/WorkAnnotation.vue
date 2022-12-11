<template>
  <b-container>
    <h2>Annotation des ouvrages publiés</h2>
    <b-form-group label="Titre">
      <b-form-input type="text" v-model="updatedData.title" />
    </b-form-group>
    <b-form-group label="Lien">
      <b-form-input type="url" v-model="updatedData.link"/>
    </b-form-group>
    <b-form-group label="Type de publication">
      <b-form-input type="text" v-model="updatedData.publicationType"/>
    </b-form-group>
    <b-form-group label="Année ou numéro">
      <b-form-input type="text" v-model="updatedData.yearOrNumber"/>
    </b-form-group>
<!--    <b-textarea v-model="text" rows="10" max-rows="30"/>-->

    <b-button type="save" @click="save" :disabled="isEqual">Sauver</b-button>
  </b-container>
</template>

<script>
import {getPublishedWork, updatePublishedWork} from "@/services/api";
import {mapState} from "vuex";

export default {
  name: "WorkAnnotation",
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