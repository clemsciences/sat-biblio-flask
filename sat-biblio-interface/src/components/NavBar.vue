<template>

  <div class="container">
    <b-navbar class="navbar-default fixed-top navbar-dark sat-color-nav">
      <b-navbar-brand><h1>SAT - Biblio</h1></b-navbar-brand>
      <b-navbar-toggle target="navbarSupportedContent"></b-navbar-toggle>
      <b-collapse is-nav style="height: 1px;" id="navbarSupportedContent">
            <b-navbar-nav>
                <b-nav-item to="/" class="nav-link space-around titre-nav-item">Accueil</b-nav-item>
                <b-nav-item>
                    <b-nav-item-dropdown text="Créer" class="titre-nav-item">
                      <b-dropdown-item to="/auteur/creer">Créer auteur</b-dropdown-item>
                      <b-dropdown-item to="/reference-livre/creer">Créer référence</b-dropdown-item>
                      <b-dropdown-item to="/enregistrement/creer">Créer enregistrement</b-dropdown-item>
                    </b-nav-item-dropdown>
                </b-nav-item>
                <b-nav-item class="active">
                  <b-nav-item-dropdown text="Consulter" class="titre-nav-item">
                    <b-dropdown-item to="/auteur/liste">Consulter auteurs</b-dropdown-item>
                    <b-dropdown-item to="/reference-livre/liste">Consulter références</b-dropdown-item>
                    <b-dropdown-item to="/enregistrement/liste">Consulter catalogue</b-dropdown-item>
<!--                    <router-link class="nav-link" to="/enregistrement/liste">Catalogue</router-link>-->
                  </b-nav-item-dropdown>
                </b-nav-item>
                <b-nav-item class="active nav-link space-around titre-nav-item" to="/exporter">Exporter</b-nav-item>
                <b-nav-item class="active nav-link space-around titre-nav-item" to="/rechercher">Rechercher</b-nav-item>
                <b-nav-item>
                  <b-nav-item-dropdown text="Emprunter" class="titre-nav-item">
                      <b-dropdown-item to="/emprunt/livre">Nouvel emprunt</b-dropdown-item>
                      <b-dropdown-item to="/emprunt/liste">Livres empruntés</b-dropdown-item>
                  </b-nav-item-dropdown>
                </b-nav-item>
                <b-nav-item to="/contact" class="nav-link space-around titre-nav-item">Contact</b-nav-item>
            </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>

</template>

<script>
export default {
  name: "NavBar"
}
</script>

<style scoped>
.sat-color-nav
{
background-color: #6cb0f3;
}
/*b-nav-item-dropdown
{
  background-color: #6cb0f3;
}*/

.titre-nav-item
{
  font-size: 1.5rem;
}



</style>