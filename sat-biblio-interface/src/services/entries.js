

export const entries = {
    author: {string: "auteur"},
    reference: {string: "référence"},
    record: {string: "enregistrement"},
    user: {string: "utilisateur"},
}


export function goToEntryView(id, entryType) {
    switch (entryType) {
        case entries.author.string:
            return `/auteur/lire/${id}`;
        case entries.reference.string:
            return `/reference-livre/lire/${id}`;
        case entries.record.string:
            return `/enregistrement/lire/${id}`;
        case entries.user.string:
            return `/utilisateur/lire/${id}`;
        default:
            return "";

    }

}
