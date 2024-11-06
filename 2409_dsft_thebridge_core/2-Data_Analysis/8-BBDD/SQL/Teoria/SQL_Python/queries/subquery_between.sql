SELECT CompanyName
FROM Customers
WHERE CustomerID IN (SELECT CustomerId FROM Orders WHERE OrderDate BETWEEN '2016-07-10' AND '2016-07-20')