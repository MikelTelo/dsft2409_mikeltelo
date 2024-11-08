### Ejercicio 1: Restaurantes
READ
--------
1. Mostrar todos los documentos de la colección restaurantes
db.restaurants.find();
2. Mostrar los campos restaurant_id, nombre, distrito y cocina, pero excluya el campo _id para todos los documentos de la colección restaurantes
db.restaurants.find({},{"restaurant_id" : 1,"name":1,"borough":1,"cuisine" :1,"_id":0});
3. Mostrar los primeros 5 restaurantes que se encuentran en el distrito Bronx
db.restaurants.find({"borough": "Bronx"}).limit(5);
4. Encontrar los restaurantes que lograron una puntuación superior a 80 pero inferior a 100
db.restaurants.find({grades : { $elemMatch:{"score":{$gt : 80 , $lt :100}}}});
5. Encontrar los restaurantes que se ubican en un valor de latitud inferior a -95.754168
db.restaurants.find({"address.coord" : {$lt : -95.754168}});
6. Encontrar los restaurantes que no preparan ninguna cocina de 'estadounidense' y lograron una puntuación superior a 70 y se ubicaron en una longitud inferior a -65.754168. Nota: Realice esta consulta sin usar el operador $and
db.restaurants.find(
                           {
                             "cuisine" : {$ne : "American "},
                             "grades.score" :{$gt: 70},
                             "address.coord" : {$lt : -65.754168}
                            }
                     );
                     db.restaurants.find(
                           {
                             "cuisine" : {$not:/.*American.*/,
                             "grades.score" :{$gt: 70},
                             "address.coord" : {$lt : -65.754168}
                            }
                     );
7. Encontrar los restaurantes que no preparan comida americana y lograron  calificación 'A' que no pertenece al distrito de Brooklyn. El documento debe mostrarse según la cocina en orden descendente.
db.restaurants.find( {
                             "cuisine" : {$ne : "American "},
                             "grades.grade" :"A",
                             "borough": {$ne : "Brooklyn"}
                       }
                    ).sort({"cuisine":-1});
8. Encontrar los restaurantes que pertenecen al distrito Bronx y preparan platos americanos o chinos
db.restaurants.find(
    {
    "borough": "Bronx" ,
    $or : [
        { "cuisine" : "American " },
        { "cuisine" : "Chinese" }
        ]
    }
);
9. Encontrar la identificación del restaurante, el nombre, el distrito y la cocina para aquellos restaurantes que pertenecen al distrito de Staten Island o Queens o Bronxor Brooklyn
db.restaurants.find(
    {"borough" :{$in :["Staten Island","Queens","Bronx","Brooklyn"]}},
    {
    "restaurant_id" : 1,
    "name":1,"borough":1,
    "cuisine" :1
    }
);
10. Encontrar el Id. del restaurante, el nombre, el distrito y la cocina de aquellos restaurantes que lograron una puntuación que no supere los 10
db.restaurants.find(
    {"grades.score" :
        { $not:
            {$gt : 10}
        }
    },
    {
        "restaurant_id" : 1,
        "name":1,"borough":1,
        "cuisine" :1
    }
);
11. Escriba una consulta de MongoDB para encontrar la identificación, el nombre y las calificaciones del restaurante para aquellos restaurantes que obtuvieron una calificación de "A" y obtuvieron un puntaje de 11 en una fecha ISO "2014-08-11T00: 00: 00Z" entre muchas fechas de encuesta
db.restaurants.find(
                {
                 "grades.date": ISODate("2014-08-11T00:00:00Z"),
                 "grades.grade":"A" ,
                 "grades.score" : 11
                },
                {"restaurant_id" : 1,"name":1,"grades":1}
             );
12. Encontrar la identificación, el nombre, la dirección y la ubicación geográfica del restaurante para aquellos restaurantes donde el segundo elemento de la matriz coord contiene un valor que es más de 42 y hasta 52.
db.restaurants.find(
                      {
                        "address.coord.1": {$gt : 42, $lte : 52}
                      },
                        {"restaurant_id" : 1,"name":1,"address":1,"coord":1}
                   );
CREATE
--------
13. Crea un par de restaurantes que te gusten. Tendrás que buscar en google Maps los datos de las coordenadas
db.restaurants.insertOne(
   { address:   {building: "37",
        coord: [40.421459516270865, -3.696834221545593],
        street: "San Marcos",
        zipcode: "28004"},
    borough: "Chueca",
    cuisine: "Mediterranean",
    name:"Diurno",
    restaurant_id:"873683997" }
)
UPDATE
--------
14. Actualiza los restaurantes. Cambia el tipo de cocina "Ice Cream, Gelato, Yogurt, Ices" por "sweets"
db.restaurants.updateMany({"cuisine":"Ice Cream, Gelato, Yogurt, Ices"},
            {$set:{"cuisine": "sweets"}});
15. Actualiza el nombre del restaurante "Wild Asia" por "Wild Wild West"
db.restaurants.updateOne({"name": "Wild Asia"},
            {$set:{"name": "Wild Wild West"}});
DELETE
--------
16. Borra los restaurantes con latitud menor que -95.754168
db.restaurants.deleteMany( {"address.coord.0" : {$lt : -95.754168}} )
17. Borra los restaurantes cuyo nombre empiecen por "C"
db.restaurants.deleteMany( {"name" : {$regex : "^C"}} )
### Ejercicio 2 - Aggregation
Añadir los siguientes documentos a la colección empleados:
```javascript
db.employees.insertMany([
    {
        _id:1,
        firstName: "Muchelle",
        lastName: "Wallys",
        gender:'female',
        email: "muchelle@thebridgeschool.es",
        salary: 5000,
        department: {
                    "name":"HR"
                }
    },
    {
        _id:2,
        firstName: "Marta",
        lastName: "Perez",
        gender:'female',
        email: "marta@demo.com",
        salary: 8000,
        department: {
                    "name":"Finance"
                }
    },
    {
        _id:3,
        firstName: "Birja",
        lastName: "Rybera",
        gender:'male',
        email: "birja@thebridgeschool.es",
        salary: 7500,
        department: {
                    "name":"Marketing"
                }
    },
    {
        _id:4,
        firstName: "Rosa",
        lastName: "Sanchez",
        gender:'female',
        email: "rosa@demo.com",
        salary: 5000,
        department: {
                    "name":"HR"
                }
    },
    {
        _id:5,
        firstName: "Alvaru",
        lastName: "Aryas",
        gender:'male',
        email: "alvaru@thebridgeschool.es",
        salary: 4500,
        department: {
                    "name":"Finance"
                }
    },
    {
        _id:6,
        firstName: "Anita",
        lastName: "Rodrigues",
        gender:'female',
        email: "anita@demo.com",
        salary: 7000,
        department: {
                    "name":"Marketing"
                }
    },
        {
        _id:7,
        firstName: "Alejandru",
        lastName: "Regex",
        gender:'male',
        email: "alejandru@thebridgeschool.es",
        salary: 7000,
        department: {
                    "name":"Marketing"
                }
    }
])
```
1. Devuelve todas las empleadas de la empresa usando $match
db.employees.aggregate([ {$match:{ gender: 'female'}} ])
2. Devuelve un array de objetos que tenga en cada uno `{id_departamento,totalEmployees}` datos como en el siguiente ejemplo:
```javascript
[
  { _id: 'Marketing', totalEmployees: 2},
  { _id: 'HR', totalEmployees: 2},
  { _id: 'Finance', totalEmployees: 3}
]
```
db.employees.aggregate([
    { $group:{ _id:'$department.name', totalEmployees: { $sum:1 } }
}])
3. Modifica el ejercicio anterior para que sólo devuelva datos de los empleados
db.employees.aggregate([
    {$match:{ gender: 'female'}},
    { $group:{ _id:'$department.name', totalEmployees: { $sum:1 } }
}])
4. Devuelve los datos de las empleadas ordenados por salario ascendente
db.employees.aggregate([
    { $match:{ gender:'female'}},
    { $sort:{ salary:1}}
])
5. Devuelve los datos de las empleadas por departamento ordenados por total salario ascendente para sacar una salida parecida a:
```javascript
[
  { _id: { deptName: 'Finance' }, totalEmployees: 2, totalSalaries: 12500},
  { _id: { deptName: 'HR' }, totalEmployees: 1, totalSalaries: 10000},
  { _id: { deptName: 'Marketing' }, totalEmployees: 2, totalSalaries: 5000}
]
```
db.employees.aggregate([
    { $match:{ gender:'female'}},
    { $group:{ _id:{ deptName:'$department.name'}, totalEmployees: { $sum:1}, totalSalaries: { $sum:'$salary'} } },
    { $sort:{ totalSalaries:1}}
])