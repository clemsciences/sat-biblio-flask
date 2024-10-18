<template>
  <b-container>
    <Title title="Liens utiles" info=""/>

    <b-row v-for="item in rows" :key="item.link" class="p-2">
<!--      <b-col cols="10">-->
      <span>{{item.description}}<br/></span>
      <br/>
      <a :href="item.link">{{item.link}}</a>
        <b-button size="sm" class="ml-3" @click="goToInANewTab(item.link)">
          <b-icon icon="box-arrow-up-right"/>
        </b-button>

<!--      </b-col>-->
<!--      <b-col cols="2">-->

<!--      </b-col>-->
    </b-row>

<!--    <b-list-group>-->
<!--      <b-list-group-item v-for="item in rows" :key="item.link">-->
<!--        {{item.description}}-->
<!--        <a :href="item.link">{{item.link}}</a>-->
<!--        <b-button class="ml-3" @click="goToInANewTab(item.link)">Ouvrir dans un nouvel onglet</b-button>-->
<!--      </b-list-group-item>-->
<!--    </b-list-group>-->
  </b-container>
</template>


<script>

import Title from "@/components/visuel/Title.vue";

class LinkRow {
   constructor(description, link) {
     this.description = description;
     this.link = link;
   }
}
export default {
  name: "LinkView",
  components: {Title},
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
              `${process.env.VUE_APP_SITE_API_URL}/static/sat_biblio_documentation-1.pdf`),
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