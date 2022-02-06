SELECT Name, Price_book, Kolvo FROM book join postav
    using(ID_book) where year(Date_p) = $year;