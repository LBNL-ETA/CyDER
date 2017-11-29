CyDER - Django apps
======

Apps
--------

Each app focus on implementing a part of the CyDER:
- api: api entry point  
- main: implement the main frame of the website (login/logout, homepage) and resources used site wide  
- models: implement the db model for the grid models, api to access them, tools to visualize them...  
- projects: implement the the project manager, tools and api  
- ...

API
-------

The api app serve as a unified entry point to access the api defined in the different app of the website. So the api code can be written inside each application, and accessible through /api/...

To do so, each app that need to expose an api should contain an api.py file.  
Im this file, import `from cyder.api.urls import apirouter, urlpatterns`, write the views for the api and expose them using apirouter/urlpatterns.
