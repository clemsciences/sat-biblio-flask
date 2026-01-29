<template>
  <b-container>
    <Title info="Cette page permet de fusionner deux auteurs qui sont des doublons."
           id="id-merge-authors">
      Fusionner des auteurs
    </Title>

    <b-card v-if="duplicateAuthors.length > 1" title="Homonymes potentiels" class="mb-3">
      <p>Voici les auteurs ayant le même nom de famille. Vous pouvez les sélectionner pour la fusion.</p>
      <b-table striped hover :items="duplicateAuthors" :fields="duplicateFields">
        <template #cell(name)="data">
          {{ data.item.first_name }} {{ data.item.family_name }}
        </template>
        <template #cell(actions)="data">
          <b-button size="sm" variant="info" class="mr-1" @click="setAsAuthor1(data.item)">
            Auteur 1
          </b-button>
          <b-button size="sm" variant="info" @click="setAsAuthor2(data.item)">
            Auteur 2
          </b-button>
          <b-button size="sm" variant="outline-primary" class="ml-1" @click="viewAuthor(data.item.id)">
            Voir
          </b-button>
        </template>
      </b-table>
    </b-card>

    <b-card title="Sélection des auteurs">
      <b-button size="sm" variant="outline-secondary" @click="fetchAllDuplicates" class="mb-3">
        Chercher tous les homonymes de la base
      </b-button>
      <b-row>
        <b-col md="6">
          <h5>Premier auteur</h5>
          <b-form-group label="Rechercher l'auteur 1">
            <vue-typeahead-bootstrap
              v-model="query1"
              :data="suggestions1"
              :serializer="s => s.text"
              placeholder="Tapez le nom de l'auteur"
              @hit="selectAuthor1($event)"
            />
          </b-form-group>
          <div v-if="author1">
            <p><strong>Sélectionné :</strong> {{ author1.text }} (ID: {{ author1.value }})</p>
            <b-button size="sm" variant="outline-primary" @click="viewAuthor(author1.value)" class="mb-2">
              Voir la fiche de l'auteur
            </b-button>
            <div v-if="books1.length > 0">
              <h6>Livres associés :</h6>
              <ul>
                <li v-for="book in books1" :key="book.id">
                  <a href="#" @click.prevent="viewBook(book.id)">{{ book.description }}</a>
                </li>
              </ul>
            </div>
            <p v-else-if="loadingBooks1">Chargement des livres...</p>
            <p v-else>Aucun livre associé.</p>
          </div>
        </b-col>
        <b-col md="6">
          <h5>Deuxième auteur</h5>
          <b-form-group label="Rechercher l'auteur 2">
            <vue-typeahead-bootstrap
              v-model="query2"
              :data="suggestions2"
              :serializer="s => s.text"
              placeholder="Tapez le nom de l'auteur"
              @hit="selectAuthor2($event)"
            />
          </b-form-group>
          <div v-if="author2">
            <p><strong>Sélectionné :</strong> {{ author2.text }} (ID: {{ author2.value }})</p>
            <b-button size="sm" variant="outline-primary" @click="viewAuthor(author2.value)" class="mb-2">
              Voir la fiche de l'auteur
            </b-button>
            <div v-if="books2.length > 0">
              <h6>Livres associés :</h6>
              <ul>
                <li v-for="book in books2" :key="book.id">
                  <a href="#" @click.prevent="viewBook(book.id)">{{ book.description }}</a>
                </li>
              </ul>
            </div>
            <p v-else-if="loadingBooks2">Chargement des livres...</p>
            <p v-else>Aucun livre associé.</p>
          </div>
        </b-col>
      </b-row>
    </b-card>

    <b-card v-if="author1 && author2" title="Action" class="mt-3">
      <p>Lequel souhaitez-vous <strong>conserver</strong> ? L'autre sera supprimé et ses références seront rattachées à celui conservé.</p>
      <b-form-group>
        <b-form-radio v-model="idKeep" :value="author1.value">{{ author1.text }}</b-form-radio>
        <b-form-radio v-model="idKeep" :value="author2.value">{{ author2.text }}</b-form-radio>
      </b-form-group>

      <b-button variant="danger" :disabled="!idKeep || loading" @click="confirmMerge">
        <b-spinner small v-if="loading"></b-spinner>
        Fusionner les auteurs
      </b-button>
    </b-card>

    <b-alert v-if="message" :variant="messageVariant" show class="mt-3" dismissible @dismissed="message=''">
      {{ message }}
    </b-alert>

    <b-modal id="modal-confirm-merge" title="Confirmer la fusion" @ok="doMerge">
      <p v-if="authorToKeep && authorToDelete">
        Êtes-vous sûr de vouloir fusionner ces auteurs ?<br>
        L'auteur <strong>{{ authorToKeep.text }}</strong> sera conservé.<br>
        L'auteur <strong>{{ authorToDelete.text }}</strong> sera <strong>supprimé</strong> et ses références seront transférées.
      </p>
      <p class="text-danger">Cette action est irréversible.</p>
    </b-modal>
  </b-container>
</template>

<script>
import Title from "../visuel/Title";
import {searchNearAuthors, mergeAuthors, getEntryListAssociatedToAuthor, searchAuthors, getAuthorDuplicates} from "@/services/api";

export default {
  name: "MergeAuthors",
  components: {Title},
  data() {
    return {
      query1: '',
      query2: '',
      suggestions1: [],
      suggestions2: [],
      author1: null,
      author2: null,
      books1: [],
      books2: [],
      loadingBooks1: false,
      loadingBooks2: false,
      duplicateAuthors: [],
      idKeep: null,
      loading: false,
      message: '',
      messageVariant: 'info',
      duplicateFields: [
        { key: 'name', label: 'Nom complet' },
        { key: 'id', label: 'ID' },
        { key: 'actions', label: 'Actions' }
      ]
    }
  },
  computed: {
    authorToKeep() {
      if (this.idKeep === this.author1?.value) return this.author1;
      if (this.idKeep === this.author2?.value) return this.author2;
      return null;
    },
    authorToDelete() {
      if (this.idKeep === this.author1?.value) return this.author2;
      if (this.idKeep === this.author2?.value) return this.author1;
      return null;
    }
  },
  methods: {
    getSuggestions(query, target) {
      if (query.length >= 2) {
        searchNearAuthors(`auteur=${encodeURIComponent(query)}`)
          .then((response) => {
            if (response.data.success) {
              this[target] = response.data.suggestedAuthors;
            }
          }).catch();
      }
    },
    selectAuthor1(event) {
      this.author1 = event;
      this.fetchBooks1(event.value);
      this.fetchDuplicates(event.family_name);
    },
    selectAuthor2(event) {
      this.author2 = event;
      this.fetchBooks2(event.value);
      this.fetchDuplicates(event.family_name);
    },
    setAsAuthor1(author) {
      const event = {
        text: `${author.first_name} ${author.family_name}`,
        value: author.id,
        family_name: author.family_name,
        first_name: author.first_name
      };
      this.query1 = event.text;
      this.selectAuthor1(event);
    },
    setAsAuthor2(author) {
      const event = {
        text: `${author.first_name} ${author.family_name}`,
        value: author.id,
        family_name: author.family_name,
        first_name: author.first_name
      };
      this.query2 = event.text;
      this.selectAuthor2(event);
    },
    fetchDuplicates(familyName) {
      if (familyName && familyName !== "[collectif]" && familyName !== "[anonyme]") {
        searchAuthors({family_name: familyName})
          .then(response => {
            if (response.data.success) {
              this.duplicateAuthors = response.data.results;
            }
          })
          .catch(error => console.error(error));
      } else {
        this.duplicateAuthors = [];
      }
    },
    fetchAllDuplicates() {
      this.loading = true;
      getAuthorDuplicates(this.$store.state.connectionInfo.token)
        .then(response => {
          if (response.data.success) {
            // response.data.duplicates is a list of {family_name, authors: []}
            // We want to flatten it or just show them.
            // For now, let's just take all authors from all groups.
            const all = [];
            response.data.duplicates.forEach(group => {
              all.push(...group.authors);
            });
            this.duplicateAuthors = all;
          }
        })
        .catch(error => {
          console.error(error);
          this.message = "Erreur lors de la récupération des homonymes.";
          this.messageVariant = "danger";
        })
        .finally(() => {
          this.loading = false;
        });
    },
    fetchBooks1(id) {
      this.loadingBooks1 = true;
      getEntryListAssociatedToAuthor(id, "type=reference")
        .then(response => {
          if (response.data.success) {
            this.books1 = response.data.entries;
          }
        })
        .finally(() => {
          this.loadingBooks1 = false;
        });
    },
    fetchBooks2(id) {
      this.loadingBooks2 = true;
      getEntryListAssociatedToAuthor(id, "type=reference")
        .then(response => {
          if (response.data.success) {
            this.books2 = response.data.entries;
          }
        })
        .finally(() => {
          this.loadingBooks2 = false;
        });
    },
    viewAuthor(id) {
      let routeData = this.$router.resolve(`/auteur/lire/${id}`);
      window.open(routeData.href, '_blank');
    },
    viewBook(id) {
      let routeData = this.$router.resolve(`/reference-livre/lire/${id}`);
      window.open(routeData.href, '_blank');
    },
    confirmMerge() {
      this.$bvModal.show('modal-confirm-merge');
    },
    doMerge() {
      this.loading = true;
      const idDelete = this.idKeep === this.author1.value ? this.author2.value : this.author1.value;
      const token = this.$store.getters.getConnectionInfo.token;

      mergeAuthors(this.idKeep, idDelete, token)
        .then((response) => {
          if (response.data.success) {
            this.message = response.data.message;
            this.messageVariant = "success";
            this.reset();
          } else {
            this.message = response.data.message;
            this.messageVariant = "danger";
          }
        })
        .catch((error) => {
          this.message = "Une erreur est survenue lors de la fusion.";
          this.messageVariant = "danger";
          console.error(error);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    reset() {
      this.query1 = '';
      this.query2 = '';
      this.author1 = null;
      this.author2 = null;
      this.books1 = [];
      this.books2 = [];
      this.duplicateAuthors = [];
      this.idKeep = null;
    }
  },
  watch: {
    query1(val) {
      this.getSuggestions(val, 'suggestions1');
    },
    query2(val) {
      this.getSuggestions(val, 'suggestions2');
    }
  }
}
</script>

<style scoped>
</style>
