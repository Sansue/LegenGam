<p align="center">
<img alt="logo" src="./graph/static/LogoChart.png" width="256" height="256">
</p>

--- 
# LegenGam

This project was made by Axel Maral and Ethan Girard during our internship at Cenareo,
from june to july 2023.

Its aim was to train us on the techs and libs (django, chart.js, html, css, js...) 
needed to implement a statistics tool in the Cenareo web app.

---

## Setup

The project is a very simple django website containing one app.

In order to make this work, you just need to:
- Clone this repository
- Get our [Database dump](https://drive.google.com/file/d/1H-V_T0W8le9wx4lmS4wzHFle3vnip9g0/view?usp=sharing) that contains all the LoL games
- Set up a [Python venv](https://www.w3schools.com/django/django_create_virtual_environment.php) in the repository
- In this venv, install [Django](https://www.w3schools.com/django/django_install_django.php) and psycopg2 : ```pip install psycopg2``` or ```pip install psycopg2-binary```
- [Restore the database dump](https://www.postgresql.org/docs/current/backup-dump.html) and [connect the newly created database to your django project](https://docs.djangoproject.com/en/4.2/ref/databases/#postgresql-notes)
- Finally, run ```python manage.py runserver``` to start a local server [in which you can see the site](http://127.0.0.1:8000/home/)

---

## Chart viewer

### Description

The chart viewer is a tool that takes datasets and allows the user to see the resulting data in charts 
of his choice with multiple options to personalize them (chart type, scales, number of objects displayed, sorting) and export 
the result in a PDF.

Its principle is quite simple : 

You first have a unique chart viewer in which there is the example chart.

When you click a dataset other than the default one displayed on the screen, 
the frontend asks the django backend with a "fetch" request a JSON file with the needed data. It then treats this data
and all the chart modifications with js.

You can also add and remove chart viewers on your page to see multiple charts at once, which works the same way as the
datasets with AJAX requests.

See here where the chart viewer files are located in the project :
- The html base file : 
  - ```graph/templates/index/ajax_graph.html```
- The base (and only, as of right now) chart viewer component : 
  - ```graph/templates/index/ajax_graph_component.html```
- The javascript that makes everything work : 
  - ```graph/static/js/ajax_graph.js```
- The django urls file for backend requests (The page url is 'ajax_graph' and AJAX requests are 'get_html' and 'get_data') : 
  - ```graph/urls.py``` 
- The django views file for the same purpose : 
  - ```graph/views.py```
- The python file that sends the html component to the front end through the AJAX request : 
  - ```graph/ajax_graph_html_renderer.py```


### Modifying the ajax_graph.js to Add New Datasets and HTML Components

To modify the provided script to add new datasets and handle different HTML components, you'll need to make changes in a few key areas. Here's a step-by-step guide:

1. **Adding a New Dataset**

   To add a new dataset, you'll need to make changes in the `get_data` and `handle_config` functions.

   - In the `get_data` function:
     - Add a new `if` condition to handle the new dataset name. For example:
       ```javascript
       else if (dataset === "new_dataset") {
           // Handle the new dataset
       }
       ```
     - Inside the condition, fetch the data for the new dataset and populate the necessary variables (`all_charts[i].all_data`, `all_charts[i].chart_types`, etc.) accordingly.
     - Create the configuration for the new dataset using the `handle_config` function.

   - In the `handle_config` function:
     - Add a new `else if` condition to handle the new dataset name. For example:
       ```javascript
       else if (all_charts[i].current_dataset === "new_dataset") {
           // Handle the new dataset configuration
       }
       ```
     - Inside the condition, define the necessary labels, colors, datasets, and options for the new dataset.
     - Update the returned configuration object with the new dataset's information.

2. **Handling Different HTML Components**

   To handle different HTML components, you'll need to modify the `add_new_viewer` and `create_viewer_objects` functions.

   - In the `add_new_viewer` function:
     - Modify the `formData.append('html_type', 'base')` line to set the appropriate `html_type` based on the component you want to add. For example:
       ```javascript
       formData.append('html_type', 'new_component');
       ```
     - Ensure that the server-side code (`get_html/` endpoint) returns the correct HTML template for the new component.

   - In the `create_viewer_objects` function:
     - Add a new `if` condition to handle the new HTML component. For example:
       ```javascript
       if (html_type === 'new_component') {
           // Handle the new component's creation and event listeners
       }
       ```
     - Inside the condition, create the necessary objects, buttons, and event listeners specific to the new component.

3. **Additional Considerations**

   - If your new dataset requires additional server-side endpoints for data retrieval, you'll need to implement those endpoints and modify the `fetch` requests in the `get_data` function accordingly.
   - Depending on the complexity of the new component, you may need to modify the server-side code to generate the appropriate HTML template for the new component.

