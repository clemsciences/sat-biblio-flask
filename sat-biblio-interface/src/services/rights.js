/**
 * Un lecteur peut lire la liste des auteurs, des références bibliographiques et des enregistrements.
 * Un contributeur peut ajouter de nouvelles entrées.
 * Un éditeur peut modifier des entrées. Il peut aussi exporter les données dans des fichiers.
 * Un gestionnaire gère les droits des lecteurs, des contributeurs et des éditeurs.
 * L'administrateur a accès à la base de données.
 *
 */
export const rights = {
    lecteur: {index: 1, string: "lecteur"},
    contributeur: {index: 2, string: "contributeur"},
    editeur: {index: 3, string: "éditeur"},
    gestionnaire: {index: 4, string: "gestionnaire"},
    administrateur: {index: 5, string: "adminstrateur"}
}

function canDo(right, rightIndex) {
    return right.index <= rightIndex;
}

export function getRightString(rightIndex) {
    let selectedRight = rights.lecteur.string;

    for( const [key, value] of Object.entries(rights)) {
        console.log(key, value);
        if(rightIndex === value.index) {
            selectedRight = value.string;
        }
    }
    return selectedRight;
}

/**
 * 2
 * @param rightIndex
 * @returns {boolean}
 */
export function canContribute(rightIndex) {
    return canDo(rights.contributeur, rightIndex);
}

/**
 * 5
 * @param rightIndex
 * @returns {boolean}
 */
export function isAdmin(rightIndex) {
    return canDo(rights.administrateur, rightIndex);
}


/**
 * 4
 * @param rightIndex
 * @returns {boolean}
 */
export function canManage(rightIndex) {
    return canDo(rights.gestionnaire, rightIndex);
}

/**
 * 3
 * @param rightIndex
 * @returns {boolean}
 */
export function canEdit(rightIndex) {
    return canDo(rights.editeur, rightIndex);
}
