

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
        this.selectedReference = {value: -1, text: ""};
        this.description = "";
        this.cote = "";
        this.annee = "";
        this.nb_exemplaire_supp = 0;
        this.provenance =  "";
        this.mots_clef = "";

        this.reference = {value: -1, text: ""};
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
        this.file = "";
        this.selectedMethod = "";
        this.startDate = "";
        this.endDate = "";
        this.status = "";
        this.idUser = -1;
    }
}