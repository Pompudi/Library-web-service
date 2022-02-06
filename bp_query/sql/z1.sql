SELECT Name  FROM book join (SELECT Name_izd, ID_book from doc join postav
    using(ID_doc) where year(Date_p) = 2013 and month(Date_p)=03)pos
    using(ID_book) where Name_izd = $publishing group by ID_book;