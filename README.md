# webshop-task

## Running this project
To run the project clone the project:
```
git clone https://github.com/bassamalasadi/webshop-task.git
```
Install python version 3.8 on your computer:
[Download Python](https://www.python.org/downloads/)
then follow these steps which will install the virtual environment and create new `env` folder: 
```
pip install virtualenv
virtualenv env
```

To activate the virtual environment on :
mac/linux terminal
```
source env/bin/activate
```
on windows terminal
```
env\Scripts\activate
```
In the base directory of this project

Then you need to install the project backages from requirements.txt
```
pip install -r requirements.txt
```
Finally run the project 
```
python manage.py runserver
```
Then go to:
```http://127.0.0.1:8000```
or go as an admin to:
```http://127.0.0.1:8000/admin/```.
The username `bassam` and password `badboy999` to login in Django administration
