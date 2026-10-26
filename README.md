# CS-340 Client/Server Development: Grazioso Salvare Dashboard

This repository contains my portfolio artifacts from CS-340 Client/Server Development at Southern New Hampshire University.

## Contents

- `ProjectTwoDashboard.ipynb`: the final Grazioso Salvare dashboard, built with Dash, Plotly, and Dash Leaflet
- `CRUD_Python_Module.py`: the reusable CRUD module from Project One that connects the dashboard to MongoDB
- `ProjectTwo_README_LeanneByrne.docx`: the Project Two README, covering functionality, rescue filter criteria, testing, and setup steps
- `Grazioso Salvare Logo.png`: the logo displayed on the dashboard

## About the Project

Grazioso Salvare, an organization that trains dogs for search and rescue, needed a way to find shelter dogs that are good training candidates. The dashboard connects to a MongoDB database of Austin Animal Center outcome records and lets staff filter dogs by rescue type (Water Rescue, Mountain or Wilderness Rescue, and Disaster or Individual Tracking), browse and sort the results in an interactive data table, see the breed mix of the current results in a pie chart, and locate a selected dog on a map. The application follows the Model-View-Controller pattern: MongoDB is the model, the Dash layout is the view, and Dash callbacks that call the CRUD module act as the controller.

## Reflection

### How do you write programs that are maintainable, readable, and adaptable?

I write code in small, focused pieces with clear names, comments that explain why a choice was made, and consistent error handling. The CRUD Python module from Project One is the best example from this course. It wraps every database operation in an AnimalShelter class with four methods (create, read, update, and delete), takes credentials as constructor parameters instead of hardcoding them, validates input before touching the database, and returns predictable values such as True or False and lists of documents. Because of that, the Project Two dashboard never had to contain any database code. Each callback simply called `db.read()` with a query, which kept the dashboard code short and readable and meant that any database change only needed to be made in one place. I tested the module on its own before building the dashboard, so when something broke later I could narrow the problem down quickly. In the future, this module could be reused for any application that needs to work with a MongoDB collection, such as an adoption website, a reporting script, or a REST API. Pointing it at a different database or collection only requires different constructor arguments.

### How do you approach a problem as a computer scientist?

I start by breaking the client's requirements into specific, testable pieces. For Grazioso Salvare, I translated each rescue type in their specification into a precise MongoDB query: the preferred breeds became an `$in` list, the training age range became `$gte` and `$lte` conditions on age in weeks, and the sex requirement became an exact match on `sex_upon_outcome`. I then built the project in layers, starting with the database (importing data, creating indexes, and setting up a user with least-privilege access), then the CRUD module, then the dashboard, and I tested each layer before moving to the next. This project differed from my earlier coursework because it was built around a client's needs rather than a set of isolated exercises, and every module built directly on the previous one, so early design decisions such as making the CRUD module reusable paid off later. For future client requests, I would keep using this approach: gather and clarify requirements first, design the data model around how the data will actually be queried, add indexes for the most common queries, follow least privilege for database accounts, and use unit, integration, and regression testing as each feature is added.

### What do computer scientists do, and why does it matter?

Computer scientists turn real-world problems into working systems that help people make better decisions with less effort. Without a tool like this dashboard, Grazioso Salvare staff would have to search through thousands of shelter records by hand to find dogs that match their breed, age, and sex criteria. The dashboard narrows that search to the right candidates in one click, shows the results in a clear table and chart, and maps where each dog is located. That saves staff time, reduces the chance of overlooking good candidates, and lets the organization focus on training dogs that will go on to save lives. Because the code is modular and documented, other organizations could adapt it for their own needs as well.

## Technologies

MongoDB, Python, PyMongo, Dash, Plotly, Dash Leaflet, Pandas, and Jupyter Lab in the Codio environment.

## Contact

Leanne Byrne
