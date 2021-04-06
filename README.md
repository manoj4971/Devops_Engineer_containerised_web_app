# Web application 
##  Tool
**Python**, the most favorite language and used language in most of my projets motivated me in choosing this as basic tool . 

Python is know for its simplicity and its clean and concise way of implementing things. 

As its most preferred languages to build backend applications and its growing domain in web applications.

The ease of implementation, and a supportive community. 
## Web Framework 
### Flask 
 
Flask is simple and ease to get started when compared to  Django, as it is heavy for building web applications, 

Another major reason was companies and organisation moving away from monolithic applications towards the era of the cloud. 

Flask is used a webframe work in this task. 

### Jinga
Jinja is used for directly importing  the python variables and functions to HTML file, 
Flask supports Jinja Template . 
It is  a modern and designer user friendly templating language available for Python.

HTML file implemented with Jina Template enables to use python code directly on web-development
which enhancing the efficiency of the code structure.

## Requirements & Setup
- Python — 3.7 would be great
- Pycharm community IDE because it’s awesome & free

### Conceptual Path  

- requirements.txt file  stores the dependiencies and plugins, which is given in dockerfile to run the application.
- Backend functional coding can be seen in app.py file and connected with index.html file.
- Index.html responsible for front end funtionalities provisioning 
- Flask acts as a communication channel between app.py and index.html file 

## Implementation : 
- Python application running

***python -m flask run***

- Docker Build

***docker build --tag python-docker .***

- Docker Run

***docker run -it -v /var/run/docker.sock:/var/run/docker.sock -v /usr/bin/docker:/usr/bin/docker --publish 8080:8080 python-docker***

## Output 

- The tool listens to the port 8080 and exposes a http endpoint and returns the docker containers running locally containing information from each conatiner (conatiner name , container id ,status). 
- Search query enables to access the particular conatiner information by passing container name. 


https://user-images.githubusercontent.com/76168664/113769373-3727c400-9721-11eb-9f89-dc0838ebc5d9.PNG










