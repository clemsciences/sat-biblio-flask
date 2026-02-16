<template>
  <BContainer>

    <router-link :to="{ name: 'works'}">Liste des ouvrages</router-link>

    <BulletinSuggestion v-model="selectedNamedEntity" class="my-3"/>
<!--    <h3>{{ selectedNamedEntity }}</h3>-->
    <BListGroup>
      <BListGroupItem v-for="item in citedWorks.result" :key="`${item.published_work.id_}-${item.citation_published_work.text}`">
        <BCard>
          <BCardTitle :title="`${item.published_work.publication_type} ${item.published_work.year}`"/>
          <BCardBody>
            <span>{{ item.citation_published_work.text }}</span>
<!--            <a :href=""></a>-->
          </BCardBody>
        </BCard>
      </BListGroupItem>
    </BListGroup>

    <BListGroup>
      <BListGroupItem v-for="item in citedWorks.result" :key="`${item.published_work.id_}-${item.citation_published_work.text}`">
        <BCard>
          <BCardTitle :title="`${item.published_work.publication_type} ${item.published_work.year}`"/>
          <BCardBody>
            <span>{{ item.citation_published_work.text }}</span>
<!--            <a :href=""></a>-->
          </BCardBody>
        </BCard>
      </BListGroupItem>
    </BListGroup>





<!--    <BPagination-->
<!--      v-model="currentPage"-->
<!--      :total-rows="totalNumber"-->
<!--      :per-page="perPage"-->
<!--      aria-controls="my-table"/>-->
<!--&lt;!&ndash;    :sort-by="sortBy" @row-dblclicked="goToUser" :filter="onFilter"&ndash;&gt;-->
<!--    <BTable striped bordered hover :items="search" :fields="fields"-->
<!--             primary-key="id" :per-page="perPage" :current-page="currentPage"-->

<!--             ref="userTable">-->
<!--      <template #table-caption>La liste des résultats correspondant à votre requête dans la base.</template>-->

<!--    </BTable>-->

  </BContainer>

</template>

<script>
import {getPublishedWorks, searchWorks} from "@/services/api.js";
import BulletinSuggestion from "@/components/recherche/SuggestionBulletin.vue";

export default {
  name: "SearchBulletin",
  components: {BulletinSuggestion},
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
      getPublishedWorks("").then(
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