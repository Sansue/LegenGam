<p align="center">
<img alt="logo" src="./graph/static/LogoChart.png" width="256" height="256">
</p>

--- 
#### LegenGam

This project was made by Axel Maral and Ethan Girard during our internship at Cenareo,
from june to july 2023.

Its aim was to train us on the techs and libs (django, chart.js, html, css, js...) 
needed to implement a statistics tool in the Cenareo web app.

---

#### Setup

The project is a very simple django website containing one app.

In order to make this work, you just need to:
- Clone this repository
- Get our [Database dump](https://drive.google.com/file/d/1H-V_T0W8le9wx4lmS4wzHFle3vnip9g0/view?usp=sharing) that contains all the LoL games
- Set up a [Python venv](https://www.w3schools.com/django/django_create_virtual_environment.php) in the repository
- In this venv, install [Django](https://www.w3schools.com/django/django_install_django.php) and psycopg2 : ```pip install psycopg2``` or ```pip install psycopg2-binary```
- [Restore the database dump](https://www.postgresql.org/docs/current/backup-dump.html) and [connect the newly created database to your django project](https://docs.djangoproject.com/en/4.2/ref/databases/#postgresql-notes)
- Finally, run ```python manage.py runserver``` to start a local server [in which you can see the site](http://127.0.0.1:8000/home/)

---

#### Chart viewer

Now for the interesting part of the project (at least according to cenarists) :

The chart viewer is a tool that takes datasets and allows the user to see the resulting data in charts 
of his choice with multiple options to personalize them (chart type, scales, number of objects displayed, sorting) and export 
the result in a PDF.

Its principle is quite simple : When you click a dataset other than the default one displayed on the screen, 
the frontend asks the django backend with a "fetch" request a JSON file with the needed data. It then treats this data
and all the chart modifications with js.

See here where the chart viewer files are located in the project :
- The html base file ![](./readme_images/ajax_graph_html.png)
