<template>

  <div class="container">
    <b-navbar class="navbar navbar-default fixed-top navbar-dark bg-primary">
      <b-navbar-brand><h1>SAT - Biblio</h1></b-navbar-brand>
      <b-navbar-toggle target="navbarSupportedContent"></b-navbar-toggle>
      <b-collapse is-nav style="height: 1px;" id="navbarSupportedContent">
            <b-navbar-nav>
                <b-nav-item>
                  <router-link to="/" class="nav-link space-around">Accueil</router-link>
                </b-nav-item>
                <b-nav-item>
                    <b-nav-item-dropdown text="Créer" >
                      <b-dropdown-item><router-link to="/auteur/creer">Créer auteur</router-link></b-dropdown-item>
                      <b-dropdown-item><router-link to="/reference-livre/creer">Créer référence</router-link></b-dropdown-item>
                      <b-dropdown-item><router-link to="/enregistrement/creer">Créer enregistrement</router-link></b-dropdown-item>
                    </b-nav-item-dropdown>
                </b-nav-item>
                <b-nav-item class="active">
                  <router-link class="nav-link" to="/enregistrement/liste">Catalogue</router-link>
                </b-nav-item>
                <b-nav-item class="active">
                  <router-link to="/exporter" class="nav-link space-around">Exporter</router-link>
                </b-nav-item>
                <b-nav-item class="nav-item active">
                  <router-link to="/rechercher" class="nav-link space-around">Rechercher</router-link>
                </b-nav-item>
                <b-nav-item>
                  <b-nav-item-dropdown text="Emprunter">
                      <b-dropdown-item><router-link to="/emprunt/livre">Nouvel emprunt</router-link></b-dropdown-item>
                      <b-dropdown-item><router-link to="/emprunt/liste">Livres empruntés</router-link></b-dropdown-item>
                  </b-nav-item-dropdown>
                </b-nav-item>
                <b-nav-item>
                  <router-link to="/contact" class="nav-link space-around">Contact</router-link>
                </b-nav-item>
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
b-nav-item-dropdown
{
  background-color: #6cb0f3;
}

b-dropdown-item
{
  background-color: #6cb0f3;
}

</style>