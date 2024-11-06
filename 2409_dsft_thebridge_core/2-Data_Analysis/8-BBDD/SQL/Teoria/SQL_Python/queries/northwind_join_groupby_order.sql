-- How many objects has each customer from UK ordered each year?
SELECT Customers.CompanyName, strftime('%Y', Orders.OrderDate) as year, SUM( [Order Details].Quantity )
FROM Customers	
	INNER JOIN Orders ON Customers.CustomerID = Orders.CustomerID
	INNER JOIN [Order Details] ON Orders.OrderID = [Order Details].OrderID
WHERE Customers.Country = 'UK'
GROUP BY Customers.CompanyName, year
ORDER BY Customers.CompanyName, year;