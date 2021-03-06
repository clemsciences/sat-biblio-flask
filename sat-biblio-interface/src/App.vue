<template>
  <div id="app">
    <NavBar v-bind:connected="connected"/>
    <router-view></router-view>
  </div>
</template>

<script>

import NavBar from "./components/NavBar";
import localStorageManager from './services/localstorageManager';
// import router from "./router";
import {mapState} from 'vuex';
import {checkUserLogin} from "./services/api";
export default {
  name: 'App',
  components: {
    NavBar
  },
  methods: {
    checkLogin: function() {
      checkUserLogin()
          .then(
              (response) => {
                if(response.data.success) {
                  let connectionInfo = response.data.connectionInfo;
                  if(response.data.connected) {
                    this.$store.commit("connect", {...connectionInfo});
                  } else {
                    this.$store.commit("disconnect");
                  }
                } else {
                  this.$store.commit("disconnect");
                }
              }
          );
    }
  },
  mounted() {
    this.checkLogin();

    // router.beforeEach((to, from, next) => {
    //   this.checkLogin();
    //   next();
    // });

    // axios.interceptors.response.use(function(response) {
    //   response.connected = this.connected;
    //   return response;
    // });
  },
  computed: {
    ...mapState(["connected"])
  },
  watch: {
    connectionInfo: {
      deep: true,
      handler(newValue) {
        localStorageManager.updateSessionInfo(newValue)
      }
    }
  }
}
</script>

<style>

html{
    width:100%;

}

body {
    font-family: 'Verdana', sans-serif;
    padding: 80px 20px 20px 25px;
    width: 100%;
}

a {
    color: #2a99b6;
}

a:hover {
    color: #33bbdf;
}

header, footer, div.page {
    width: 100%;
    margin: auto auto;
    background: #6cb0f3;
    padding: 20px 30px;
}

header h1 {
    color: #6cb0f3;
    margin: 0;
    font-weight: normal;
    font-size: 42px;

}


header nav ul {
    list-style: none;
    margin: 0;
    padding: 0;
}

header nav ul li {
    display: inline;
    margin: 0 0px 0 0;
    padding: 0;
}

div.page {
    background: #f1fbfe;
}

table
{
    border-collapse: collapse;
}
td, th /* Mettre une bordure sur les td ET les th */
{
    border: 1px solid black;
}

p {
    text-align: justify;
}
h1
{
    /*font-size: 1.3em;*/
    color: antiquewhite;
}

h2
{
    /*font-size: 1.5em;*/
    color: #005db6;

}
/*@font-face {*/
    /*font-family: ;*/
    /*src: url() format('');*/
/*}*/

/*body*/
/*{*/
    /*background-image: url("");*/
    /*background-attachment: fixed;*/
/*}*/

.bg-primary{
    background-color: #6cb0f3 !important;
}


blockquote{
  background: #dbf4f9;
  border-left: 10px solid #1547ff;
}

.arrondie
{
    -moz-border-radius:7px;
    -webkit-border-radius:7px;
    border-radius:7px;
}

.navbar-nav, .nav-link{
    padding-left: 0.2rem;
    padding-right: 0.2rem;

}
.btn {
    border: solid;
}

.space-around {
    padding-left: 10px;
}


</style>
