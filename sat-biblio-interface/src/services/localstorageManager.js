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
        return JSON.parse(localStorage.getItem(SAT_BIBLIO_INFO) || {connected: false})
    }
}

export default localStorageManager;