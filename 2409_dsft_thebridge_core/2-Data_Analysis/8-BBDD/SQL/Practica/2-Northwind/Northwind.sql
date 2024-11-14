-- Analiza las ventas por regiones
SELECT 
    C.Region AS Region,
    P.ProductName AS Product,
    SUM(OD.Quantity * OD.UnitPrice * (1 - OD.Discount)) AS TotalSales
FROM 
    Orders O
JOIN 
    Order_Details OD ON O.OrderID = OD.OrderID
JOIN 
    Customers C ON O.CustomerID = C.CustomerID
JOIN 
    Products P ON OD.ProductID = P.ProductID
WHERE 
    C.Region IS NOT NULL
GROUP BY 
    C.Region, P.ProductName
ORDER BY 
    C.Region, TotalSales DESC;


