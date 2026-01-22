<template>
  <b-container>
    <Title info="Liste des mots clefs définis dans les enregistrements du catalogue.">
      Mots clefs
    </Title>
    <b-row class="mt-4">
      <b-col lg="12">
        <b-form-group label="Trier par :">
          <b-form-radio-group
            v-model="sortBy"
            :options="sortOptions"
            name="radio-sorting"
          ></b-form-radio-group>
        </b-form-group>
      </b-col>
    </b-row>
    <b-row class="mt-2">
      <b-col lg="12">
        <div class="d-flex flex-wrap">
          <b-button
            v-for="keyword in sortedKeywords"
            :key="keyword.text"
            variant="outline-primary"
            class="m-1"
            @click="goToRecords(keyword.text)"
          >
            {{ keyword.text }} <b-badge v-if="sortBy === 'frequency'" variant="light">{{ keyword.count }}</b-badge>
          </b-button>
        </div>
      </b-col>
    </b-row>
    <b-row v-if="loading" class="justify-content-center mt-4">
      <b-spinner label="Chargement..."></b-spinner>
    </b-row>
    <b-row v-if="error" class="justify-content-center mt-4 text-danger">
      {{ error }}
    </b-row>
  </b-container>
</template>

<script>
import { getBookRecordsKeywords } from "@/services/api";
import Title from "../visuel/Title";

export default {
  name: "ListeMotsClefs",
  components: { Title },
  data() {
    return {
      keywords: [],
      loading: false,
      error: null,
      sortBy: "alphabetic",
      sortOptions: [
        { text: "Alphabétique", value: "alphabetic" },
        { text: "Fréquence", value: "frequency" }
      ]
    };
  },
  computed: {
    sortedKeywords() {
      const k = [...this.keywords];
      if (this.sortBy === "alphabetic") {
        return k.sort((a, b) => a.text.localeCompare(b.text));
      } else if (this.sortBy === "frequency") {
        return k.sort((a, b) => b.count - a.count || a.text.localeCompare(b.text));
      }
      return k;
    }
  },
  mounted() {
    if (this.$route.query.sort && this.sortOptions.some(opt => opt.value === this.$route.query.sort)) {
      this.sortBy = this.$route.query.sort;
    }
    this.fetchKeywords();
  },
  watch: {
    sortBy(newVal) {
      if (this.$route.query.sort !== newVal) {
        this.$router.replace({
          query: { ...this.$route.query, sort: newVal }
        }).catch(err => {
          if (err.name !== 'NavigationDuplicated') {
            console.error(err);
          }
        });
      }
    }
  },
  methods: {
    fetchKeywords() {
      this.loading = true;
      getBookRecordsKeywords()
        .then(response => {
          if (response.data.success) {
            this.keywords = response.data.keywords;
          } else {
            this.error = "Erreur lors de la récupération des mots clefs.";
          }
        })
        .catch(err => {
          console.error(err);
          this.error = "Erreur lors de la récupération des mots clefs.";
        })
        .finally(() => {
          this.loading = false;
        });
    },
    goToRecords(keyword) {
      this.$router.push({
        name: "enregistrement-liste",
        query: { mot_clef: keyword }
      });
    }
  }
};
</script>

<style scoped>
.flex-wrap {
  gap: 10px;
}
</style>
