import axios from 'axios';
const api = axios.create({
    baseURL: process.env.VUE_APP_SITE_API_URL,
    withCredentials: true,
    headers: {
        "Content-Type": "application/json",
        // 'Access-Control-Allow-Origin': 'https://bht.societearcheotouraine.fr'
    }
})
// axios.defaults.baseURL = process.env.VUE_APP_SITE_API_URL;
// axios.defaults.withCredentials = true;
// axios.defaults.headers.post['Access-Control-Allow-Origin'] = 'https://bht.societearcheotouraine.fr';


// region users
export function connectUser(args) {
  return api.post("/users/connect/", args);
}

export function createUser(formData) {
  return api.post('/users/create/', formData);
}

export function disconnectUser() {
  return api.get("/users/disconnect/");
}

export function haveForgottenPassword(formData) {
  return api.post("/users/forgotten-password/", formData);
}

export function recreatePassword(currentPassword, newPassword) {
  return api.post('/users/new-password/', {currentPassword, newPassword});
}

export function confirmUserRegistration(inscriptionToken, emailAddress) {
  return api.get(`/users/confirm/${inscriptionToken}/?email=${emailAddress}`);
}

export function checkUserLogin() {
  return api.post('/users/check_login/');
}

export function searchNearUsers(params) {
  return api.get(`/users/search-near/?${params}`)
}

export function retrieveUsers(params, token) {
  return api.get(`/users/${params}`, { headers: { Authorization: `Bearer ${token}` } });
}

export function getUsersCount(params, token) {
  return api.get(`/users/count/${params}`, { headers: { Authorization: `Bearer ${token}` } });
}

export function retrieveUser(id, token) {
  return api.get(`/users/${id}/`, { headers: { Authorization: `Bearer ${token}` } });
}

export function updateUser(id, user, token) {
  return api.put(`/users/${id}/`, user, { headers: { Authorization: `Bearer ${token}` } });
}

export function deleteUser(id, token) {
  return api.delete(`/users/${id}/`, { headers: { Authorization: `Bearer ${token}` } });
}

export function resendConfirmationEmail(id, token) {
  return api.get(`/users/${id}/resend-confirmation-email/`, { headers: { Authorization: `Bearer ${token}` } });
}

// endregion

// region auteurs
export function createAuthor(author, token) {
  return api.post("/authors/", author, { headers: { Authorization: `Bearer ${token}` } });
}

export function retrieveAuthors(params) {
  return api.get(`/authors/${params}`);
}

export function retrieveNotValidatedAuthors(params) {
  return retrieveAuthors(`?valid=0&${params}`);
}

export function retrieveAuthor(authorId) {
  return api.get(`/authors/${authorId}/`);
}

export function updateAuthor(authorId, author, token) {
  return api.put(`/authors/${authorId}/`, author, { headers: { Authorization: `Bearer ${token}` } });
}

export function deleteAuthor(authorId, token) {
  return api.delete(`/authors/${authorId}/`, { headers: { Authorization: `Bearer ${token}` } });
}

export function getAuthorsCount(params) {
  return api.get(`/authors/count/${params}`);
}

export function getNotValidatedAuthorsCount(params) {
  return getAuthorsCount(`?valid=0&${params}`);
}

export function searchNearAuthors(params) {
  return api.get(`/authors/search-near/?${params}`);
}

export function searchAuthors(data) {
  return api.post("/authors/search/", data);
}

export function mergeAuthors(idKeep, idDelete, token) {
  return api.post("/authors/merge/", {id_keep: idKeep, id_delete: idDelete}, { headers: { Authorization: `Bearer ${token}` } });
}

export function getAuthorDuplicates(token) {
  return api.get("/authors/duplicates/", { headers: { Authorization: `Bearer ${token}` } });
}


export function getEntryListAssociatedToAuthor(authorId, params) {
  return api.get(`/authors/${authorId}/entries/?${params}`)
}

export function getEntryListAssociatedToAuthorCount(authorId, params) {
  if(params) {
      return api.get(`/authors/${authorId}/entries/count/?${params}`);
  } else {
    return api.get(`/authors/${authorId}/entries/count/`);
  }
}

// endregion

// region references

export function createBookReference(bookReference, token) {
  return api.post("/book-references/", bookReference, { headers: { Authorization: `Bearer ${token}` } });
}

export function retrieveBookReferences(params) {
  return api.get(`/book-references/${params}`);
}

export function retrieveNotValidatedBookReferences(params) {
  return retrieveBookReferences(`?valid=0&${params}`);
}

export function retrieveBookReference(bookReferenceId) {
  return api.get(`/book-references/${bookReferenceId}/`);
}

export function updateBookReference(bookReferenceId, bookReference, token) {
  return api.put(`/book-references/${bookReferenceId}/`, bookReference, { headers: { Authorization: `Bearer ${token}` } });
}

export function deleteBookReference(bookReferenceId, token) {
  return api.delete(`/book-references/${bookReferenceId}/`, { headers: { Authorization: `Bearer ${token}` } });
}

export function getBookReferencesCount(params) {
  return api.get(`/book-references/count/${params}`);
}

export function getNotValidatedBookReferencesCount(params) {
  return getBookReferencesCount(`?valid=0&${params}`);
}

export function searchNearBookReferences(params) {
  return api.get(`/book-references/search-near/?${params}`)
}

export function getEntryListAssociatedToReference(bookReference, params) {
  return api.get(`/book-references/${bookReference}/entries/?${params}`)
}

export function getEntryListAssociatedToReferenceCount(bookReference, params) {
  if(params) {
    return api.get(`/book-references/${bookReference}/entries/count/?${params}`);
  } else {
    return api.get(`/book-references/${bookReference}/entries/count/`);
  }
}

// endregion

// region records

export function createBookRecord(bookRecord, token) {
  return api.post("/book-records/", bookRecord, { headers: { Authorization: `Bearer ${token}` } });
}

export function retrieveBookRecords(params) {
  return api.get(`/book-records/${params}`);
}

export function retrieveNotValidatedBookRecords(params) {
  return retrieveBookRecords(`?valid=0&${params}`);
}

export function retrieveBookRecord(bookRecordId) {
  return api.get(`/book-records/${bookRecordId}/`);
}

export function updateBookRecord(bookRecordId, bookRecord, token) {
  return api.put(`/book-records/${bookRecordId}/`, bookRecord, { headers: { Authorization: `Bearer ${token}` } });
}

export function deleteBookRecord(bookRecordId, token) {
  return api.delete(`/book-records/${bookRecordId}/`, { headers: { Authorization: `Bearer ${token}` } });
}

export function getBookRecordsCount(params) {
  return api.get(`/book-records/count/${params}`);
}

export function getNotValidatedBookRecordsCount(params) {
  return getBookRecordsCount(`?valid=0&${params}`);
}

export function searchNearBookRecords(params) {
  return api.get(`/book-records/search-near/?${params}`);
}

export function getBookRecordsKeywords() {
  return api.get("/book-records/keywords/");
}

export function getEntryListAssociatedToBookRecords(bookRecordId, params) {
  return api.get(`/book-records/${bookRecordId}/entries/?${params}`);
}

export function getEntryListAssociatedToBookRecordsCount(bookRecordId, params) {
  if(params) {
    return api.get(`/book-records/${bookRecordId}/entries/count/?${params}`);
  } else {
    return api.get(`/book-records/${bookRecordId}/entries/count/`);
  }
}

// endregion

// region records with reference
/**
 *
 * @param {BookRecordWithReference} bookRecordWithReference
 * @param {String} token
 * @returns {Promise<AxiosResponse<any>>}
 */
export function createBookRecordWithReference(bookRecordWithReference, token) {
  return api.post("/book-records-with-reference/", bookRecordWithReference, { headers: { Authorization: `Bearer ${token}` } });
}

/**
 *
 * @param {Object} params
 * @returns {Promise<AxiosResponse<any>>}
 */
export function retrieveBookRecordsWithReference(params) {
  return api.get(`/book-records-with-reference/${params}`);
}

export function exportBookRecordsWithReference(params) {
    return api({
        url: `/book-records-with-reference/export/?${params}`,
        method: 'GET',
        responseType: 'blob'
      });
}
/**
 *
 * @param {Number} bookRecordId
 * @returns {Promise<AxiosResponse<any>>}
 */
export function retrieveBookRecordWithReference(bookRecordId) {
  return api.get(`/book-records-with-reference/${bookRecordId}/`);
}

/**
 *
 * @param {Number} bookRecordId
 * @param {BookRecordWithReference} bookRecordWithReference
 * @param token
 * @returns {Promise<AxiosResponse<any>>}
 */
export function updateBookRecordWithReference(bookRecordId, bookRecordWithReference, token) {
  return api.put(`/book-records-with-reference/${bookRecordId}/`, bookRecordWithReference, { headers: { Authorization: `Bearer ${token}` } });
}
// endregion

// region borrowings
export function createBorrowing(borrowing, token) {
  return api.post("/borrowings/", borrowing, { headers: { Authorization: `Bearer ${token}` } });
}

export function retrieveBorrowings(params) {
  return api.get(`/borrowings/${params}`);
}

export function retrieveBorrowing(borrowingId) {
  return api.get(`/borrowings/${borrowingId}/`);
}

export function updateBorrowing(borrowingId, borrowing, token) {
  return api.put(`/borrowings/${borrowingId}/`, borrowing, { headers: { Authorization: `Bearer ${token}` } });
}

export function deleteBorrowing(borrowingId, token) {
  return api.delete(`/borrowings/${borrowingId}/`, { headers: { Authorization: `Bearer ${token}` } });
}

export function getBorrowingsCount(params) {
  return api.get(`/borrowings/count/${params}`);
}

export function getCurrentBorrowingStateOfRecord(recordId) {
  return api.get(`/book-references/${recordId}/borrowings/current/`);
}

export function getBorrowingStateOfRecord(recordId) {
  return api.get(`/book-references/${recordId}/borrowings/`);
}
// endregion

// region contact
export function sendMessageToAdmin(message, theSum, emailAddress) {
  return api.post('/contact/send-message/', {message, theSum, emailAddress});
}
// endregion

// region log events

export function retrieveLogEvents(params, token) {
  return api.get(`/log-events/${params}`, { headers: { Authorization: `Bearer ${token}` } });
}


export function getLogEventsCount(params, token) {
  return api.get(`/log-events/count/${params}`, { headers: { Authorization: `Bearer ${token}` } });
}

// endregion


// region import
// region import csv
export function markRowAsProcessed(nRow) {
  return api.get(`/import-csv/rows/${nRow}/add-store`)
}

export function markRowAsNotProcessed(nRow) {
  return api.get(`/import-csv/rows/${nRow}/remove-store`);
}
// endregion

// export function importOneCatalogue() {
//   return api.post("/imports-ci-2023/");
// }

export function getCatalogueListRequest(params) {
  return api.get(`/import-ci-2023/catalogues/${params}`);
}

export function getCataloguesCountRequest(params) {
  return api.get(`/import-ci-2023/catalogues/count/${params}`);
}

export function uploadOneCatalogueRequest(formData, token) {
  return api.post("/import-ci-2023/catalogues/", formData, { headers: { Authorization: `Bearer ${token}` } });
}

export function getCatalogueInfoByKey(key) {
  return api.get(`/import-ci-2023/catalogues/${key}/?action=info`);
}

export function getCatalogueImportByKey(key) {
  return api.get(`/import-ci-2023/keys/${key}/`);
}

export function applyCatalogueRequest(key, action) {
  return api.get(`/import-ci-2023/catalogues/${key}/?action=${action}`);
}

export function downloadCatalogueToFix(key) {
  return applyCatalogueRequest(key, "to-fix");
}
export function deleteCatalogueByKey(key, token) {
  return api.delete(`/import-ci-2023/catalogues/${key}/`, { headers: { Authorization: `Bearer ${token}` } });
}

export function getOneImportRequest(importId) {
  return api.get(`/import-ci-2023/${importId}/`);
}

export function importCatalogueFromFileRequest(data, token) {
  return api.post(`/import-ci-2023/`, data, { headers: { Authorization: `Bearer ${token}` } });
}

export function checkColumnsRequest(key, ignore_n_first_rows) {
  return api.get(`/import-ci-2023/catalogues/${key}/?action=check&ignore_n_first_rows=${ignore_n_first_rows}`)
}

export async function getCatalogueReferenceColumns(key) {
  return api.get(`/import-ci-2023/catalogues/${key}/?action=reference`);
}

export function previewCatalogueRequest(key, ignoreNFirstRows, nFirstRows, filterByVerifiedEntry) {
  return api.get(`/import-ci-2023/catalogues/${key}/?action=preview&ignore_n_first_rows=${ignoreNFirstRows}&n_first_rows=${nFirstRows}&filter_by_verified_entry=${filterByVerifiedEntry}`)
}

// region too much
export function goToNextNotMarkedRow(nRow) {
  return api.get(`/import-csv/rows/${nRow}/go-to-next-not-marked-row`);
}

export function importAllCatalogue() {
  return api.get("/import/all/");
}

export function deleteAllCatalogue() {
  return api.delete("/import/catalogue/");
}
// endregion
// endregion

// region export
export function exportXLSXRequest(params) {
  return api.get(`/export/xlsx/${params}`);
}

export function exportCSVRequest(params) {
  return api.get(`/export/csv/${params}`);
}
// endregion

// region search
export function searchWorks(params) {
  return api.get(`/search/works/${params}`);
}

export function searchApproximateNamedEntities(params) {
  return api.get(`/search/named-entities/${params}`)
}

export function getPublishedWorks(params) {
  return api.get(`/works/published/${params}`)
}

export function addPublishedWorks(publishedWork, token, params) {
  return api.post(`/works/published/${params}`, publishedWork, { headers: { Authorization: `Bearer ${token}` } })
}

export function updatePublishedWork(publishedWorkId, publishedWork, token, params) {
  return api.put(`/works/published/${publishedWorkId}/${params}`, publishedWork, { headers: { Authorization: `Bearer ${token}` } })
}

export function getPublishedWork(publishedWorkId, params) {
  return api.get(`/works/published/${publishedWorkId}/${params}`)
}

// endregion

// region dublin core
export function getDublinCoreEntries(query, params) {
  // params: {
  //    query: String,
  //    count: 0 or 1
  //    ...
  // }
  return api.get(`/dublin-core/?${query}`, params);
}

export function getDublinCoreEntry(id, params) {
  return api.get(`/dublin-core/${id}`, params);
}
// endregion

// region ark
export function resolveArk(naan, arkName) {
  return api.get(`/ark:/${naan}/${arkName}`);
}

export function generateArkForAllEntriesMissingOnes() {
    return api.get(`/ark/generate-for-all-entries-missing-ark/`);
}
// endregion

// region societaire / adhesion SAT
export function sendSatSubscription(formData) {
  return api.post('/send-sat/', formData);
}
// endregion
