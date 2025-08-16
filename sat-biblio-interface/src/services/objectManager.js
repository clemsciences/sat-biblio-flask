

export class Author {
    constructor() {
        this.clear();
    }
    getPrettyForm() {
        return `${this.family_name} (${this.first_name})`;
    }

    clear() {
        this.first_name = '';
        this.family_name = '';
    }
}

export class BookReference {
    constructor() {
        this.clear()
    }
    // getPrettyForm() {
        // let authorPrettyForm = "";
        // this.selectedAuthors.forEach(
        //     (value) => {
        //         authorPrettyForm = authorPrettyForm + value.getPrettyForm();
        //     }
        // )
    // }

    clear() {
        this.selectedAuthors = [];
        this.authorsForm = "";
        this.titre = "";
        this.lieu_edition = "";
        this.editeur = "";
        this.annee = "";
        this.nb_page = "";
        this.valide = false;
        this.description = "";
        this.ark_name = "";

    }
}

export class Record {
    constructor() {
        this.clear();
    }

    clear() {
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
        this.row = "";
        this.ark_name = "";
    }
}

export class BookRecordWithReference {
    constructor() {
        this.clear();
    }

    clear() {
        this.authors = [];
        this.selectedAuthors = [];
        // authors as mentioned in the book
        this.authorsForm = "";
        // title
        this.titre = "";
        // where it was published
        this.lieu_edition = "";
        // publisher
        this.editeur = "";
        // year of publication
        this.publication_annee = "";
        this.nb_page = "";
        this.valide = false;
        this.reference_description = "";
        // ARK name of the reference
        this.reference_ark_name = "";
        this.record_description = "";
        // id of the book in the library
        this.cote = "";

        this.annee_entree = "";
        // how many books of it do we have.
        this.nb_exemplaire_supp = 0;
        // where the book comes from
        this.provenance =  "";
        // key words
        this.aide_a_la_recherche = "";
        // ARK name of the record
        this.record_ark_name = "";

        this.referenceId = -1;
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

export class DublinCore {
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