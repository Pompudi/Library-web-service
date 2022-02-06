select ID_book, Name_book, ID_doc, Name_izd, Price from books_for_sale
where ID_book = $book_id and ID_doc = $izd_id