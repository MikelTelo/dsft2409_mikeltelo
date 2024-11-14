--ex1
SELECT * 
FROM customers
WHERE country = "Brazil";

--ex2
SELECT *
FROM employees
WHERE title = "Sales Support Agent";

--ex3
/*SELECT *
FROM tracks
WHERE composer = "AC/DC";*/

SELECT 
tracks.Name AS Nombre_cancion,
artists.Name AS Nombre_artista,
albums.title AS Nombre_album
FROM tracks
INNER JOIN albums ON  albums.AlbumId = tracks.AlbumId
INNER JOIN artists ON artists.ArtistId = albums.ArtistId
WHERE artists.Name = "AC/DC";

-- exercise 4
SELECT firstname || " " || lastname AS Nombre_completo,
customerid AS ID,
country AS País
FROM customers
WHERE country <> "USA";

--exercise 5
SELECT
firstname || " " ||lastname AS Nombre_completo,
City || " " || State || " " || Country AS Dirección,
email
FROM employees
WHERE title = "Sales Support Agent"

--exercise 6
SELECT DISTINCT
billingcountry
FROM invoices;

--7
SELECT
State,
Count(customerid) AS N_clientes
FROM customers
WHERE country = "USA"
GROUP BY state
ORDER BY 2 DESC

--8
SELECT
invoiceid,
SUM(quantity) AS N_articulos
FROM invoice_items
WHERE invoiceid IN (37)
GROUP BY 1

--9
SELECT 
artists.Name,
COUNT(tracks.trackid)
FROM tracks
INNER JOIN albums ON tracks.albumid = albums.albumid
INNER JOIN artists ON albums.artistid = artists.artistid
WHERE artists.name = "AC/DC"
GROUP BY 1

--10
SELECT
invoiceid,
SUM(quantity) AS N_articulos
FROM invoice_items
--WHERE invoiceid IN (37)
GROUP BY 1
ORDER BY 2 DESC

--11
SELECT 
billingcountry,
COUNT(invoiceid)
FROM invoices
GROUP BY 1
ORDER BY 2 DESC
--LIMIT 5;

--12
SELECT
strftime("%Y", invoicedate) AS Año,
COUNT(invoiceid)
FROM invoices
WHERE Año IN ("2009","2011")
GROUP BY 1

--13
SELECT SUM(N_facturas)
FROM
(
SELECT
strftime("%Y", invoicedate) AS Año,
COUNT(invoiceid) AS N_facturas
FROM invoices
WHERE Año BETWEEN "2009" AND "2011"
GROUP BY 1)

--ex14
SELECT
country,
COUNT(customerid)
FROM customers
WHERE country IN ("Spain","Brazil")
GROUP BY 1

--ex15
SELECT name
FROM tracks
WHERE Name LIKE "You%"


--Parte2
--1
SELECT
c.firstname || " " || c.lastname AS Nombre_cliente,
i.invoiceid AS Id_factura,
i.invoicedate AS Fecha_factura,
i.billingcountry AS Pais_factura
FROM invoices i
INNER JOIN customers c ON i.customerid = c.customerid
WHERE c.country = "Brazil"
 
--2
SELECT
e.firstname || " " || e.lastname AS Nombre_empleado,
i.invoiceid,
i.InvoiceDate,
i.billingcountry
FROM invoices i
INNER JOIN customers c ON i.customerid = c.customerid
INNER JOIN employees e on c.supportrepid = e.employeeid

--3
SELECT
c.firstname || " " || c.lastname AS Nombre_cliente,
c.country AS Pais_cliente,
e.firstname || " " || e.lastname AS Nombre_empleado,
SUM(i.total)
FROM invoices i
INNER JOIN customers c ON i.customerid = c.customerid
INNER JOIN employees e ON c.supportrepid = e.employeeid
GROUP BY 1,2,3
ORDER BY 4 DESC

--4
SELECT ii.invoiceid,
ii.trackid,
t.name AS Nombre_cancion
FROM invoice_items ii
INNER JOIN tracks t ON ii.trackid = t.trackid

--5
SELECT
t.Name AS Nombre_cancion,
mt.Name AS Nombre_formato,
a.title AS Nombre_album,
g.Name AS Nombre_genero
FROM tracks t
INNER JOIN albums a ON t.albumid = a.albumid
INNER JOIN genres g ON t.genreid = g.GenreId
INNER JOIN media_types mt ON t.MediaTypeId = mt.MediaTypeId

--6
SELECT
pt.playlistid,
p.name AS Nombre_playlist,
COUNT(pt.trackid)
FROM playlist_track pt
INNER JOIN playlists p ON p.PlaylistId = pt.playlistid
GROUP BY 1,2
ORDER BY 3 DESC

--7
SELECT
e.firstname || " " || e.lastname AS Nombre_empleado,
SUM(i.total)
FROM invoices i
INNER JOIN customers c ON i.customerid = c.customerid
INNER JOIN employees e ON c.supportrepid = e.employeeid
GROUP BY 1
ORDER BY 2 DESC

--8
SELECT
e.firstname || " " || e.lastname AS Nombre_empleado,
SUM(i.total)
FROM invoices i
INNER JOIN customers c ON i.customerid = c.customerid
INNER JOIN employees e ON c.supportrepid = e.employeeid
WHERE strftime("%Y", i.invoicedate) = "2009"
GROUP BY 1
ORDER BY 2 DESC
--LIMIT 1

--9
SELECT
ar.artistid,
ar.Name as Nombre_artista,
SUM(i.total) AS Ventas_totales
FROM invoices i
INNER JOIN invoice_items ii ON i.invoiceid = ii.invoiceid
INNER JOIN tracks t ON ii.trackid = t.trackid
INNER JOIN albums a ON t.albumid = a.albumid
INNER JOIN artists ar ON a.artistid = ar.ArtistId
GROUP BY 1,2
ORDER BY 3 DESC
--LIMIT 3

