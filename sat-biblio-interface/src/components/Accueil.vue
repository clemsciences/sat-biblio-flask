<template>
  <b-container class="text-center my-5">
    <h2 class="mb-4">Catalogue en ligne de la Bibliothèque d'Histoire de la Touraine - BHT</h2>

    <!-- Connection Info -->
    <div v-if="connected">
      <h3>Connexion</h3>
      <p>
        Vous êtes connecté en tant que
        <b>{{ connectionInfo.first_name }} {{ connectionInfo.family_name }}</b>
        (<i>{{ connectionInfo.email }}</i>). Vous êtes
        <b>{{ rightString }}</b>.
      </p>
    </div>

    <!-- Description -->
    <p class="lead mt-4">
      Bienvenue sur SatBiblio, une application web qui permet de consulter et de gérer
      le catalogue de la bibliothèque de la Société Archéologique de Touraine.
    </p>

    <!-- Bouton central -->
    <b-button
      variant="primary"
      size="lg"
      href="/catalogue"
      class="my-4"
    >
      <b-icon icon="book"></b-icon>
      Consulter le catalogue
    </b-button>

    <div>
      <a href="#new-tool" class="mx-2">Raisons de ce nouvel outil</a>
      <!--<a href="#video-introduction" class="mx-2">Vidéo d'introduction</a>-->
      <a href="/conception" class="mx-2">Conception</a>
      <a href="/liens" class="mx-2">Liens utiles</a>
    </div>

    <b-button variant="secondary"
    size="mg"
    href="#video-introduction"
    class="my-4">
      <b-icon icon="file-play"></b-icon>
      Voir la vidéo d'introduction

    </b-button>

    <div class="d-flex flex-wrap justify-content-center align-items-center mt-5" id="book-images">

    <b-img
        class="m-3 img-fluid"
    sizes="(max-width: 200px) 100vw, 200px"
    srcset="
    bht_livres_1_z2ivvi/bht_livres_1_z2ivvi_c_scale,w_200.jpg 200w,
    bht_livres_1_z2ivvi/bht_livres_1_z2ivvi_c_scale,w_347.jpg 347w,
    bht_livres_1_z2ivvi/bht_livres_1_z2ivvi_c_scale,w_459.jpg 459w,
    bht_livres_1_z2ivvi/bht_livres_1_z2ivvi_c_scale,w_553.jpg 553w,
    bht_livres_1_z2ivvi/bht_livres_1_z2ivvi_c_scale,w_639.jpg 639w,
    bht_livres_1_z2ivvi/bht_livres_1_z2ivvi_c_scale,w_713.jpg 713w,
    bht_livres_1_z2ivvi/bht_livres_1_z2ivvi_c_scale,w_785.jpg 785w,
    bht_livres_1_z2ivvi/bht_livres_1_z2ivvi_c_scale,w_854.jpg 854w,
    bht_livres_1_z2ivvi/bht_livres_1_z2ivvi_c_scale,w_920.jpg 920w,
    bht_livres_1_z2ivvi/bht_livres_1_z2ivvi_c_scale,w_974.jpg 974w,
    bht_livres_1_z2ivvi/bht_livres_1_z2ivvi_c_scale,w_1033.jpg 1033w,
    bht_livres_1_z2ivvi/bht_livres_1_z2ivvi_c_scale,w_1091.jpg 1091w,
    bht_livres_1_z2ivvi/bht_livres_1_z2ivvi_c_scale,w_1145.jpg 1145w,
    bht_livres_1_z2ivvi/bht_livres_1_z2ivvi_c_scale,w_1201.jpg 1201w,
    bht_livres_1_z2ivvi/bht_livres_1_z2ivvi_c_scale,w_1253.jpg 1253w,
    bht_livres_1_z2ivvi/bht_livres_1_z2ivvi_c_scale,w_1302.jpg 1302w,
    bht_livres_1_z2ivvi/bht_livres_1_z2ivvi_c_scale,w_1354.jpg 1354w,
    bht_livres_1_z2ivvi/bht_livres_1_z2ivvi_c_scale,w_1398.jpg 1398w,
    bht_livres_1_z2ivvi/bht_livres_1_z2ivvi_c_scale,w_1400.jpg 1400w"
    src="bht_livres_1_z2ivvi_c_scale,w_1400.jpg"
    alt=""/>


    <b-img
        class="m-3 img-fluid"
    sizes="(max-width: 200px) 100vw, 200px"
    srcset="
    bht_livres_2_unizmo/bht_livres_2_unizmo_c_scale,w_200.jpg 200w,
    bht_livres_2_unizmo/bht_livres_2_unizmo_c_scale,w_343.jpg 343w,
    bht_livres_2_unizmo/bht_livres_2_unizmo_c_scale,w_451.jpg 451w,
    bht_livres_2_unizmo/bht_livres_2_unizmo_c_scale,w_542.jpg 542w,
    bht_livres_2_unizmo/bht_livres_2_unizmo_c_scale,w_628.jpg 628w,
    bht_livres_2_unizmo/bht_livres_2_unizmo_c_scale,w_706.jpg 706w,
    bht_livres_2_unizmo/bht_livres_2_unizmo_c_scale,w_776.jpg 776w,
    bht_livres_2_unizmo/bht_livres_2_unizmo_c_scale,w_839.jpg 839w,
    bht_livres_2_unizmo/bht_livres_2_unizmo_c_scale,w_902.jpg 902w,
    bht_livres_2_unizmo/bht_livres_2_unizmo_c_scale,w_964.jpg 964w,
    bht_livres_2_unizmo/bht_livres_2_unizmo_c_scale,w_1025.jpg 1025w,
    bht_livres_2_unizmo/bht_livres_2_unizmo_c_scale,w_1078.jpg 1078w,
    bht_livres_2_unizmo/bht_livres_2_unizmo_c_scale,w_1135.jpg 1135w,
    bht_livres_2_unizmo/bht_livres_2_unizmo_c_scale,w_1192.jpg 1192w,
    bht_livres_2_unizmo/bht_livres_2_unizmo_c_scale,w_1243.jpg 1243w,
    bht_livres_2_unizmo/bht_livres_2_unizmo_c_scale,w_1294.jpg 1294w,
    bht_livres_2_unizmo/bht_livres_2_unizmo_c_scale,w_1346.jpg 1346w,
    bht_livres_2_unizmo/bht_livres_2_unizmo_c_scale,w_1398.jpg 1398w,
    bht_livres_2_unizmo/bht_livres_2_unizmo_c_scale,w_1400.jpg 1400w"
    src="bht_livres_2_unizmo_c_scale,w_1400.jpg"
    alt=""/>



    <b-img
        class="m-3 img-fluid"
    sizes="(max-width: 200px) 100vw, 200px"
    srcset="
    bht_livres_3_ui0v8v/bht_livres_3_ui0v8v_c_scale,w_200.jpg 200w,
    bht_livres_3_ui0v8v/bht_livres_3_ui0v8v_c_scale,w_345.jpg 345w,
    bht_livres_3_ui0v8v/bht_livres_3_ui0v8v_c_scale,w_450.jpg 450w,
    bht_livres_3_ui0v8v/bht_livres_3_ui0v8v_c_scale,w_536.jpg 536w,
    bht_livres_3_ui0v8v/bht_livres_3_ui0v8v_c_scale,w_619.jpg 619w,
    bht_livres_3_ui0v8v/bht_livres_3_ui0v8v_c_scale,w_696.jpg 696w,
    bht_livres_3_ui0v8v/bht_livres_3_ui0v8v_c_scale,w_767.jpg 767w,
    bht_livres_3_ui0v8v/bht_livres_3_ui0v8v_c_scale,w_830.jpg 830w,
    bht_livres_3_ui0v8v/bht_livres_3_ui0v8v_c_scale,w_892.jpg 892w,
    bht_livres_3_ui0v8v/bht_livres_3_ui0v8v_c_scale,w_954.jpg 954w,
    bht_livres_3_ui0v8v/bht_livres_3_ui0v8v_c_scale,w_1015.jpg 1015w,
    bht_livres_3_ui0v8v/bht_livres_3_ui0v8v_c_scale,w_1071.jpg 1071w,
    bht_livres_3_ui0v8v/bht_livres_3_ui0v8v_c_scale,w_1130.jpg 1130w,
    bht_livres_3_ui0v8v/bht_livres_3_ui0v8v_c_scale,w_1184.jpg 1184w,
    bht_livres_3_ui0v8v/bht_livres_3_ui0v8v_c_scale,w_1238.jpg 1238w,
    bht_livres_3_ui0v8v/bht_livres_3_ui0v8v_c_scale,w_1290.jpg 1290w,
    bht_livres_3_ui0v8v/bht_livres_3_ui0v8v_c_scale,w_1344.jpg 1344w,
    bht_livres_3_ui0v8v/bht_livres_3_ui0v8v_c_scale,w_1397.jpg 1397w,
    bht_livres_3_ui0v8v/bht_livres_3_ui0v8v_c_scale,w_1400.jpg 1400w"
    src="bht_livres_3_ui0v8v_c_scale,w_1400.jpg"
    alt=""/>


    <b-img
        class="m-3 img-fluid"
    sizes="(max-width: 200px) 100vw, 200px"
    srcset="
    bht_livres_4_j09v5z/bht_livres_4_j09v5z_c_scale,w_200.jpg 200w,
    bht_livres_4_j09v5z/bht_livres_4_j09v5z_c_scale,w_346.jpg 346w,
    bht_livres_4_j09v5z/bht_livres_4_j09v5z_c_scale,w_464.jpg 464w,
    bht_livres_4_j09v5z/bht_livres_4_j09v5z_c_scale,w_534.jpg 534w,
    bht_livres_4_j09v5z/bht_livres_4_j09v5z_c_scale,w_617.jpg 617w,
    bht_livres_4_j09v5z/bht_livres_4_j09v5z_c_scale,w_692.jpg 692w,
    bht_livres_4_j09v5z/bht_livres_4_j09v5z_c_scale,w_764.jpg 764w,
    bht_livres_4_j09v5z/bht_livres_4_j09v5z_c_scale,w_828.jpg 828w,
    bht_livres_4_j09v5z/bht_livres_4_j09v5z_c_scale,w_893.jpg 893w,
    bht_livres_4_j09v5z/bht_livres_4_j09v5z_c_scale,w_951.jpg 951w,
    bht_livres_4_j09v5z/bht_livres_4_j09v5z_c_scale,w_1006.jpg 1006w,
    bht_livres_4_j09v5z/bht_livres_4_j09v5z_c_scale,w_1066.jpg 1066w,
    bht_livres_4_j09v5z/bht_livres_4_j09v5z_c_scale,w_1122.jpg 1122w,
    bht_livres_4_j09v5z/bht_livres_4_j09v5z_c_scale,w_1176.jpg 1176w,
    bht_livres_4_j09v5z/bht_livres_4_j09v5z_c_scale,w_1232.jpg 1232w,
    bht_livres_4_j09v5z/bht_livres_4_j09v5z_c_scale,w_1286.jpg 1286w,
    bht_livres_4_j09v5z/bht_livres_4_j09v5z_c_scale,w_1335.jpg 1335w,
    bht_livres_4_j09v5z/bht_livres_4_j09v5z_c_scale,w_1389.jpg 1389w,
    bht_livres_4_j09v5z/bht_livres_4_j09v5z_c_scale,w_1394.jpg 1394w,
    bht_livres_4_j09v5z/bht_livres_4_j09v5z_c_scale,w_1400.jpg 1400w"
    src="bht_livres_4_j09v5z_c_scale,w_1400.jpg"
    alt=""/>



<!--      <b-img src="bht_livres_1.jpg" class="m-3 img-fluid" style="max-width: 200px" alt="Livres sur étagère"/>-->
<!--      <b-img src="bht_livres_2.jpg" class="m-3 img-fluid" style="max-width: 200px" alt="Livres sur étagère"/>-->
<!--      <b-img src="bht_livres_3.jpg" class="m-3 img-fluid" style="max-width: 200px" alt="Livres sur étagère"/>-->
<!--      <b-img src="bht_livres_4.jpg" class="m-3 img-fluid" style="max-width: 200px" alt="Livres sur étagère"/>-->
    </div>

    <!-- Bouton toggle et collapsible (placé plus bas à gauche) -->
    <div class="text-start mt-5" id="new-tool">
<!--      <b-button v-b-toggle.collapse-why variant="info" size="sm">-->
        <h5>Pourquoi passer à ce nouvel outil ?</h5>
<!--      </b-button>-->
<!--      <b-collapse id="collapse-why" class="mt-3">-->
      <b-list-group>
        <b-list-group-item>
          Le catalogue est <b>centralisé</b>.<br/> <span class="detail">Si quelqu'un fait une modification, celle-ci est directement accessible par tous les utilisateurs, évitant ainsi d'avoir différentes versions.</span>
        </b-list-group-item>
        <b-list-group-item>
          Le catalogue est <b>accessible</b> à tous.<br/> <span class="detail">Des droits spécifiques permettent de gérer et de modifier le catalogue.</span>
        </b-list-group-item>
        <b-list-group-item>
          Le catalogue est <b>indépendant</b> du format.<br/> <span class="detail">Les données peuvent être exportées dans le format souhaité.</span>
        </b-list-group-item>
        <b-list-group-item>
          Le système permet la <b>gestion des emprunts</b> et l'envoi automatique d'emails aux retardataires.
        </b-list-group-item>
      </b-list-group>
<!--      </b-collapse>-->
    </div>

    <div class="d-flex flex-wrap justify-content-center align-items-center mt-5" id="book-images">
<!--      <b-img src="bht_rdc_1_dyb5uq/bht_rdc_1_dyb5uq_c_scale,w_1400.jpg"-->
<!--             class="m-auto img-fluid"-->
<!--             style="max-width: 1000px"-->
<!--             alt="Photo du rez-de-chaussée de la bibliothèque."/>-->
<b-img
    class="m-3 img-fluid"
sizes="(max-width: 1000px) 100vw, 1000px"
srcset="
bht_rdc_1_dyb5uq/bht_rdc_1_dyb5uq_c_scale,w_200.jpg 200w,
bht_rdc_1_dyb5uq/bht_rdc_1_dyb5uq_c_scale,w_410.jpg 410w,
bht_rdc_1_dyb5uq/bht_rdc_1_dyb5uq_c_scale,w_565.jpg 565w,
bht_rdc_1_dyb5uq/bht_rdc_1_dyb5uq_c_scale,w_683.jpg 683w,
bht_rdc_1_dyb5uq/bht_rdc_1_dyb5uq_c_scale,w_866.jpg 866w,
bht_rdc_1_dyb5uq/bht_rdc_1_dyb5uq_c_scale,w_964.jpg 964w,
bht_rdc_1_dyb5uq/bht_rdc_1_dyb5uq_c_scale,w_998.jpg 998w,
bht_rdc_1_dyb5uq/bht_rdc_1_dyb5uq_c_scale,w_1131.jpg 1131w,
bht_rdc_1_dyb5uq/bht_rdc_1_dyb5uq_c_scale,w_1220.jpg 1220w,
bht_rdc_1_dyb5uq/bht_rdc_1_dyb5uq_c_scale,w_1321.jpg 1321w,
bht_rdc_1_dyb5uq/bht_rdc_1_dyb5uq_c_scale,w_1395.jpg 1395w,
bht_rdc_1_dyb5uq/bht_rdc_1_dyb5uq_c_scale,w_1400.jpg 1400w"
src="bht_rdc_1_dyb5uq/bht_rdc_1_dyb5uq_c_scale,w_1400.jpg"
alt=""/>
    </div>
<!--    <iframe width="560" height="315" src="https://www.youtube.com/embed/nqsV88Uqhpg?si=6IzUGsdQaHQw-6gX" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>-->

    <div id="video-introduction">
      <b-embed
        type="iframe"
        aspect="16by9"
        src="https://www.youtube.com/embed/nqsV88Uqhpg?si=6IzUGsdQaHQw-6gX"
        allowfullscreen
      ></b-embed>
    </div>
  </b-container>
</template>
<script>

import {mapState} from "vuex";
import {getRightString} from "@/services/rights";
export default {
name: "Accueil",
  components: {},
  computed: {
    ...mapState(["connected", "connectionInfo"]),
    rightString: function () {
      return getRightString(this.connectionInfo.right);
    }
  }

}
</script>

<style scoped>

#new-tool,
#video-introduction {
  scroll-margin-top: 72px; /* Adjust to your navbar height */
}



</style>