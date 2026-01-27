<template>
  <b-container>
    <Title title="Notes de version" info="Historique des modifications du projet SAT-Biblio."/>

    <b-row v-if="loading" class="justify-content-center my-5">
      <b-spinner label="Chargement des notes de version..."></b-spinner>
    </b-row>

    <b-row v-if="error" class="justify-content-center my-5 text-danger">
      <p>{{ error }}</p>
      <b-button variant="outline-primary" @click="fetchReleases" class="ml-3">Réessayer</b-button>
    </b-row>

    <div v-if="!loading && !error">
      <b-card v-for="release in releases" :key="release.id" class="mb-4 shadow-sm">
        <template #header>
          <div class="d-flex justify-content-between align-items-center">
            <h3 class="mb-0">{{ release.name || release.tag_name }}</h3>
            <b-badge variant="info">{{ formatDate(release.published_at) }}</b-badge>
          </div>
        </template>

        <b-card-text>
          <div class="release-body" v-html="renderMarkdown(release.body)"></div>
        </b-card-text>

        <template #footer>
          <div class="d-flex justify-content-between align-items-center">
            <small class="text-muted">Tag: {{ release.tag_name }}</small>
            <b-button :href="release.html_url" target="_blank" variant="outline-secondary" size="sm">
              Voir sur GitHub <b-icon icon="box-arrow-up-right" class="ml-1"/>
            </b-button>
          </div>
        </template>
      </b-card>
    </div>
  </b-container>
</template>

<script>
import Title from "@/components/visuel/Title.vue";
import axios from "axios";
import { marked } from "marked";

export default {
  name: "ChangelogView",
  components: { Title },
  data() {
    return {
      releases: [],
      loading: true,
      error: null
    };
  },
  mounted() {
    this.fetchReleases();
  },
  methods: {
    async fetchReleases() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get("https://api.github.com/repos/clemsciences/sat-biblio-flask/releases");
        this.releases = response.data;
      } catch (err) {
        console.error("Erreur lors de la récupération des releases GitHub:", err);
        this.error = "Impossible de charger les notes de version depuis GitHub.";
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateString) {
      if (!dateString) return "";
      const date = new Date(dateString);
      return date.toLocaleDateString("fr-FR", {
        year: "numeric",
        month: "long",
        day: "numeric"
      });
    },
    renderMarkdown(text) {
      if (!text) return "";
      return marked(text);
    }
  }
};
</script>

<style scoped>
.release-body {
  text-align: left;
  line-height: 1.6;
}
.release-body h3, .release-body h4, .release-body h5 {
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  color: #005db6;
}
.release-body pre {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  border: 1px solid #dee2e6;
  overflow-x: auto;
}
.release-body code {
  color: #d63384;
  word-wrap: break-word;
}
.release-body pre code {
  color: inherit;
  word-wrap: normal;
}
.release-body ul {
  padding-left: 1.5rem;
  margin-bottom: 1rem;
}
</style>
