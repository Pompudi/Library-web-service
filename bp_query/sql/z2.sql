Select Name, sum(PriceSum), sum(Kolvo) from postav
    join (SELECT ID_doc from doc where Name_izd = $publishing)post using(ID_doc)
    join (select Name,ID_book from book)book using(ID_book)
where year(Date_p) = $year group by ID_book