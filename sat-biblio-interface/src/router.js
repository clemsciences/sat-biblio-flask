

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

Vue.use(VueRouter);

let router = new VueRouter({
    mode: "history",
    routes: [
        {
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
            path: '/utilisateur/creer',
            component: CreationUtilisateur,
            needAuth: false
        },
        {
            path: '/utilisateur/enregistre',
            component: UtilisateurEnregistre,
            needAuth: false
        },
        {
            path: '/utilisateur/mot-de-passe-oublie',
            component: MotDePasseOublie,
            needAuth: false
        },
        {
            path: '/utilisateur/reinitialiser-mot-de-passe',
            component: ReinitialisationMotDePasse,
            needAuth: false
        },
        {
            path: '/utilisateur/mot-de-passe-email',
            component: MotDePasseEmail,
            needAuth: false
        },
        {
            path: '/utilisateur/mot-de-passe-reinitialise',
            component: MotDePasseReinitialise,
            needAuth: false
        },
        {
            path: '/utilisateur/invite',
            component: Invite,
            needAuth: false
        },
        {
            path: '/utilisateur/connexion',
            component: Connexion,
            needAuth: false
        },
        {
            path: '/utilisateur/deconnexion',
            component: Deconnexion,
            needAuth: false
        },
        // endregion

        // region rechercher
        {
            path: '/rechercher',
            component: Recherche,
            needAuth: false
        },
        {
            path: '/rechercher/resultats',
            component: ResultatsRecherche,
            needAuth: false
        },
        // endregion
        // region auteur
        {
            path: '/auteur/creer',
            component: CreationAuteur,
            needAuth: true
        },
        {
            path: '/auteur/lire/:id',
            component: LireAuteur,
            needAuth: false
        },
        {
            path: '/auteur/liste',
            component: ListeAuteur,
            needAuth: false
        },
        // endregion
        // region référence bibliographique livre
        {
            path: '/reference-livre/creer',
            component: CreationReferenceLivre,
            needAuth: true
        },
        {
            path: '/reference-livre/lire/:id',
            component: LireReferenceLivre,
            needAuth: false
        },
        {
            path: '/reference-livre/liste',
            component: ListeReferenceLivre,
            needAuth: false
        },
        // endregion
        // region enregistrement
        {
            path: '/enregistrement/creer',
            component: Enregistrement,
            needAuth: true
        },
        {
            path: '/enregistrement/lire/:id',
            component: LireEnregistrement,
            needAuth: false
        },
        {
            path: '/enregistrement/liste',
            component: ListeEnregistrement,
            needAuth: false
        },
        // endregion
        {
            path: "/contact",
            component: Contact,
            needAuth: false
        },
        // region emprunt
        {
            path: "/emprunt/livre",
            component: Emprunter,
            needAuth: true
        },
        {
            path: '/emprunt/liste',
            component: ListeEmprunt,
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