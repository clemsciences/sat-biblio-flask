

import Vue from "vue";
import VueRouter from "vue-router";
import Recherche from "@/components/recherche/Recherche";
import Accueil from "@/components/Accueil";
import Export from "@/components/export/Export";
import CreationUtilisateur from "@/components/utilisateur/CreationUtilisateur";
import UtilisateurEnregistre from "@/components/utilisateur/UtilisateurEnregistre";
import MotDePasseOublie from "@/components/mot_de_passe/MotDePasseOublie";
import ReinitialisationMotDePasse from "@/components/mot_de_passe/ReinitialisationMotDePasse";
import MotDePasseEmail from "@/components/mot_de_passe/MotDePasseEmail";
import MotDePasseReinitialise from "@/components/mot_de_passe/MotDePasseReinitialise";
import Invite from "@/components/utilisateur/Invite";
import Connexion from "@/components/connexion/Connexion";
import Deconnexion from "@/components/connexion/Deconnexion";
import ResultatsRecherche from "@/components/recherche/ResultatsRecherche";
import CreationAuteur from "@/components/auteur/CreationAuteur";
import LireAuteur from "@/components/auteur/LireAuteur";
import CreationReferenceLivre from "@/components/reference_livre/CreationReferenceLivre";
import LireReferenceLivre from "@/components/reference_livre/LireReferenceLivre";
import Enregistrement from "@/components/enregistrement/Enregistrement";
import LireEnregistrement from "@/components/enregistrement/LireEnregistrement";
import ListeEnregistrement from "@/components/enregistrement/ListeEnregistrement";
import ListeReferenceLivre from "@/components/reference_livre/ListeReferenceLivre";
import Contact from "@/components/Contact";
import Emprunter from "@/components/emprunt/Emprunter";
import ListeEmprunt from "@/components/emprunt/ListeEmprunt";
import ListeAuteur from "@/components/auteur/ListeAuteur";
import Admin from "./components/admin/Admin";
import Gestionnaire from "./components/admin/Gestionnaire";
import PageNotFound from "@/components/PageNotFound";
import {isValidJwt} from "@/services/authentication";
import {rights} from "@/services/rights";
import store from "@/store";
import Utilisateur from "@/components/utilisateur/Utilisateur";
// import ImportTester from "@/components/import/ImportTester";
import ImportTester2 from "@/components/import/ImportTester2";
import LireEmprunt from "@/components/emprunt/LireEmprunt";
import LogEventList from "@/components/log/LogEventList";
import GlobalImport from "@/components/import/GlobalImport";
import ListDublinCoreEntries from "@/components/entrees/ListDublinCoreEntries";
// import ImageManager from "@/components/images/ImageManager";
import ImportExport from "@/components/import_export/ImportExport";

Vue.use(VueRouter);

let router = new VueRouter({
    mode: "history",
    routes: [
        {
            name: "recherche",
            path: '/recherche',
            component: Recherche,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        {
            path: '/',
            component: Accueil,
            name: 'accueil',
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        {
            path: '/exporter',
            component: Export,
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
            component: Invite,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        {
            name: "utilisateur-connexion",
            path: '/utilisateur/connexion',
            component: Connexion,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        {
            name: "utilisateur-deconnexion",
            path: '/utilisateur/deconnexion',
            component: Deconnexion,
            meta: {needAuth: true, reachableFrom: rights.lecteur}
        },
        {
            name: "utilisateur-lecture",
            path: '/utilisateur/lire/:id',
            component: Utilisateur,
            meta: {needAuth: true, reachableFrom: rights.lecteur}
        },
        // endregion

        // region rechercher
        {
            name: "utilisateur-rechercher",
            path: '/rechercher',
            component: Recherche,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        {
            name: "utilisateur-resultats",
            path: '/rechercher/resultats',
            component: ResultatsRecherche,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        },
        // endregion
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
            component: Enregistrement,
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
        // region admin
        {
            name: "administrateur",
            path: "/administrateur",
            component: Admin,
            meta: {needAuth: true, reachableFrom: rights.administrateur}
        },
        {
            name: "log-events",
            path: "/evenements",
            component: LogEventList,
            meta: {needAuth: true, reachableFrom: rights.administrateur}
        },
        {
            name: "gestionnaire",
            path: "/gestionnaire",
            component: Gestionnaire,
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
            component: ListDublinCoreEntries
        },
        {
            name: "dublin-core-entry",
            path: "/dublin-core/:id",
        },
        // endregion
        // region page not found
        {
            name: "not-found",
            path: "*",
            component: PageNotFound,
            meta: {needAuth: false, reachableFrom: rights.lecteur}
        }
        // endregion
    ],
});

router.beforeEach(function (to, from, next) {
    if(to.meta.needAuth) {
        if(!store.state.connectionInfo.token) {
            next({
                name: 'accueil',
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
                    name: 'accueil',
                });
            }
        } else {
            store.commit("disconnect");
            next({
                name: 'accueil',
                query: {
                    redirect: to.fullPath
                }
            });
        }
    } else {
        next();
    }
})
export default router;