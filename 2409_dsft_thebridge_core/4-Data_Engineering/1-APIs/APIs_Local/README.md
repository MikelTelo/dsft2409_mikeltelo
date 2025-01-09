# APIs design

Examples of good naming ✅

* /employees
* /departments
* /employees/9e0343b9-a873-4db7-813e-fdeb68305d3b/departments
* /candidates/search?name=jhon&page=1&offset=20

The first endpoint can be used to create/update a single employee, or even to retrieve all the collection

The second endpoint is similar to the first one, but based on departments

The third can be used to update the departments of a given employee. Also, to retrieve the departments where the employee is added (if the key is found)

The last one is a search endpoint following the Google Semantic, it is retrieving the first page with only 20 candidates who are named as John

Examples of bad naming ❌

* /employee (not plural)
* /departments/create (verbosity is not allowed)
* /getEmployeeById (Please don't)
* /search?type=candidate&name=jhon&page=1&offset=20 (Avoid using flags, wrong abstraction level)



**Your endpoints are resources, not a representation of your datasource**

It is important to identify the objects which they will be presented as resources in an agnostic manner.

One of the most common pitfalls, is to design the endpoints keeping the datasource on mind. I mean, imagine you have a Relational Database, and it contains VEHICLE, CAR, BIKE, PIECE, VEHICLE_PIECE... as examples

Then it is wrong to have dedicated endpoints for each table, specially if VEHICLE is so abstract, and it has no meaning by itself. So this is wrong:

* /vehicles

* /cars

* /bikes

* /pieces

Probably just /cars and /bikes would be enough, and to retrieve pieces you could model in this way:

* /cars/pieces: To deal with the full catalog of pieces for cars

* /bikes/pieces: To deal with the full catalog of pieces for bikes

* /cars/{id}/pieces: To deal with the pieces they were used to manufacture a specific model of car

* /bikes/{id}/pieces: To deal with the pieces they were used to manufacture a specific model of bike