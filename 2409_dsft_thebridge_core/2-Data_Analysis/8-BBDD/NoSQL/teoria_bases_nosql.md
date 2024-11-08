# MongoDB

Existen otros tipos de bases de datos además de las relacionales de SQL. Una de las bases de datos NoSQL más populares es MongoDB.

MongoDB es una base de datos NoSQL, orientada a documentos, es decir, no utiliza el modelo de datos relacional de tablas utilizado por SQL, en su lugar, almacena la información en documentos JSON. Esto significa que una colección en MongoDB contiene documentos que pueden ser completamente distintos entre sí, cada uno con su propia estructura y contenido.

Algunos tipos de bases de datos NoSQL son:

- **Documentales:** Como MongoDB. Almacena los datos en documentos JSON.

- **Clave-Valor:** Almacena datos como un conjunto de pares clave-valor en un solo espacio de la tabla.

- **Basadas en Grafos:** Usa una estructura de grafos para almacenar información y sus relaciones.

- **Orientadas a Columnas:** Almacena los datos en columnas en lugar de filas, lo que permite un acceso más rápido y eficiente a grandes conjuntos de datos.

- **Híbridas:** Unen características de distintos tipos de bases de datos.

Las bases de datos NoSQL se utilizan cuando se espera un gran volumen de datos y existe la necesidad de manejarlo de forma eficiente. Además, son escalables fácilmente, lo que significa que pueden manejar una gran cantidad de transacciones sin sacrificar la velocidad.
# Ejemplos de bases de datos NoSQL

---

Algunos ejemplos de bases de datos NoSQL y cómo se utilizan en diferentes aplicaciones:

## MongoDB

MongoDB es una base de datos basada en documentos que se utiliza comúnmente en la web. En MongoDB, los datos se almacenan en formato de documentos JSON, lo que permite una mayor flexibilidad en el almacenamiento y la recuperación de información.

```javascript
//Ejemplo de uso de MongoDB en Node.js

const MongoClient = require('mongodb').MongoClient;
const url = 'mongodb://localhost:27017';

MongoClient.connect(url, function(err, client) {
  if (err) throw err;

  const db = client.db('mydb');
  const collection = db.collection('mycollection');

  collection.findOne({}, function(err, result) {
    if (err) throw err;

    console.log(result);
    client.close();
  });
});
```

## Neo4J

Neo4J es una base de datos basada en grafos. Es posible usar Neo4J para representar relaciones entre entidades. Por ejemplo, puede ser usada en redes sociales para representar amigos en común.

```javascript
// Ejemplo de uso de Neo4J en JavaScript

const neo4j = require('neo4j-driver').v1;
const driver = neo4j.driver('bolt://localhost', neo4j.auth.basic('username', 'password'));

const session = driver.session();

const resultPromise = session.run(
  'MATCH (a:Person)-[:FRIEND]->(friend_of_friend) WHERE a.name = $name RETURN friend_of_friend.name',
  { name: 'Alice' }
);

resultPromise.then(result => {
  session.close();

  const singleRecord = result.records[0];
  const node = singleRecord.get(0);

  console.log(node.properties.name);
});

```

## Redis

Redis es una base de datos de clave-valor. Redis puede ser usada para almacenar y recuperar información a una velocidad extremadamente alta. Eso lo hace popular en aplicaciones como la caché de datos.

```javascript
// Ejemplo de uso de Redis en JavaScript

const redis = require('redis');
const client = redis.createClient();

client.on('error', function(err) {
  console.log('Error:', err);
});

client.set('key', 'value', redis.print);

client.get('key', function(err, reply) {
  console.log(reply);
});
```
---

En resumen, MongoDB es una base de datos NoSQL orientada a documentos, que se utiliza ampliamente en aplicaciones modernas, especialmente en aquellas que manejan grandes volúmenes de datos. Ofrece muchas ventajas, como una fácil escalabilidad, rápido acceso a los datos, capacidad de cambiar la estructura de datos en cualquier momento y una sintaxis fácil de entender para los desarrolladores.

Ventajas de usar MongoDB:

- **Flexibilidad y escalabilidad:** MongoDB es altamente escalable y permite almacenar y procesar grandes volúmenes de datos. Además, su modelo de datos orientado a documentos ofrece una mayor flexibilidad que el modelo relacional de SQL, lo que resulta útil en situaciones en las que las estructuras de datos son complejas o cambian con frecuencia.

- **Velocidad y eficiencia:** MongoDB realiza operaciones rápidas de lectura y escritura y puede procesar datos en paralelo. Esto lo hace una opción adecuada para aplicaciones web y móviles en las que se necesitan tiempos de respuesta rápidos y bajos tiempos de inactividad.

- **Escritura robusta:** MongoDB escribe datos con una técnica llamada compromiso de escritura de "escribir con mayoría". Esto significa que el sistema no confirmará que una escritura se realizó correctamente a menos que se hayan escritos los datos en la mayoría de los servidores. Esto hace que sea difícil perder datos al realizar escrituras.

Desventajas de usar MongoDB:

- **Sin soporte de transacciones completas:** A diferencia de SQL, MongoDB no soporta transacciones completas, lo que significa que las operaciones no se pueden revertir una vez que se han realizado. Si se requiere un acceso garantizado para realizar elementos transaccionales, SQL es la solución ideal.

- **Menor madurez y menor popularidad:** A pesar de su rápida adopción, MongoDB ha estado en la industria por mucho menos tiempo que SQL. Esto significa que puede haber menos documentación, menos herramientas, y menos apoyo general para la plataforma en comparación con SQL.

- **Menor control de la integridad de los datos:** El modelo de datos de documentos/jerarquías propenso a errores en la inserción y actualización de documentos. MongoDB tiene muchas restricciones que no se pueden imponer, como las verificaciones de integridad referencial que se realizan en SQL. Por lo tanto, si se requiere un alto nivel de integridad de datos, SQL es todavía una opción más recomendable.

Escenarios en los que usaría SQL:

1. **Necesita un alto nivel de integridad de los datos:** SQL es mejor cuando se necesita un alto nivel de integridad de los datos. Esto se debe a las restricciones que se imponen en la estructura de la base de datos para garantizar la integridad referencial y otros tipos de integridad.

2. **Se requiere soporte para transacciones completas:** SQL es mejor cuando necesita soporte para transacciones completas. Esto significa que puede ser capaz de hacer cambios a varias tablas a la vez, y que puede deshacer las operaciones si es necesario.

3. **La aplicacion es de misión crítica:** Si su aplicación es crítica para el negocio y no puede tener tiempos de inactividad, SQL es una mejor opción para su base de datos ya que es más maduro y ha sido ampliamente utilizado durante mucho tiempo.

Escenarios en los que usaría MongoDB:

1. **Requiere alta flexibilidad:** MongoDB es una buena opción cuando se requiere una alta flexibilidad. Esto se debe a que los documentos no tienen que tener la misma estructura, lo que facilita la modificación de la estructura de datos en cualquier momento.

2. **Manejo de grandes volujenes de datos:** MongoDB es una buena opción cuando se requiere manejar grandes volúmenes de datos. MongoDB es capaz de gestionar y procesar una gran cantidad de datos simultáneamente gracias a su arquitectura de tipo "Sharing Nothing".

3. **Aplicaciones web y móviles:** MongoDB es una buena opción para las aplicaciones web y móviles debido a su rápida capacidad de respuesta y bajos tiempos de inactividad.

Para conectarse a una base de datos de MongoDB y mostrar o modificar registros, se pueden seguir los siguientes pasos:

1. Instalar y configurar MongoDB en la máquina local o en un servidor remoto.
    
2. Descargar la biblioteca del controlador de MongoDB para el lenguaje de programación que se está utilizando. Por ejemplo, para Node.js, se puede instalar el controlador usando npm:

    ```
    npm install mongodb
    ```

3. Establecer una conexión a la base de datos utilizando la biblioteca del controlador. Para hacer esto, se necesitará proporcionar el URL de la base de datos y un objeto de configuración que incluye opciones como la autenticación y la conexión en línea o fuera de línea.

    ```js
    const { MongoClient } = require('mongodb');
    const uri = 'mongodb+srv://<user>:<password>@<cluster>.mongodb.net/<dbname>?retryWrites=true&w=majority';
    const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });
    
    client.connect().then(() => {
      console.log('Connected to MongoDB');
      const db = client.db('mydb');
    }).catch((err) => {
      console.log(err);
    });
    ```

4. Una vez que se haya establecido la conexión, se pueden utilizar los métodos de la biblioteca del controlador para leer, escribir o modificar registros.

    Para leer registros, se puede utilizar el método `find()` de la colección.

    ```js
    const usersCollection = db.collection('users');
    const users = await usersCollection.find().toArray();
    console.log(users);
    ```

    Para escribir o modificar registros en MongoDB, se puede utilizar el método `insertOne()`, `insertMany()`, `updateOne()` o `updateMany()` según sea necesario.

    ```js
    const users = [{ name: 'John', age: 30 }, { name: 'Jane', age: 28 }];
    const insertResult = await usersCollection.insertMany(users);
    console.log(`Inserted ${insertResult.insertedCount} users`);

    const query = { name: 'John' };
    const newValue = { $set: { age: 31 } };
    const updateResult = await usersCollection.updateOne(query, newValue);
    console.log(`Updated ${updateResult.modifiedCount} user`);
    ```

5. Cerrar la conexión una vez que se hayan completado todas las operaciones en la base de datos.

    ```js
    await client.close();
    console.log('Disconnected from MongoDB');
    ```

Estos son los pasos básicos para conectarse a una base de datos de MongoDB y realizar operaciones CRUD en ella. Hay muchas otras opciones y métodos disponibles en la biblioteca del controlador de MongoDB, por lo que es importante leer la documentación oficial para aprender cómo aprovechar al máximo sus características.

En MongoDB, las relaciones entre diferentes documentos se pueden abordar de varias maneras. A continuación, se muestran algunas técnicas comunes utilizadas para relacionar documentos, junto con ejemplos de cómo acceder y recuperar esas relaciones desde Node.js.

1. **Referencias:** En este enfoque, en lugar de incluir toda la información en un solo documento, se guarda solo un ID de referencia a otro documento que contiene la información detallada. Por ejemplo, se puede tener una colección de usuarios y otra colección de posts, donde cada post tiene una referencia a un usuario.

    ```json
    // User document
    {
      "_id": ObjectId("507f1f77bcf86cd797439011"),
      "name": "John Doe"
    }

    // Post document
    {
      "_id": ObjectId("507f1f77bcf86cd797439012"),
      "title": "My first post",
      "body": "Some text here",
      "author": ObjectId("507f1f77bcf86cd797439011")
    }
    ```

    Para recuperar los datos relacionados, se deben realizar dos consultas: una para recuperar el documento principal (por ejemplo, un post), y otra para recuperar el documento relacionado (por ejemplo, un usuario).

    ```js
    const post = await db.collection('posts').findOne({ _id: postId });
    const authorId = post.author;
    const author = await db.collection('users').findOne({ _id: authorId });
    console.log(post.title, 'by', author.name);
    ```

2. **Incrustación/embebido:** En este enfoque, toda la información se incluye en un solo documento. Por ejemplo, se puede tener una colección de posts que contiene toda la información relacionada con los usuarios como un objeto anidado.

    ```json
    // Post document with nested user information
    {
      "_id": ObjectId("507f1f77bcf86cd797439012"),
      "title": "My first post",
      "body": "Some text here",
      "author": {
        "name": "John Doe",
        "age": 30
      }
    }
    ```

    Para acceder a los datos relacionados, solo se necesita una consulta.

    ```js
    const post = await db.collection('posts').findOne({ _id: postId });
    console.log(post.title, 'by', post.author.name);
    ```

3. **Denormalización:** En este enfoque, se copia la información de un documento a otro para evitar la necesidad de realizar varias consultas. Por ejemplo, se puede tener una colección de posts que incluye información duplicada relacionada con los usuarios.

    ```json
    // Post document with duplicated user information
    {
      "_id": ObjectId("507f1f77bcf86cd797439012"),
      "title": "My first post",
      "body": "Some text here",
      "authorName": "John Doe"
    }
    ```

    Para acceder a los datos relacionados, solo se necesita una consulta en la colección de posts.

    ```js
    const post = await db.collection('posts').findOne({ _id: postId });
    console.log(post.title, 'by', post.authorName);
    ```

Cada técnica tiene sus propias ventajas y desventajas, y la elección de una técnica dependerá de las necesidades específicas de la aplicación.

---

El patrón Modelo-Vista-Controlador (MVC) es una arquitectura de software que divide una aplicación en tres componentes principales: el modelo, la vista y el controlador. Al trabajar con MongoDB y Mongoose, el patrón MVC se puede utilizar de la siguiente manera:

- El modelo representa los datos en la base de datos MongoDB, y se definen modelos de Mongoose para manejar las operaciones en las colecciones de MongoDB.

- La vista es la parte de la aplicación que muestra información al usuario. En una aplicación web, esto puede ser una página HTML, pero también podría ser una interfaz de línea de comandos o una aplicación móvil.

- El controlador procesa las solicitudes del usuario y actúa como intermediario entre el modelo y la vista. En una aplicación web, el controlador podría ser una función que maneja las solicitudes HTTP de los usuarios.

A continuación se detallan los pasos para implementar el patrón MVC en una aplicación de Node.js con MongoDB y Mongoose:

1. Configuración de la conexión a MongoDB utilizando Mongoose:

    ```js
    const mongoose = require('mongoose');
    
    const uri = 'mongodb://localhost:27017/my-db';
    mongoose.connect(uri, { useNewUrlParser: true, useUnifiedTopology: true })
      .then(() => {
        console.log('Connected to MongoDB');
      })
      .catch((err) => {
        console.log(err);
      });
    ```

2. Definición del modelo de Mongoose para acceder a las colecciones de MongoDB. Por ejemplo, para crear un modelo de Usuarios:

    ```js
    const mongoose = require('mongoose');
    
    const userSchema = new mongoose.Schema({
        name: String,
        email: String,
        age: Number
    });
    
    const User = mongoose.model('User', userSchema);
    
    module.exports = User;
    ```

3. Definición del controlador que maneja las operaciones solicitadas por la vista y actúa como intermediario entre la vista y el modelo. Por ejemplo, para listar todos los usuarios:

    ```js
    const User = require('../models/user');
    
    const listUsers = async (req, res) => {
        const users = await User.find({});
        res.render('users/list', { users: users });
    };
    
    module.exports = { listUsers };
    ```

4. Definición de la vista mediante un motor de plantillas, como pug. Por ejemplo, para mostrar una lista de usuarios:

    ```js
    h1 Users
    ul
        each user in users
            li= user.name
    ```

Con estos pasos, se puede implementar el patrón MVC en una aplicación de Node.js con MongoDB y Mongoose. La implementación de este patrón ayuda a separar la lógica de la aplicación en componentes claramente definidos, lo que facilita la comprensión y el mantenimiento del código.

## Referencias

- [MongoDB](https://www.mongodb.com/)
- [Mongoose](https://mongoosejs.com/)

