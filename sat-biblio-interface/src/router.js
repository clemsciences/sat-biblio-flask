

import { createRouter, createWebHistory } from "vue-router";
import RechercheView from "@/components/recherche/Recherche.vue";
import AccueilView from "@/components/AccueilView.vue";
import ExportView from "@/components/export/ExportView.vue";
import CreationUtilisateur from "@/components/utilisateur/CreationUtilisateur.vue";
import UtilisateurEnregistre from "@/components/utilisateur/UtilisateurEnregistre.vue";
import MotDePasseOublie from "@/components/mot_de_passe/MotDePasseOublie.vue";
import ReinitialisationMotDePasse from "@/components/mot_de_passe/ReinitialisationMotDePasse.vue";
import MotDePasseEmail from "@/components/mot_de_passe/MotDePasseEmail.vue";
import MotDePasseReinitialise from "@/components/mot_de_passe/MotDePasseReinitialise.vue";
import InviteView from "@/components/utilisateur/Invite.vue";
import ConnexionView from "@/components/connexion/ConnexionView.vue";
import DeconnexionView from "@/components/connexion/DeconnexionView.vue";
import ResultatsRecherche from "@/components/recherche/ResultatsRecherche.vue";
import CreationAuteur from "@/components/auteur/CreationAuteur.vue";
import LireAuteur from "@/components/auteur/LireAuteur.vue";
import CreationReferenceLivre from "@/components/reference_livre/CreationReferenceLivre.vue";
import LireReferenceLivre from "@/components/reference_livre/LireReferenceLivre.vue";
import EnregistrementView from "@/components/enregistrement/EnregistrementView.vue";
import LireEnregistrement from "@/components/enregistrement/LireEnregistrement.vue";
import ListeEnregistrement from "@/components/enregistrement/ListeEnregistrement.vue";
import ListeReferenceLivre from "@/components/reference_livre/ListeReferenceLivre.vue";
import Contact from "@/components/ContactView.vue";
import Emprunter from "@/components/emprunt/Emprunter.vue";
import ListeEmprunt from "@/components/emprunt/ListeEmprunt.vue";
import ListeAuteur from "@/components/auteur/ListeAuteur.vue";
import ListeMotsClefs from "@/components/enregistrement/ListeMotsClefs.vue";
import StatisticsDashboard from "@/components/statistics/StatisticsDashboard.vue";
import AdminView from "@/components/admin/AdminView.vue";
import GestionnaireView from "@/components/admin/GestionnaireView.vue";
import PageNotFoundView from "@/components/PageNotFound.vue";
import {isValidJwt} from "@/services/authentication.js";
import {rights} from "@/services/rights.js";
import store from "@/store.js";
import UtilisateurView from "@/components/utilisateur/UtilisateurView.vue";
// import ImportTester from "@/components/import/ImportTester.vue";
import ImportTester2 from "@/components/import/ImportTester2.vue";
import LireEmprunt from "@/components/emprunt/LireEmprunt.vue";
import LogEventListView from "@/components/log/LogEventList.vue";
import GlobalImport from "@/components/import/GlobalImport.vue";
import ListDublinCoreEntriesView from "@/components/entrees/ListDublinCoreEntries.vue";
// import ImageManager from "@/components/images/ImageManager.vue";
import ImportExport from "@/components/import_export/ImportExport.vue";
import SearchBulletin from "@/components/recherche/SearchBulletin.vue";
import WorkListView from "@/components/works/WorkList.vue";
import WorkAnnotationView from "@/components/works/WorkAnnotation.vue";
import ImportList from "@/components/import/ImportList.vue";
import ImportItem from "@/components/import/ImportItemView.vue";
import ArkView from "@/components/ark/ArkView.vue";
import LinkView from "@/components/LinkView.vue";
import ConceptionView from "@/components/ConceptionView.vue";
import ChangelogView from "@/components/ChangelogView.vue";
import CreationEnregistrementComplet from "./components/enregistrement_complet/CreationEnregistrementComplet.vue";
import LireEnregistrementComplet from "./components/enregistrement_complet/LireEnregistrementComplet.vue";
import ListeEnregistrementComplet from "./components/enregistrement_complet/ListeEnregistrementComplet.vue";
import SatSubscription from "@/components/societaire/SatSubscription.vue";
import MergeAuthors from "@/components/admin/MergeAuthors.vue";

const router = createRouter({
    history: createWebHistory(),
    scrollBehavior(to, from, savedPosition) {
        if (to.hash) {
            return {
                el: to.hash,
            }
        }
        if (savedPosition) {
            return savedPosition;
        }
        if (to.path === from.path && JSON.stringify(to.query) !== JSON.stringify(from.query)) {
          return false;
        }

        return { top: 0, left: 0 };
    },
    routes: [
        {
            name: "recherche",
            path: '/recherche',
            component: RechercheView,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        {
            path: '/',
            component: AccueilView,
            name: 'accueil',
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        {
            path: '/exporter',
            component: ExportView,
            meta: {needAuth: true, reachableFrom: rights.lecteur}
        },
        // region utilisateurs
        {
            name: "utilisateur-creer",
            path: '/utilisateur/creer',
            component: CreationUtilisateur,
            meta: {needAuth: false, reachableFrom: rights.contributeur}
        },
        {
            name: "verification-enregistrement",
            path: '/utilisateur/verification-enregistrement',
            component: UtilisateurEnregistre,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        {
            name: "utilisateur-mot-de-passe-oublie",
            path: '/utilisateur/mot-de-passe-oublie',
            component: MotDePasseOublie,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        {
            name: "utilisateur-reinitialiser-mot-de-passe",
            path: '/utilisateur/reinitialiser-mot-de-passe',
            component: ReinitialisationMotDePasse,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        {
            name: "utilisateur-mot-de-passe-oublie-email",
            path: '/utilisateur/mot-de-passe-email',
            component: MotDePasseEmail,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        {
            name: 'utilisateur-mot-de-passe-reinitialise',
            path: '/utilisateur/mot-de-passe-reinitialise',
            component: MotDePasseReinitialise,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        {
            name: "utilisateur-invite",
            path: '/utilisateur/invite',
            component: InviteView,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        {
            name: "utilisateur-connexion",
            path: '/utilisateur/connexion',
            component: ConnexionView,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        {
            name: "utilisateur-deconnexion",
            path: '/utilisateur/deconnexion',
            component: DeconnexionView,
            meta: {needAuth: true, reachableFrom: rights.lecteur}
        },
        {
            name: "utilisateur-lecture",
            path: '/utilisateur/lire/:id',
            component: UtilisateurView,
            meta: {needAuth: true, reachableFrom: rights.lecteur}
        },
        // endregion

        // region rechercher
        {
            name: "utilisateur-rechercher",
            path: '/rechercher',
            component: RechercheView,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        {
            name: "utilisateur-resultats",
            path: '/rechercher/resultats',
            component: ResultatsRecherche,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        {
            name: "recherche-bulletin",
            path: "/rechercher/bulletins",
            component: SearchBulletin,
            meta: {needAuth: false, reachableFrom: rights.contributeur}
        },
        {
            name: 'works',
            path: '/works/published/',
            component: WorkListView,
            meta: {needAuth: true, reachableFrom: rights.administrateur}
        },
        {
            name: 'works-item',
            path: '/works/published/:id',
            component: WorkAnnotationView,
            meta: {needAuth: true, reachableFrom: rights.administrateur}
        },
        // endregion
        // region import
        {
            name: "import-export",
            path: "/gestionnaire-importation",
            component: ImportExport,
            meta: {needAuth: true, reachableFrom: rights.administrateur}
        },
        {
            name: 'import-csv',
            path: "/importation",
            component: ImportTester2,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        {
            name: 'import-csv-globale',
            path: "/importation-globale",
            component: GlobalImport,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        {
            name: "import-lists",
            path: "/administrateur/imports",
            component: ImportList,
            meta: {needAuth: true, reachableFrom: rights.administrateur}
        },
        {
            name: "import-item",
            path: "/administrateur/imports/:id",
            component: ImportItem,
            meta: {needAuth: true, reachableFrom: rights.administrateur}
        },
        // endregion
        // region auteur
        {
            name: "auteur-creer",
            path: '/auteur/creer',
            component: CreationAuteur,
            meta: {needAuth: true, reachableFrom: rights.contributeur}
        },
        {
            name: "auteur-lire",
            path: '/auteur/lire/:id',
            component: LireAuteur,
            meta: {needAuth: false, reachableFrom: rights.contributeur}
        },
        {
            name: "auteur-liste",
            path: '/auteur/liste',
            component: ListeAuteur,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        // endregion
        // region référence bibliographique livre
        {
            name: "reference-livre-creer",
            path: '/reference-livre/creer',
            component: CreationReferenceLivre,
            meta: {needAuth: true, reachableFrom: rights.contributeur}
        },
        {
            name: "reference-livre-lire",
            path: '/reference-livre/lire/:id',
            component: LireReferenceLivre,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        {
            name: "reference-livre-liste",
            path: '/reference-livre/liste',
            component: ListeReferenceLivre,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        // endregion
        // region enregistrement
        {
            name: "enregistrement-creer",
            path: '/enregistrement/creer',
            component: EnregistrementView,
            meta: {needAuth: true, reachableFrom: rights.contributeur}
        },
        {
            name: "enregistrement-lire",
            path: '/enregistrement/lire/:id',
            component: LireEnregistrement,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        {
            name: "enregistrement-liste",
            path: '/enregistrement/liste',
            component: ListeEnregistrement,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        {
            name: "mots-clefs",
            path: '/mots-clefs',
            component: ListeMotsClefs,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        {
            name: "catalogue",
            path: '/catalogue',
            component: ListeEnregistrementComplet,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        {
            name: "new-catalogue-entry",
            path: '/catalogue/creer',
            component: CreationEnregistrementComplet,
            meta: {needAuth: true, reachableFrom: rights.contributeur}
        },
        {
            name: "read-catalogue-entry",
            path: '/catalogue/lire/:id',
            component: LireEnregistrementComplet,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        {
            name: "statistiques",
            path: '/statistiques',
            component: StatisticsDashboard,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },

        // endregion
        {
            name: "contact",
            path: "/contact",
            component: Contact,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        // region emprunt
        {
            name: "emprunt-livre",
            path: "/emprunt/livre",
            component: Emprunter,
            meta: {needAuth: true, reachableFrom: rights.gestionnaire}
        },
        {
            name: "emprunt-liste",
            path: '/emprunt/liste',
            component: ListeEmprunt,
            meta: {needAuth: true, reachableFrom: rights.contributeur}
        },
        {
            name: "emprunt-voir",
            path: '/emprunt/:id',
            component:  LireEmprunt,
            meta: {needAuth: true, reachableFrom: rights.lecteur}
        },
        // endregion
        // region diverse
        {
            name: "links-page",
            path: "/liens",
            component: LinkView,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        {
            name: "conception-page",
            path: "/conception",
            component: ConceptionView,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        {
            name: "changelog-page",
            path: "/notes-de-version",
            component: ChangelogView,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        // endregion
        // region admin
        {
            name: "administrateur",
            path: "/administrateur",
            component: AdminView,
            meta: {needAuth: true, reachableFrom: rights.editeur}
        },
        {
            name: "merge-authors",
            path: '/administrateur/fusionner-auteurs',
            component: MergeAuthors,
            meta: {needAuth: true, reachableFrom: rights.editeur}
        },
        {
            name: "log-events",
            path: "/evenements",
            component: LogEventListView,
            meta: {needAuth: true, reachableFrom: rights.administrateur}
        },
        {
            name: "gestionnaire",
            path: "/gestionnaire",
            component: GestionnaireView,
            meta: {needAuth: true, reachableFrom: rights.gestionnaire}
        },
        // {
        //     name: "log-events",
        //     path: "/evenements/lire/:id",
        // },
        // endregion
        // region dublin core
        {
            name: "dublin-core",
            path: "/dublin-core",
            component: ListDublinCoreEntriesView
        },
        {
            name: "dublin-core-entry",
            path: "/dublin-core/:id",
        },
        // endregion
        // region ark
        {
            name: "",
            path: "/ark:/:naan/:ark_name",
            component: ArkView,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        // endregion
        // region
        // {
        //     name: "image-manager",
        //     path: "/gestionnaire-images",
        //     component: ImageManager
        // },
        // endregion
        {
            name: "",
            path: "/adhesion-sat",
            component: SatSubscription
        },
        // region page not found
        {
            name: "not-found",
            path: "/:pathMatch(.*)*",
            component: PageNotFoundView,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        }
        // endregion
    ],
});

router.beforeEach(function (to, from, next) {
    if(to.meta.needAuth) {
        if(!store.state.connectionInfo.token) {
            next({
                name: 'utilisateur-connexion',
                query: {
                    redirect: to.fullPath
                }
            });
            return;
        }
        const isValid = isValidJwt(store.state.connectionInfo.token);
        if(isValid) {
            if(to.meta.reachableFrom.index <= store.getters.getUserRight) {
                next();
            } else {
                next({
                    name: 'utilisateur-connexion',
                });
                // if(from.query.redirect) {
                //     console.log()
                //     next(from.query.redirect);
                // } else {
                //     next({
                //     name: 'utilisateur-connexion',
                // });
                // }
            }
        } else {
            store.commit("disconnect");
            next({
                name: 'utilisateur-connexion',
                query: {
                    redirect: to.fullPath
                }
            });
        }
    } else {
        next();
        // if(from.query.redirect) {
        //     console.log();
        //     next(from.query.redirect);
        // } else {
        //     next();
        // }
    }
});
export default router;