

/**
 *
 * @param {Author} author
 * @returns {string}
 */
export function renderAuthor(author) {
    return `${author.family_name} (${author.first_name})`
}

/**
 *
 * @param {BookReference} reference
 * @returns {string}
 */
export function renderReference(reference) {
    let result = "";
    if(typeof reference.selectedAuthors !== "undefined") {
        reference.selectedAuthors.forEach((value) => {
            result += `${renderAuthor(value)},`;
        });
    }
    result += `${reference.titre}, ${reference.lieu_edition}, ${reference.editeur}, ${reference.annee}, ${reference.nb_page}`;
    return result;
}

/**
 *
 * @param {Record} record
 */
export function renderRecord(record) {
    let result = "";
    result += `${record.cote}, `
    result += renderReference(record.selectedReference);
    return result;
}