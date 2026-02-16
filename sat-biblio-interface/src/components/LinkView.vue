<template>
  <BContainer>
    <AppTitle title="Liens utiles" info=""/>

    <BRow v-for="item in rows" :key="item.link" class="p-2">
<!--      <BCol cols="10">-->
      <span>{{item.description}}<br/></span>
      <br/>
      <a :href="item.link">{{item.link}}</a>
        <BButton size="sm" class="ms-3" @click="goToInANewTab(item.link)">
          <IBiBoxArrowUpRight/>
        </BButton>

<!--      </BCol>-->
<!--      <BCol cols="2">-->

<!--      </BCol>-->
    </BRow>

<!--    <BListGroup>-->
<!--      <BListGroupItem v-for="item in rows" :key="item.link">-->
<!--        {{item.description}}-->
<!--        <a :href="item.link">{{item.link}}</a>-->
<!--        <BButton class="ms-3" @click="goToInANewTab(item.link)">Ouvrir dans un nouvel onglet</BButton>-->
<!--      </BListGroupItem>-->
<!--    </BListGroup>-->
  </BContainer>
</template>


<script>

import AppTitle from "@/components/visuel/AppTitle.vue";
import {BButton, BContainer, BRow} from "bootstrap-vue-next";

class LinkRow {
   constructor(description, link) {
     this.description = description;
     this.link = link;
   }
}
export default {
  name: "LinkView",
  components: {BButton, BRow, BContainer, AppTitle},
  data: function() {
    return {
      rows: [
        new LinkRow(
            "Le site internet de la Société Archéologique de Touraine",
            `https://www.societearcheotouraine.eu/`),
          new LinkRow(
              "Le site internet Gallica pour voir les bulletins de la Société Archéologique de Touraine",
              'https://gallica.bnf.fr/ark:/12148/cb34429572f/date.item'),
          new LinkRow("Lire la documentation de ce site internet",
              `${import.meta.env.VITE_APP_SITE_API_URL}/static/sat_biblio_documentation-1.pdf`),
          new LinkRow("Catalogue SUDOC en ligne",
              "https://www.sudoc.abes.fr/"),
          new LinkRow("Catalogue de la BNF (Bibliothèque nationale de France",
              "https://catalogue.bnf.fr/index.do"),
          new LinkRow("Consulter la collection de la SAT sur Flora",
          "https://floraweb.cg37.fr"),
          new LinkRow("Bibliothèque municipale de Tours", "https://www.bm-tours.fr/recherche---catalogue"),
          new LinkRow("Catalogue de la bibliothèque municipale de Tours",
              "https://www.bm-tours.fr/recherche---catalogue"),
          new LinkRow("Archives départementales d'Indre-et-Loire",
              "https://archives.touraine.fr/"),
          new LinkRow("Bibliothèques de l'université de Tours", "https://bibliotheques.univ-tours.fr/"),
          new LinkRow("Bibliothèque du CESR (Centre d'études supérieures de la Renaissance)", "https://cesr.cnrs.fr/documentation")


      ]

    }
  },
  methods: {
    goToInANewTab(url) {
      window.open(url,'_blank');
    }
  }
}
</script>

<style scoped>
a {
  margin-left: 0.5em;
  margin-right: 0.5em;
}

</style>