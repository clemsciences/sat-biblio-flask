

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
    if(reference) {
        if (typeof reference.selectedAuthors !== "undefined") {
            for (let value of reference.selectedAuthors) {
                result += `${renderAuthor(value)},`;
            }
        }

        if (result.length === 0) {
            console.log(result.length === 0);
            result += "[anonyme]"
        }
        result += `${renderTitle(reference)}, ${renderEditor(reference)}, ${renderYear(reference)} ${renderPages(reference)}`;
    }
    return result;
}

// export function renderAuthor(reference) {
//   if (reference.family_name.length === 0 && reference.first_name.length === 0) {
//     return "<i>auteur</i>"
//   }
//   return `${reference.family_name} (${reference.first_name})`
// }
/**
 *
 * @param {BookReference} reference
 * @returns {string|*|string}
 */
export function renderTitle(reference) {
  if(reference.titre.length === 0) {
    return "<Titre inconnu>";
  }
  return reference.titre;
}

/**
 *
 * @param {BookReference} reference
 * @returns {string}
 */
export function renderEditor(reference) {
  let lieu_edition = reference.lieu_edition;
  let editeur = reference.editeur;
  if(lieu_edition.length === 0) {
    lieu_edition = "s. l.";
  }
  if(editeur.length === 0) {
    editeur = "s. ed.";
  }
  return `${lieu_edition}, ${editeur}`
}

/**
 *
 * @param {BookReference} reference
 * @returns {string}
 */
export function renderYear(reference) {
  if(reference.year) {
    return `${reference.year}`;
  }
  return "s. d."
}

/**
 *
 * @param {BookReference} reference
 * @returns {string}
 */
export function renderPages(reference) {
  if(typeof reference.nb_page === "number") {
    if(reference.nb_page === 0) {
      return '';
    }
    return `,${reference.nb_page } p.`;
  } else {
    if (reference.nb_page.length === 0) {
      return '';
    }
    return `,${reference.nb_page} p.`;
  }
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