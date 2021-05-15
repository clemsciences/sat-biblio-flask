const SAT_BIBLIO_INFO = "SatBiblioInfo";



let localStorageManager = {
    updateSessionInfo(newValue) {
        try {
            const dataJson = JSON.stringify(newValue)
            localStorage.setItem(SAT_BIBLIO_INFO, dataJson);
        } catch (error) {
            console.error(error);
            throw error;
        }
    },
    getSessionInfo() {
        if(localStorage.getItem(SAT_BIBLIO_INFO)) {
            return JSON.parse( localStorage.getItem(SAT_BIBLIO_INFO))
        } else {
            return {};
        }
    },
    removeSessionInfo() {
        localStorage.clear();
    }
}

export default localStorageManager;