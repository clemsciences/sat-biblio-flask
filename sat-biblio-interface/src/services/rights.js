
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

export function canContribute(rightIndex) {
    return canDo(rights.contributeur, rightIndex);
}

export function isAdmin(rightIndex) {
    return canDo(rights.administrateur, rightIndex);
}

export function canManage(rightIndex) {
    return canDo(rights.gestionnaire, rightIndex);
}

export function canEdit(rightIndex) {
    return canDo(rights.editeur, rightIndex);
}





