

import Vue from "vue";
import VueRouter from "vue-router";
import Recherche from "@/components/recherche/Recherche";
import Accueil from "@/components/Accueil";
import Export from "@/components/export/Export";
import CreationUtilisateur from "@/components/utilisateur/CreationUtilisateur";
import UtilisateurEnregistre from "@/components/utilisateur/UtilisateurEnregistre";
import MotDePasseOublie from "@/components/utilisateur/MotDePasseOublie";
import ReinitialisationMotDePasse from "@/components/utilisateur/ReinitialisationMotDePasse";
import MotDePasseEmail from "@/components/utilisateur/MotDePasseEmail";
import MotDePasseReinitialise from "@/components/utilisateur/MotDePasseReinitialise";
import Invite from "@/components/utilisateur/Invite";
import Connexion from "@/components/utilisateur/Connexion";
import Deconnexion from "@/components/utilisateur/Deconnexion";
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

Vue.use(VueRouter);

let router = new VueRouter({
    mode: "history",
    routes: [
        {
            name: "recherche",
            path: '/recherche',
            component: Recherche,
            needAuth: false
        },
        {
            path: '',
            component: Accueil,
            needAuth: false,
            name: 'accueil'
        },
        {
            path: '/exporter',
            component: Export,
            needAuth: true
        },
        // region utilisateurs
        {
            name: "utilisateur-creer",
            path: '/utilisateur/creer',
            component: CreationUtilisateur,
            needAuth: false
        },
        {
            name: "utilisateur-enregistre",
            path: '/utilisateur/enregistre',
            component: UtilisateurEnregistre,
            needAuth: false
        },
        {
            name: "utilisateur-mot-de-passe-oublie",
            path: '/utilisateur/mot-de-passe-oublie',
            component: MotDePasseOublie,
            needAuth: false
        },
        {
            name: "utilisateur-reinitialiser-mot-de-passe",
            path: '/utilisateur/reinitialiser-mot-de-passe',
            component: ReinitialisationMotDePasse,
            needAuth: false
        },
        {
            name: "utilisateur-mot-de-passe-oublie-email",
            path: '/utilisateur/mot-de-passe-email',
            component: MotDePasseEmail,
            needAuth: false
        },
        {
            name: 'utilisateur-mot-de-passe-reinitialise',
            path: '/utilisateur/mot-de-passe-reinitialise',
            component: MotDePasseReinitialise,
            needAuth: false
        },
        {
            name: "utilisateur-invite",
            path: '/utilisateur/invite',
            component: Invite,
            needAuth: false
        },
        {
            name: "utilisateur-connexion",
            path: '/utilisateur/connexion',
            component: Connexion,
            needAuth: false
        },
        {
            name: "utilisateur-deconnexion",
            path: '/utilisateur/deconnexion',
            component: Deconnexion,
            needAuth: false
        },
        // endregion

        // region rechercher
        {
            name: "utilisateur-rechercher",
            path: '/rechercher',
            component: Recherche,
            needAuth: false
        },
        {
            name: "utilisateur-resultats",
            path: '/rechercher/resultats',
            component: ResultatsRecherche,
            needAuth: false
        },
        // endregion
        // region auteur
        {
            name: "auteur-creer",
            path: '/auteur/creer',
            component: CreationAuteur,
            needAuth: true
        },
        {
            name: "auteur-lire",
            path: '/auteur/lire/:id',
            component: LireAuteur,
            needAuth: false
        },
        {
            name: "auteur-liste",
            path: '/auteur/liste',
            component: ListeAuteur,
            needAuth: false
        },
        // endregion
        // region référence bibliographique livre
        {
            name: "reference-livre-creer",
            path: '/reference-livre/creer',
            component: CreationReferenceLivre,
            needAuth: true
        },
        {
            name: "reference-livre-lire",
            path: '/reference-livre/lire/:id',
            component: LireReferenceLivre,
            needAuth: false
        },
        {
            name: "reference-livre-liste",
            path: '/reference-livre/liste',
            component: ListeReferenceLivre,
            needAuth: false
        },
        // endregion
        // region enregistrement
        {
            name: "enregistrement-creer",
            path: '/enregistrement/creer',
            component: Enregistrement,
            needAuth: true
        },
        {
            name: "enregistrement-lire",
            path: '/enregistrement/lire/:id',
            component: LireEnregistrement,
            needAuth: false
        },
        {
            name: "enregistrement-liste",
            path: '/enregistrement/liste',
            component: ListeEnregistrement,
            needAuth: false
        },
        // endregion
        {
            name: "contact",
            path: "/contact",
            component: Contact,
            needAuth: false
        },
        // region emprunt
        {
            name: "emprunt-livre",
            path: "/emprunt/livre",
            component: Emprunter,
            needAuth: true
        },
        {
            name: "emprunt-liste",
            path: '/emprunt/liste',
            component: ListeEmprunt,
            needAuth: true
        },
        {
            name: "administrateur",
            path: "/administrateur",
            component: Admin,
            needAuth: true,
        },
        {
            name: "gestionnaire",
            path: "/gestionnaire",
            component: Gestionnaire,
            needAuth: true
        }
        // endregion
    ],
});
router.beforeEach((to, from, next) => {
        if(to.needAuth) {
            next({
                name: 'accueil',
                query: {
                    redirect: to.fullPath
                }
            })
        } else {
            next();
        }
})
export default router;