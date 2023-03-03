# coder-t2a2
Webserver Flask API project for CoderAcademy course.

[Github Repo](https://github.com/willr42/coder-t2a2).

[Project Management Board](https://trello.com/b/C1nWwPAe/t2a2-flask-api).

# R1 Identification of the problem you are trying to solve by building this particular app.

Amateur horticulturalists are faced with a huge knowledge area they need to track - all the varieties of plants they can keep. How much water they need, how often, what sort of soil they need, their climate conditions, and so on. And tracking the plants you actually own can be just as complicated.

# R2 	Why is it a problem that needs solving?

My API will allow a user to create their own virtual Garden. They can register an account using their email. They can then create a new Garden, and begin adding plants to it. This Garden will track the plants inside it, and track what plants have been watered recently, what have yet to be watered, and if any are overdue for their next watering. Creating this virtual representation of a garden means users can be in more control of their hobby than ever.

# R3 Why have you chosen this database system. What are the drawbacks compared to others?

TODO answer here

# R4 	Identify and discuss the key functionalities and benefits of an ORM

TODO answer here

# R5 	Document all endpoints for your API

TODO answer here

# R6 	An ERD for your app

![ER Diagram](docs/er-diagram.png)

# R7 	Detail any third party services that your app will use

TODO answer here

# R8 	Describe your projects models in terms of the relationships they have with each other

TODO answer at end of project

# R9 	Discuss the database relations to be implemented in your application

There are four main relations in this project. Users, Gardens, Plants, and the table that connects a Garden with the Plants inside it (called GardenPlants).

Users are how we represent the user in the app. The primary key is a surrogate key, an autoincrementing integer ID. They have a `full_name` field to store their personal information, which might be important for later expansion of the API or a frontend. They have an email for communicating with users, and a field called `expert` which determines whether they're able to make changes to the Plants database.

A User can only have one Garden. Each Garden has a connection to the user that created it, and a `creation_date` to keep track of when it was created, a `garden_type` which represents what sort of Garden the user has (eg. "indoor", "outdoor" or even "terrarium") and a surrogate primary key.

Plants are the main data being stored in the API, along with the Gardens and their connection to them. The Plant model contains a field of `name`, which represents the scientific name of the plant, and an array of strings called `common_name`. Arrays are a Postgres feature and allow us to store multiple strings in a singular field. Both `cycle` and `watering` are enums, another Postgres feature. Enums are a static list of values that ensures that any data we insert must be drawn from this list. This has the effect of limiting duplication and enforcing specific values **at the database level**, rather than requiring backend logic. The primary key is the ubiquitous surrogate key.

GardenPlants is the final model, which connects the Garden a User has created with Plants. Thus we have two foreign keys, one from Gardens, one from Plants. The `last_watered` field keeps track of when a user has last watered a particular plant. The `placement` field tracks the sun conditions the plant is placed in (full shade, full sun, or a mix). `Healthiness` is an integer from 1 to 10 that tracks exactly that — how well a plant is doing (10 being peak condition, 1 being on its last legs). Finally, the surrogate key of `garden_plant_id`.

# R10 	Describe the way tasks are allocated and tracked in your project

While I'm a team of one, I'm running this project in an Agile way. I've developed a backlog of features that I need in my app. There are some dependencies, which means being aware of assigning myself tasks before I'm able to actually complete them, so I'm using a Trello board where the hierarchy in the list represents their ability to be completed. When generating the backlog, I left notes for myself in terms of potential pitfalls or things to watch out for. 

The process involves moving each card into In Dev, where I work on the particular feature. Once complete, I move it to Dev Done. Tasks in Dev Done are considered provisionally complete. In a regular rhythm, I revisit the tasks in Dev Done and consider their future. Either they have generated further tasks I couldn't foresee, which go into the backlog. Or they require further development that I couldn't foresee, so they stay in this column. Or they are fully completed, in which case they enter Done.

This Kanban style of working is very visual and tactile, and I found it worked well on the previous assignment.

For full details, see my [Garden API Trello](https://trello.com/b/C1nWwPAe/t2a2-flask-api) board.
