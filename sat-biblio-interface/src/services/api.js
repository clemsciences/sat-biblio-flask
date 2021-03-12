import axios from 'axios';

// region users
export function connectUser(args) {
  return axios.post("/users/connect", args);
}

export function createUser(formData) {
  return axios.post('/users/create', formData);
}

export function disconnectUser() {
  return axios.get("/users/disconnect");
}

export function haveForgottenPassword() {
  return axios.get("/users/forgotten_password");
}

export function recreatePassword(password) {
  return axios.post('/users/reinitiate-password', {password});
}

export function checkUserLogin() {
  return axios.post('/users/check_login');
}

// endregion

// region auteurs
export function createAuthor(author) {
  return axios.post("/authors", author);
}

export function retrieveAuthors(params) {
  return axios.get(`/authors${params}`);
}

export function retrieveAuthor(authorId) {
  return axios.get(`/authors/${authorId}/`);
}

export function updateAuthor(authorId, author) {
  return axios.put(`/authors/${authorId}`, author);
}

export function deleteAuthor(authorId) {
  return axios.delete(`/authors/${authorId}`);
}

export function getAuthorsCount(params) {
  return axios.get(`/authors/count${params}`);
}

// endregion

// region references

export function createBookReference(bookReference) {
  return axios.post("/book-references", bookReference);
}

export function retrieveBookReferences(params) {
  return axios.get(`/book-references${params}`);
}

export function retrieveBookReference(bookReferenceId) {
  return axios.get(`/book-references/${bookReferenceId}/`);
}

export function updateBookReference(bookReferenceId, bookReference) {
  return axios.put(`/book-references/${bookReferenceId}`, bookReference);
}

export function deleteBookReference(bookReferenceId) {
  return axios.delete(`/book-references/${bookReferenceId}`);
}

export function getBookReferencesCount(params) {
  return axios.get(`/book-references/count${params}`);
}

// endregion

// region records

export function createBookRecord(bookRecord) {
  return axios.post("/book-records", bookRecord);
}

export function retrieveBookRecords(params) {
  return axios.get(`/book-records${params}`);
}

export function retrieveBookRecord(bookRecordId) {
  return axios.get(`/book-records/${bookRecordId}/`);
}

export function updateBookRecord(bookRecordId, bookRecord) {
  return axios.put(`/book-records/${bookRecordId}`, bookRecord);
}

export function deleteBookRecord(bookRecordId) {
  return axios.delete(`/book-records/${bookRecordId}`);
}

export function getBookRecordsCount(params) {
  return axios.get(`/book-records/count${params}`);
}

// endregion

// region borrowings
export function createBorrowing(borrowing) {
  return axios.post("/borrowings", borrowing);
}

export function retrieveBorrowings(params) {
  return axios.get(`/borrowings${params}`);
}

export function retrieveBorrowing(borrowingId) {
  return axios.get(`/borrowings/${borrowingId}/`);
}

export function updateBorrowing(borrowingId, borrowing) {
  return axios.put(`/borrowings/${borrowingId}`, borrowing);
}

export function deleteBorrowing(borrowingId) {
  return axios.delete(`/borrowings/${borrowingId}`);
}

export function getBorrowingsCount(params) {
  return axios.get(`/borrowings/count${params}`);
}
// endregion