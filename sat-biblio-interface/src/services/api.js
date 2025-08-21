import axios from 'axios';

// region users
export function connectUser(args) {
  return axios.post("/users/connect/", args);
}

export function createUser(formData) {
  return axios.post('/users/create/', formData);
}

export function disconnectUser() {
  return axios.get("/users/disconnect/");
}

export function haveForgottenPassword(formData) {
  return axios.post("/users/forgotten-password/", formData);
}

export function recreatePassword(currentPassword, newPassword) {
  return axios.post('/users/new-password/', {currentPassword, newPassword});
}

export function confirmUserRegistration(inscriptionToken, emailAddress) {
  return axios.get(`/users/confirm/${inscriptionToken}/?email=${emailAddress}`);
}

export function checkUserLogin() {
  return axios.post('/users/check_login/');
}

export function searchNearUsers(params) {
  return axios.get(`/users/search-near/?${params}`)
}

export function retrieveUsers(params, token) {
  return axios.get(`/users/${params}`, { headers: { Authorization: `Bearer ${token}` } });
}

export function getUsersCount(params, token) {
  return axios.get(`/users/count/${params}`, { headers: { Authorization: `Bearer ${token}` } });
}

export function retrieveUser(id, token) {
  return axios.get(`/users/${id}/`, { headers: { Authorization: `Bearer ${token}` } });
}

export function updateUser(id, user, token) {
  return axios.put(`/users/${id}/`, user, { headers: { Authorization: `Bearer ${token}` } });
}

export function deleteUser(id, token) {
  return axios.delete(`/users/${id}/`, { headers: { Authorization: `Bearer ${token}` } });
}

export function resendConfirmationEmail(id, token) {
  return axios.get(`/users/${id}/resend-confirmation-email/`, { headers: { Authorization: `Bearer ${token}` } });
}

// endregion

// region auteurs
export function createAuthor(author, token) {
  return axios.post("/authors/", author, { headers: { Authorization: `Bearer ${token}` } });
}

export function retrieveAuthors(params) {
  return axios.get(`/authors/${params}`);
}

export function retrieveNotValidatedAuthors(params) {
  return retrieveAuthors(`?valid=0&${params}`);
}

export function retrieveAuthor(authorId) {
  return axios.get(`/authors/${authorId}/`);
}

export function updateAuthor(authorId, author, token) {
  return axios.put(`/authors/${authorId}/`, author, { headers: { Authorization: `Bearer ${token}` } });
}

export function deleteAuthor(authorId, token) {
  return axios.delete(`/authors/${authorId}/`, { headers: { Authorization: `Bearer ${token}` } });
}

export function getAuthorsCount(params) {
  return axios.get(`/authors/count/${params}`);
}

export function getNotValidatedAuthorsCount(params) {
  return getAuthorsCount(`?valid=0&${params}`);
}

export function searchAuthors(params) {
  return axios.post("/authors/search/", params);
}

export function searchNearAuthors(params) {
  return axios.get(`/authors/search-near/?${params}`);
}


export function getEntryListAssociatedToAuthor(authorId, params) {
  return axios.get(`/authors/${authorId}/entries/?${params}`)
}

export function getEntryListAssociatedToAuthorCount(authorId, params) {
  if(params) {
      return axios.get(`/authors/${authorId}/entries/count/?${params}`);
  } else {
    return axios.get(`/authors/${authorId}/entries/count/`);
  }
}

// endregion

// region references

export function createBookReference(bookReference, token) {
  return axios.post("/book-references/", bookReference, { headers: { Authorization: `Bearer ${token}` } });
}

export function retrieveBookReferences(params) {
  return axios.get(`/book-references/${params}`);
}

export function retrieveNotValidatedBookReferences(params) {
  return retrieveBookReferences(`?valid=0&${params}`);
}

export function retrieveBookReference(bookReferenceId) {
  return axios.get(`/book-references/${bookReferenceId}/`);
}

export function updateBookReference(bookReferenceId, bookReference, token) {
  return axios.put(`/book-references/${bookReferenceId}/`, bookReference, { headers: { Authorization: `Bearer ${token}` } });
}

export function deleteBookReference(bookReferenceId, token) {
  return axios.delete(`/book-references/${bookReferenceId}/`, { headers: { Authorization: `Bearer ${token}` } });
}

export function getBookReferencesCount(params) {
  return axios.get(`/book-references/count/${params}`);
}

export function getNotValidatedBookReferencesCount(params) {
  return getBookReferencesCount(`?valid=0&${params}`);
}

export function searchBookReferences(params) {
  return axios.post("/book-references/search/", params)
}

export function searchNearBookReferences(params) {
  return axios.get(`/book-references/search-near/?${params}`)
}

export function getEntryListAssociatedToReference(bookReference, params) {
  return axios.get(`/book-references/${bookReference}/entries/?${params}`)
}

export function getEntryListAssociatedToReferenceCount(bookReference, params) {
  if(params) {
    return axios.get(`/book-references/${bookReference}/entries/count/?${params}`);
  } else {
    return axios.get(`/book-references/${bookReference}/entries/count/`);
  }
}

// endregion

// region records

export function createBookRecord(bookRecord, token) {
  return axios.post("/book-records/", bookRecord, { headers: { Authorization: `Bearer ${token}` } });
}

export function retrieveBookRecords(params) {
  return axios.get(`/book-records/${params}`);
}

export function retrieveNotValidatedBookRecords(params) {
  return retrieveBookRecords(`?valid=0&${params}`);
}

export function retrieveBookRecord(bookRecordId) {
  return axios.get(`/book-records/${bookRecordId}/`);
}

export function updateBookRecord(bookRecordId, bookRecord, token) {
  return axios.put(`/book-records/${bookRecordId}/`, bookRecord, { headers: { Authorization: `Bearer ${token}` } });
}

export function deleteBookRecord(bookRecordId, token) {
  return axios.delete(`/book-records/${bookRecordId}/`, { headers: { Authorization: `Bearer ${token}` } });
}

export function getBookRecordsCount(params) {
  return axios.get(`/book-records/count/${params}`);
}

export function getNotValidatedBookRecordsCount(params) {
  return getBookRecordsCount(`?valid=0&${params}`);
}

export function searchBookRecords(params) {
  return axios.post("/book-records/search/", params);
}

export function searchNearBookRecords(params) {
  return axios.get(`/book-records/search-near/?${params}`);
}

export function getEntryListAssociatedToBookRecords(bookRecordId, params) {
  return axios.get(`/book-records/${bookRecordId}/entries/?${params}`);
}

export function getEntryListAssociatedToBookRecordsCount(bookRecordId, params) {
  if(params) {
    return axios.get(`/book-records/${bookRecordId}/entries/count/?${params}`);
  } else {
    return axios.get(`/book-records/${bookRecordId}/entries/count/`);
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
  return axios.post("/book-records-with-reference/", bookRecordWithReference, { headers: { Authorization: `Bearer ${token}` } });
}

/**
 *
 * @param {Object} params
 * @returns {Promise<AxiosResponse<any>>}
 */
export function retrieveBookRecordsWithReference(params) {
  return axios.get(`/book-records-with-reference/${params}`);
}

export function exportBookRecordsWithReference(params) {
    return axios({
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
  return axios.get(`/book-records-with-reference/${bookRecordId}/`);
}

/**
 *
 * @param {Number} bookRecordId
 * @param {BookRecordWithReference} bookRecordWithReference
 * @param token
 * @returns {Promise<AxiosResponse<any>>}
 */
export function updateBookRecordWithReference(bookRecordId, bookRecordWithReference, token) {
  return axios.put(`/book-records-with-reference/${bookRecordId}/`, bookRecordWithReference, { headers: { Authorization: `Bearer ${token}` } });
}
// endregion

// region borrowings
export function createBorrowing(borrowing, token) {
  return axios.post("/borrowings/", borrowing, { headers: { Authorization: `Bearer ${token}` } });
}

export function retrieveBorrowings(params) {
  return axios.get(`/borrowings/${params}`);
}

export function retrieveBorrowing(borrowingId) {
  return axios.get(`/borrowings/${borrowingId}/`);
}

export function updateBorrowing(borrowingId, borrowing, token) {
  return axios.put(`/borrowings/${borrowingId}/`, borrowing, { headers: { Authorization: `Bearer ${token}` } });
}

export function deleteBorrowing(borrowingId, token) {
  return axios.delete(`/borrowings/${borrowingId}/`, { headers: { Authorization: `Bearer ${token}` } });
}

export function getBorrowingsCount(params) {
  return axios.get(`/borrowings/count/${params}`);
}

export function getCurrentBorrowingStateOfRecord(recordId) {
  return axios.get(`/book-references/${recordId}/borrowings/current/`);
}

export function getBorrowingStateOfRecord(recordId) {
  return axios.get(`/book-references/${recordId}/borrowings/`);
}
// endregion

// region contact
export function sendMessageToAdmin(message, theSum, emailAddress) {
  return axios.post('/contact/send-message/', {message, theSum, emailAddress});
}
// endregion

// region log events

export function retrieveLogEvents(params, token) {
  return axios.get(`/log-events/${params}`, { headers: { Authorization: `Bearer ${token}` } });
}


export function getLogEventsCount(params, token) {
  return axios.get(`/log-events/count/${params}`, { headers: { Authorization: `Bearer ${token}` } });
}

// endregion


// region import
// region import csv
export function markRowAsProcessed(nRow) {
  return axios.get(`/import-csv/rows/${nRow}/add-store`)
}

export function markRowAsNotProcessed(nRow) {
  return axios.get(`/import-csv/rows/${nRow}/remove-store`);
}
// endregion

// export function importOneCatalogue() {
//   return axios.post("/imports-ci-2023/");
// }

export function getCatalogueListRequest(params) {
  return axios.get(`/import-ci-2023/catalogues/${params}`);
}

export function getCataloguesCountRequest(params) {
  return axios.get(`/import-ci-2023/catalogues/count/${params}`);
}

export function uploadOneCatalogueRequest(formData, token) {
  return axios.post("/import-ci-2023/catalogues/", formData, { headers: { Authorization: `Bearer ${token}` } });
}

export function getCatalogueInfoByKey(key) {
  return axios.get(`/import-ci-2023/catalogues/${key}/?action=info`);
}

export function getCatalogueImportByKey(key) {
  return axios.get(`/import-ci-2023/keys/${key}/`);
}

export function applyCatalogueRequest(key, action) {
  return axios.get(`/import-ci-2023/catalogues/${key}/?action=${action}`);
}

export function downloadCatalogueToFix(key) {
  return applyCatalogueRequest(key, "to-fix");
}
export function deleteCatalogueByKey(key, token) {
  return axios.delete(`/import-ci-2023/catalogues/${key}/`, { headers: { Authorization: `Bearer ${token}` } });
}

export function getOneImportRequest(importId) {
  return axios.get(`/import-ci-2023/${importId}/`);
}

export function importCatalogueFromFileRequest(data, token) {
  return axios.post(`/import-ci-2023/`, data, { headers: { Authorization: `Bearer ${token}` } });
}

export function checkColumnsRequest(key, ignore_n_first_rows) {
  return axios.get(`/import-ci-2023/catalogues/${key}/?action=check&ignore_n_first_rows=${ignore_n_first_rows}`)
}

export async function getCatalogueReferenceColumns(key) {
  return axios.get(`/import-ci-2023/catalogues/${key}/?action=reference`);
}

export function previewCatalogueRequest(key, ignoreNFirstRows, nFirstRows, filterByVerifiedEntry) {
  return axios.get(`/import-ci-2023/catalogues/${key}/?action=preview&ignore_n_first_rows=${ignoreNFirstRows}&n_first_rows=${nFirstRows}&filter_by_verified_entry=${filterByVerifiedEntry}`)
}

// region too much
export function goToNextNotMarkedRow(nRow) {
  return axios.get(`/import-csv/rows/${nRow}/go-to-next-not-marked-row`);
}

export function importAllCatalogue() {
  return axios.get("/import/all/");
}

export function deleteAllCatalogue() {
  return axios.delete("/import/catalogue/");
}
// endregion
// endregion

// region export
export function exportXLSXRequest(params) {
  return axios.get(`/export/xlsx/${params}`);
}

export function exportCSVRequest(params) {
  return axios.get(`/export/csv/${params}`);
}
// endregion

// region search
export function searchWorks(params) {
  return axios.get(`/search/works/${params}`);
}

export function searchApproximateNamedEntities(params) {
  return axios.get(`/search/named-entities/${params}`)
}

export function getPublishedWorks(params) {
  return axios.get(`/works/published/${params}`)
}

export function addPublishedWorks(publishedWork, token, params) {
  return axios.post(`/works/published/${params}`, publishedWork, { headers: { Authorization: `Bearer ${token}` } })
}

export function updatePublishedWork(publishedWorkId, publishedWork, token, params) {
  return axios.put(`/works/published/${publishedWorkId}/${params}`, publishedWork, { headers: { Authorization: `Bearer ${token}` } })
}

export function getPublishedWork(publishedWorkId, params) {
  return axios.get(`/works/published/${publishedWorkId}/${params}`)
}

// endregion

// region dublin core
export function getDublinCoreEntries(query, params) {
  // params: {
  //    query: String,
  //    count: 0 or 1
  //    ...
  // }
  return axios.get(`/dublin-core/?${query}`, params);
}

export function getDublinCoreEntry(id, params) {
  return axios.get(`/dublin-core/${id}`, params);
}
// endregion

// region ark
export function resolveArk(naan, arkName) {
  return axios.get(`/ark:/${naan}/${arkName}`);
}

export function generateArkForAllEntriesMissingOnes() {
    return axios.get(`/ark/generate-for-all-entries-missing-ark/`);
}
// endregion