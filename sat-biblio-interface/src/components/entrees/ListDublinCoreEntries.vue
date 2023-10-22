<template>
  <b-container>
  <h2>Recherche dans la BNF</h2>
    <br/>
    <b-row class="my-3">
      <b-col cols="3">
    <b-form @submit.prevent="reloadWithUrlQueries">
<!--      <b-form-group>-->
<!--        <b-form-group label="Critère de recherche">-->
<!--          <b-form-radio v-model="researchType" value="author">Auteur</b-form-radio>-->
<!--          <b-form-radio v-model="researchType" value="title">Titre</b-form-radio>-->
<!--          <b-form-radio v-model="researchType" value="isbn">ISBN</b-form-radio>-->
<!--          <b-form-radio v-model="researchType" value="publisher">Editeur</b-form-radio>-->
<!--          -->
<!--        </b-form-group>-->
<!--      </b-form-group>-->
      <b-form-group label="Auteur" label-for="search-bnf-author-block" class="my-3">
        <b-form-input type="search" v-model="authorQuery" aria-describedby="search-bnf-author-block"/>
        <b-form-text id="search-bnf-author-block">
          Entrez le prénom et/ou le nom d'un auteur pour retrouver les fiches que vous cherchez.
        </b-form-text>
      </b-form-group>

      <b-form-group label="Titre" label-for="search-bnf-title-block" class="my-3">
        <b-form-input type="search" v-model="titleQuery" aria-describedby="search-bnf-title-block"/>
        <b-form-text id="search-bnf-title-block">
          Entrez un titre ou une partie d'un titre pour retrouver les fiches que vous cherchez.
        </b-form-text>
      </b-form-group>

      <b-form-group label="ISBN" label-for="search-bnf-isbn-block" class="my-3">
        <b-form-input type="search" v-model="isbnQuery" aria-describedby="search-bnf-isbn-block"/>
        <b-form-text id="search-bnf-isbn-block">
          Entrez un ISBN pour retrouver les fiches que vous cherchez.
        </b-form-text>
      </b-form-group>

      <b-form-group label="Editeur" label-for="search-bnf-publisher-block" class="my-3">
        <b-form-input type="search" v-model="publisherQuery" aria-describedby="search-bnf-publisher-block"/>
        <b-form-text id="search-bnf-publisher-block">
          Entrez un éditeur pour retrouver les fiches que vous cherchez.
        </b-form-text>
      </b-form-group>
      <b-form-group>
        <b-button type="submit">Rechercher</b-button>
      </b-form-group>
    </b-form>
        </b-col>
    <b-col cols="9" v-if="loading" align-self="center">
<!--      <b-col></b-col>-->
      <b-spinner label="chargement" class="my-center"/>
      </b-col>
      <b-col cols="9" v-else-if="totalNumber > 0">
      <b-pagination
          v-model="currentPage"
          :total-rows="totalNumber"
          :per-page="perPage"
          aria-controls="my-table"
          class="my-3"/>
      <b-table striped bordered hover :items="retrieveList" :fields="fields"
               primary-key="identifier" :per-page="perPage" :current-page="currentPage"
               @row-dblclicked="goTo">
        <template #table-caption v-if="caption.length > 0">{{ caption }}</template>
        <template #cell(description)="data">
          <span> {{shorten(data.item.description)}}</span>
        </template>
        <template #cell(identifier)="data">
          <span><a :href="extractLink(data.item.identifier)">{{ extractLink(data.item.identifier) }}</a>
          {{ restOfExtraction(data.item.identifier) }}
          </span>
        </template>
      </b-table>
      </b-col>
    <b-col cols="9" v-else class="my-center"><p>Il n'y a aucune entrée.</p></b-col>

    </b-row>
  </b-container>
</template>

<script>
// import ListEntries from "@/components/entrees/ListEntries";
import {getDublinCoreEntries} from "@/services/api";

export default {
  name: "ListDublinCoreEntries",
  // components: {ListEntries},
  props: {
    initialAuthorQuery: {
      type: String,
      default: ""
    },
    initialTitleQuery: {
      type: String,
      default: ""
    },
    initialISBNQuery: {
      type: String,
      default: ""
    },
    initialPublisherQuery: {
      type: String,
      default: ""
    }
  },
  data: function() {
    return {
      totalNumber: 0,
      currentPage: 1,
      perPage: 20,
      caption: "",
      sortBy: "",
      entries: [],
      authorQuery: "",
      publisherQuery: "",
      titleQuery: "",
      isbnQuery: "",
      loading: false,
      // researchType: "",
      fields: [
        {
          key: "identifier",
          label: "Identifiant"
        },
        {
          key: "title",
          label: "Titre"
        },
        {
          key: "description",
          label: "Description"
        },
        {
          key: "creator",
          label: "Auteur"
        },
        {
          key: "publisher",
          label: "Editeur"
        },
        {
          key: "date",
          label: "Date"
        },
        {
          key: "language",
          label: "Langue"
        },
        {
          key: "subject",
          label: "Sujet"
        },
        {
          key: "type",
          label: "Type"
        },
        {
          key: "format",
          label: "Format"
        },
        {
          key: "source",
          label: "Source"
        },
        // {
        //   key: "relation",
        //   label: "Relation"
        // },
        // {
        //   key: "rights",
        //   label: "Droits"
        // },
      ]
    };
  },
  mounted() {
    // this.query = this.initialQuery;
    if(this.initialAuthorQuery.length > 0) {
      this.authorQuery = this.initialAuthorQuery;
    } else if (this.$route.query.author && this.$route.query.author.length > 0) {
      this.authorQuery = decodeURIComponent(this.$route.query.author);
    }

    if(this.initialTitleQuery.length > 0) {
      this.titleQuery = this.initialTitleQuery;
    } else if (this.$route.query.title && this.$route.query.title.length > 0) {
      this.titleQuery = decodeURIComponent(this.$route.query.title);
    }

    if(this.initialPublisherQuery.length > 0) {
      this.publisherQuery = this.initialPublisherQuery;
    } else if (this.$route.query.publisher && this.$route.query.publisher.length > 0) {
      this.publisherQuery = decodeURIComponent(this.$route.query.publisher);
    }

    if(this.initialISBNQuery.length > 0) {
      this.isbnQuery = this.initialISBNQuery;
    } else if (this.$route.query.isbn && this.$route.query.isbn.length > 0) {
      this.isbnQuery = decodeURIComponent(this.$route.query.isbn);
    }

    this.loading = false;
    this.getEntryDublinCoreEntries();
  },
  computed: {
    query() {
      let queries = [];
      if(this.authorQuery.length > 0) {
        queries.push(`bib.author all "${this.authorQuery}"`);
      }
      if(this.titleQuery.length > 0) {
        queries.push(`bib.title all "${this.titleQuery}"`);
      }
      if(this.isbnQuery.length > 0) {
        queries.push(`bib.isbn all "${this.isbnQuery}"`);
      }
      if(this.publisherQuery.length > 0) {
        queries.push(`bib.publisher all "${this.publisherQuery}"`);
      }
      console.log(queries.join(" and "));
      return queries.join(" and ");
    }
  },
  // watch: {
  //   query: function(val, oldVal) {
  //     this.$router.push();
  //   }
  // },
  methods: {
    reloadWithUrlQueries() {
      this.$router.push({
        name: "dublin-core",
        query: {
          author: encodeURIComponent(this.authorQuery),
          title: encodeURIComponent(this.titleQuery),
          isbn: encodeURIComponent(this.isbnQuery),
          publisher: encodeURIComponent(this.publisherQuery)
        }
      }).then(() => {
        window.location.reload();
      });
    },
    getEntryDublinCoreEntries() {
      console.log("query "+this.query);
      this.loading = true;
      let params = `query=${this.query}&perPage=${this.perPage}`;
      getDublinCoreEntries(params).then(
          (response) => {
            this.loading = false;
            if(response.data.success) {
              this.totalNumber = response.data.total;
              this.entries = response.data.entries.records.map((entry) => entry.recordData);
              console.log(this.totalNumber);
              console.log(this.entries);
            }
          }
      ).catch(
          (reason) => {
            this.loading = false;
            console.log(reason);
          }
      );
    },
    retrieveList(ctx, callback) {
      let params = "page="+ctx.currentPage+
          "&size="+ctx.perPage+
          "&sortBy="+ctx.sortBy+`&query=${this.query}&perPage=${this.perPage}`;
      console.log(params);

      getDublinCoreEntries(params).then(
          (response) => {
            if(response.data.success) {
              this.totalNumber = response.data.total;
              this.entries = response.data.entries.records.map((entry) => entry.recordData);
              console.log(this.entries);
              callback(this.entries);
            }
          }
      ).catch(
          (reason) => {
            console.log(reason);
            callback([]);
          }
      );
      return null;
    },
    goTo: function() {
      // let id = row.id;
      // this.$router.push(`/dublin-core/${id}`);
    },
    shorten: function(text) {
      if(text.length > 100) {
        return text.substring(0, 100)+"..."
      } else {
        return text;
      }
    },
    extractLink: function(link) {
      let linkList = link.split(" ");
      if(linkList.length > 1) {
        return linkList[0];
      }
      return link;
    },
    restOfExtraction: function(link) {
      let linkList = link.split(" ");
      if(linkList.length > 1) {
        return linkList.slice(1).join(" ");
      }
      return "";
    }

  }

}
</script>

<style scoped>
  /*b-form-group {*/
  /*  margin-: 30em;*/
  /*}*/

  .my-center {
    position: fixed; top: 50%; left: 50%;
  }
</style>