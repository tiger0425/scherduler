## Astroboy
quite useful components to schedule the selenium task .


## Features
* High-availability cluster
* each component just do one thing 

## Release note
* dags/
    * tasks/ - the root module , when you add task ,please import this.
        * common/ - for some decorator or common use ,please always write here. 
        * dal/ - for data base control.
        * driver/ - 
        * ip/
        * log/
        * models/
        * worker/
        * settings.py
    * run_register_japan.py - the dag job 


## TODO LIST
* [x] - update the  puckel/docker-airflow base image with ubuntu base image.
* [x] - use the log system and map to local. 
* [x] - add timeout for func or use .
* [x] - add elk log collector.
* [ ] - use the jianjia template to config the require airflow configuration(or use the file map system).
