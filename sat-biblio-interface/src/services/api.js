import axios from 'axios';

// region auteurs
export function createAuthor(author) {
  return axios.post("/authors", author);
}

export function retrieveAuthors(params) {
  return axios.get(`/authors${params}`);
}

export function retrieveAuthorNumber(params) {
  return axios.get(`/authors/number${params}`);
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

// endregion

// region references

export function createBookReference(bookReference) {
  return axios.post("/book-references", bookReference);
}

export function retrieveBookReferences(params) {
  return axios.get(`/book-references${params}`);
}

export function retrieveBookReferenceNumber(params) {
  return axios.get(`/book-references/number${params}`);
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

// endregion

// region records

export function createBookRecord(bookRecord) {
  return axios.post("/book-records", bookRecord);
}

export function retrieveBookRecords(params) {
  return axios.get(`/book-records${params}`);
}

export function retrieveBookRecordNumber(params) {
  return axios.get(`/book-records/number${params}`);
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

// endregion

// region borrowings
export function createBorrowing(borrowing) {
  return axios.post("/borrowings", borrowing);
}

export function retrieveBorrowings(params) {
  return axios.get(`/borrowings${params}`);
}

export function retrieveBorrowingNumber(params) {
  return axios.get(`/borrowings/number${params}`);
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
// endregion