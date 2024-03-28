

export class Author {
    constructor() {
        this.first_name = '';
        this.family_name = '';
    }

    getPrettyForm() {
        return `${this.family_name} (${this.first_name})`;
    }
}

export class BookReference {
    constructor() {
        this.selectedAuthors = [];
        this.titre = "";
        this.lieu_edition = "";
        this.editeur = "";
        this.annee = "";
        this.nb_page = "";
        this.valide = false;
        this.description = "";
    }
    // getPrettyForm() {
        // let authorPrettyForm = "";
        // this.selectedAuthors.forEach(
        //     (value) => {
        //         authorPrettyForm = authorPrettyForm + value.getPrettyForm();
        //     }
        // )
    // }
}

export class Record {
    constructor() {
        this.selectedReference = new BookReference;
        this.selectedReference.value = -1;
        this.selectedReference.text = "";
        this.description = "";
        this.cote = "";
        this.annee = "";
        this.nb_exemplaire_supp = 0;
        this.provenance =  "";
        this.aide_a_la_recherche = "";

        this.reference = new BookReference();
        this.reference.value = -1;
        this.reference.text = "";
        this.suggestedReferences = [];
        this.valid = false;
        this.row = ""
    }
}

export class ImportItem {
    constructor() {
        this.title = "";
        this.description = "";
        this.datetime = "";
        this.filename = "";
        this.selectedMethod = "";
        this.startDate = "";
        this.endDate = "";
        this.status = "";
        this.idUser = -1;
    }
    fromServer(importData) {
        this.title = importData.title ?? "Aucun titre";
        this.description = importData.description ?? "Aucune description";
        this.filename = importData.filename ?? "Aucun fichier";
        this.startDate = importData.start_date ?? null;
        this.endDate = importData.end_date ?? null;
        this.selectedMethod = importData.selected_method ?? "";
        this.status = importData.status ?? "";
        this.idUser = importData.id_user ?? -2;
    }
}

export class User {
    constructor() {
        this.firstName = "";
        this.familyName = "";
        this.right = 0;
        this.dateInscription = "";
        this.email = ""
    }

    fromServer(serverData) {
        this.firstName = serverData.first_name;
        this.familyName = serverData.family_name;
        this.right = serverData.right;
        this.dateInscription = serverData.date_inscription;
        this.email = serverData.email;
    }
}

export class DublincCore {
    constructor() {
        this.title = "";
        this.date = "";
        this.subject = "";
        this.language = "";
        this.description = "";
        this.source = "";
        this.creator = "";
        this.publisher = "";
        this.contributor = "";
        this.type = "";
        this.format = "";
        this.identifier = "";
        this.relation = "";
        this.coverage = "";
        this.rights = "";
    }
}