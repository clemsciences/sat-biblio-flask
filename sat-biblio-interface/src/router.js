

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

Vue.use(VueRouter);

export default new VueRouter({
    mode: "history",
    routes: [
        {
            path: '/recherche',
            component: Recherche
        },
        {
            path: '',
            component: Accueil
        },
        {
            path: '/export',
            component: Export
        },
        // region utilisateurs
        {
            path: '/utilisateur/creer',
            component: CreationUtilisateur
        },
        {
            path: '/utilisateur/enregistre',
            component: UtilisateurEnregistre
        },
        {
            path: '/utilisateur/mot-de-passe-oublie',
            component: MotDePasseOublie
        },
        {
            path: '/utilisateur/reinitialiser-mot-de-passe',
            component: ReinitialisationMotDePasse
        },
        {
            path: '/utilisateur/mot-de-passe-email',
            component: MotDePasseEmail
        },
        {
            path: '/utilisateur/mot-de-passe-reinitialise',
            component: MotDePasseReinitialise
        },
        {
            path: '/utilisateur/invite',
            component: Invite
        },
        {
            path: '/utilisateur/connexion',
            component: Connexion
        },
        {
            path: '/utilisateur/deconnexion',
            component: Deconnexion
        },
        // endregion

        // region rechercher
        {
            path: '/rechercher',
            component: Recherche
        },
        {
            path: '/rechercher/resultats',
            component: ResultatsRecherche
        },
        // endregion
        // region auteur
        {
            path: '/auteur/creer',
            component: CreationAuteur
        },
        {
            path: '/auteur/creer',
            component: CreationAuteur
        },
        {
            path: '/auteur/lire',
            component: LireAuteur
        },
        // endregion
        // region référence bibliographique livre
        {
            path: '/reference-livre/creer',
            component: CreationReferenceLivre
        },
        {
            path: '/reference-livre/lire',
            component: LireReferenceLivre
        },
        {
            path: '/reference-livre/liste',
            component: ListeReferenceLivre
        },
        // endregion
        // region enregistrement
        {
            path: '/enregistrement/creer',
            component: Enregistrement
        },
        {
            path: '/enregistrement/lire',
            component: LireEnregistrement
        },
        {
            path: '/enregistrement/liste',
            component: ListeEnregistrement
        },
        // endregion
        {
            path: "/contact",
            component: Contact
        },
        // region emprunt
        {
            path: "/emprunt/livre",
            component: Emprunter
        },
        {
            path: '/emprunt/liste',
            component: ListeEmprunt
        }
        // endregion
    ]

})