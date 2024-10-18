<template>
  <b-container>
    <Title title="Conception" info=""/>
    <b-row>
      <h5>Le code</h5>
      <p>
        <span>Le code de SAT-Biblio est lisible par tous et se trouve sur &nbsp;</span>
        <a href="https://github.com/clemsciences/sat-biblio-flask">Github</a>
        <span>. </span>
        <span>L'interface web a été développée en <a href="https://v2.vuejs.org/">Vue JS v2</a>. </span>
        <span>Le code du serveur est développé en Python avec le <a href="https://flask.palletsprojects.com/en/3.0.x/">framework Flask</a>.</span>
      </p>
    </b-row>
    <b-row>
      <h5>Un problème ?</h5>
      <p>
        <span>Si vous constatez un problème, vous pouvez contribuer <a href="https://github.com/clemsciences/sat-biblio-flask/issues">en ouvrant un <i>issue</i> sur le projet</a> (en anglais)</span>
        <span> ou alors envoyez un message par le biais de la page <a href="/contact">Contact</a>.</span>
      </p>
    </b-row>
    <b-row>
      <h5>Licence</h5>
      <p>
        <span>
          Le code est protégé sous la licence MIT ce qui signifie que le code peut être réutilisé pour un usage commercial,
          peut être redistribué, modifié et aussi utilisé dans un cadre privé sous condition que la licence demeure et que la <i>reconnaissance de la paternité de l'&oelig;uvre</i> soit respectée.
          On ne peut exigé aucune garantie quant à la qualité du code ainsi qu'aucune responsabilité sur son usage.
        </span>
      </p>
    </b-row>
    <b-row>
      <h5>Origine</h5>
      <p>
        <span>
        Après avoir vu les outils présents alors : des fichiers Excel, l'entreprise de développer une application web pour gérer le catalogue de la bibliothèque s'est dessinée.
        C'est avec le soutien de Michèle Boiron, puis de Florence Cailleau que ce projet a pu naître.
        L'avantage de ces fichiers est d'avoir une vision tabulaire des données.
        Les désavantages sont la gestion des versions, la nécessité d'avoir un logiciel adapté et avec la bonne version.
        Le développement a donc pris 6 ans, entrecoupé de nombreuses pauses dans le projet.
        Il fallu aussi revoir intégralement les données suite au déménagement et au reformatage.
        </span>
      </p>
    </b-row>
    <b-row>
      <h5>Nécessité de changer de paradigme</h5>
      <p>
        En tant que spécialistes de la gestion des informations, de leur promotion et de leur indexation,
        les bibliothèques se doivent de suivre les standards de stockage et d'échanges de données selon
        <a href="https://www.transition-bibliographique.fr/">la transition bibliographique</a> ; SAT-Biblio a pour ambition de suivre cette voie.
      </p>
    </b-row>
    <b-row>
      <h5>Citation par ARK</h5>
      <p>
        <span>Chaque ressource possède un nom ARK non officiel qui permet de fixer un lien permanent. Cela permet de citer la ressource exactement de manière pérenne. </span>
<!--        <span>Par exemple, <b></b></span>-->
        <span>Pour que cela devienne officiel, il faudra enregistrer la bibliothèque de la société archéologique de Touraine comme étant une autorité nommante. </span>
        <span>Il faudra en faire la demande à la <a href="https://arks.org/community/">CDL</a>. </span>
        <span>Pour le moment, le numéro d’autorité nommante non officiel est &laquo;satbiblio&raquo;. </span>
        <span>Pour en savoir plus sur ARK, <a href="https://www.bnf.fr/fr/lidentifiant-ark-archival-resource-key">cliquez ici</a>. </span>
      </p>
    </b-row>
    <b-row>
      <h5>Web sémantique (en cours de réalisation)</h5>
      <p>
        <span>Chaque ressource contient dans son en-tête (balise <b>&lt;head&gt;</b>) en JSON-LD et en Dublin Core dans les balises <b>&lt;meta&gt;</b>. </span>
        <span>On pourra interroger à l'aide de Sparql le catalogue des livres. </span>
      </p>
    </b-row>
    <b-row>
      <h5>Concepteur</h5>
      <p>
        <span>Membre de la société archéologique de Touraine depuis 2018, <a href="https://clementbesnier.eu/">Clément Besnier</a> a commencé à développer SAT&hyphen;Biblio.</span>
      </p>
    </b-row>
    <b-row>
      <h5>Testeurs</h5>
      <p>
        <span>
          <a href="https://github.com/penfornis">Arnaud Penfornis</a> et <a href="https://github.com/gvisse">Guillaume Visse</a> ont aidé aux tests de l'application web et à l'amélioration de l'interface web.
        </span>
      </p>
    </b-row>

  </b-container>
</template>

<script>
import Title from "@/components/visuel/Title.vue";

export default {
  name: "ConceptionView",
  components: {Title},
  data: function () {
    return {

    }
  }

}

</script>

<style scoped>
p {
  text-indent: 5%;
}
span::before {
  line-break: normal;
}
</style>