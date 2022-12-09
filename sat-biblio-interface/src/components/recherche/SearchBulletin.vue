<template>
  <b-container>

    <SuggestionBulletin v-model="selectedNamedEntity" class="my-3"/>
<!--    <h3>{{ selectedNamedEntity }}</h3>-->
    <b-list-group>
      <b-list-group-item v-for="item in citedWorks.result" :key="`${item.published_work.id_}-${item.citation_published_work.text}`">
        <b-card>
          <b-card-title :title="`${item.published_work.publication_type} ${item.published_work.year}`"/>
          <b-card-body>
            <span>{{ item.citation_published_work.text }}</span>
<!--            <a :href=""></a>-->
          </b-card-body>
        </b-card>
      </b-list-group-item>
    </b-list-group>

    <b-list-group>
      <b-list-group-item v-for="item in citedWorks.result" :key="`${item.published_work.id_}-${item.citation_published_work.text}`">
        <b-card>
          <b-card-title :title="`${item.published_work.publication_type} ${item.published_work.year}`"/>
          <b-card-body>
            <span>{{ item.citation_published_work.text }}</span>
<!--            <a :href=""></a>-->
          </b-card-body>
        </b-card>
      </b-list-group-item>
    </b-list-group>





<!--    <b-pagination-->
<!--      v-model="currentPage"-->
<!--      :total-rows="totalNumber"-->
<!--      :per-page="perPage"-->
<!--      aria-controls="my-table"/>-->
<!--&lt;!&ndash;    :sort-by="sortBy" @row-dblclicked="goToUser" :filter="onFilter"&ndash;&gt;-->
<!--    <b-table striped bordered hover :items="search" :fields="fields"-->
<!--             primary-key="id" :per-page="perPage" :current-page="currentPage"-->

<!--             ref="userTable">-->
<!--      <template #table-caption>La liste des résultats correspondant à votre requête dans la base.</template>-->

<!--    </b-table>-->

  </b-container>

</template>

<script>
import {getWorks, searchWorks} from "@/services/api";
import SuggestionBulletin from "@/components/recherche/SuggestionBulletin";

export default {
  name: "SearchBulletin",
  components: {SuggestionBulletin},
  data: function() {
    return {
      query: '',
      selectedNamedEntity: "",
      citedWorks: [],
      works: [],
      // currentPage: 1,
      // totalNumber: 0,
      // perPage: 10,
      // fields: [],
    };
  },
  mounted() {
    this.retrieveBulletinsAndMemoires();
  },
  methods: {
    search(chosenNamedEntity) {
      let params = "?query="+encodeURIComponent(`${chosenNamedEntity}`);
      searchWorks(params).then(
          (response) => {
            console.log(response);
            this.citedWorks = response.data.suggestions;
          //
          }
      ).catch(
          (reason) => {
            console.error(reason);
          }
      )
    },
    retrieveBulletinsAndMemoires() {
      getWorks().then(
          (response) => {
            this.works = response.data.result;
          }
      ).catch((reason) => {
        console.error(reason);
      })
    }
  },
  watch: {
    selectedNamedEntity: function(newValue) {
      this.search(newValue);
    }
  }

}
</script>

<style scoped>

</style>