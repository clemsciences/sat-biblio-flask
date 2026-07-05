

/**
 *
 * @param {Author} author
 * @returns {string}
 */
export function renderAuthor(author) {
    if(author.family_name === '[collectif] (-)') {
        return `[collectif] (-)`;
    } else if (author.family_name === '[anonyme] (-)') {
        return `[anonyme] (-)`;
    }
    return `${author.family_name} (${author.first_name})`;
}

/**
 *
 * @param {BookReference} reference
 * @returns {string}
 */
export function renderReference(reference) {
    let result = "";
    if(reference) {
        if(reference.authorsForm && reference.authorsForm.length > 0) {
            result += reference.authorsForm;
        } else if (reference.selectedAuthors && reference.selectedAuthors.length > 0) {
            result += reference.selectedAuthors.map(renderAuthor).join(", ") + ", ";
        } else if (reference.authors && reference.authors.length > 0) {
            result += reference.authors.map(renderAuthor).join(", ") + ", ";
        }

        if (result.length === 0) {
            result += "[anonyme], "
        }
        result += `${renderTitle(reference)}, ${renderEditor(reference)}, ${renderYear(reference)}${renderPages(reference)}`;
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
  const annee = reference.annee ?? reference.publication_annee;
  if(annee) {
    return `${annee}`;
  }
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
    if(reference.nb_page == 0) {
      return '';
    } else if (reference.nb_page == -1) {
        return '';
    }
  if(typeof reference.nb_page === "number") {
    return `, ${reference.nb_page } p.`;
  } else if(typeof reference.nb_page === "string") {
    if (reference.nb_page.length === 0) {
      return '';
    } else if(reference.nb_page)
    return `, ${reference.nb_page} p.`;
  }
  return '';
}

/**
 *
 * @param {Record} record
 */
export function renderRecord(record) {
    let result = "";
    result += `${record.cote}, `
    if(record.selectedReference.value !== -1) {
        result += renderReference(record.selectedReference);
    } else if(record.reference.value !== -1) {
        result += renderReference(record.reference);
    }
    return result;
}