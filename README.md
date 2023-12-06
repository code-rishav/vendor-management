# VENDOR MANAGEMENT SYSTEM

This API serves as the backend for a vendor-management platform, facilitating various functionalities related to managing purchase orders, vendors, hostorical performance and authentication.

The API has been tested in [Postman](https://www.postman.com/).
The documentation for the API has been developed using Postman.
[View API Documentation](https://documenter.getpostman.com/view/28292091/2s9YeN2UEa)

Please ensure following dependencies to be installed on your system:
- Python version 3 or higher
- Package manager (pip)

## Installation 
Clone the repository
```sh
git clone https://github.com/code-rishav/vendor-management.git
```
move to project directory
```sh
cd vendor-management
```
make sure to have virtual environment installed
```sh
pip install virtualenv
```
create a virtual environment
for windows and linux
```sh
python -m venv <virtual environment name>
```
activate virtual environment
for windows
```sh
<virtual environment name>\Scripts\activate
```
for linux
```sh
source ./<virtual environment name>/bin/activate
```

install the required packages
```sh
pip install -r requirements.txt
```

upgrade the setuptools
```sh
 pip install --upgrade setuptools
```

create migrations for the models
you need to run the command for specific apps as migrations files have been excluded from the repo
```sh
python manage.py makemigrations
python manage.py makemigrations orer vendor performance
python manage.py migrate
```

create an admin user for the system 
```sh
python mangage,py createsuperuser
```

run the server
```sh
python maanage.py runserver <port>
```
example:
```sh
python manage.py runserver 8080
```

to create peformance data for all the vendors

```sh
python manage.py task
```

to test the api run the test cases:
```sh
python manage.py test
```

Addtional Improvements
- Celery can be used to create a scheduled generation of historical performance data for vendors
- Seprate endpoint for status update should be made, which will help implementing the logic without creating an overhead for post_save or pre_save

