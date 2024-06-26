# Guide for developers

This application was developed using a Django Application follows modularization and best practices as suggested by the acclaimed book [Two Scoops of Django 3.X](https://www.feldroy.com/books/two-scoops-of-django-3-x).

For comprehensive documentation about Django, visit the [Django Project Page](https://www.djangoproject.com/).

## Getting Started

This Django Application runs within a Docker container, utilizing a PostgreSQL database. The project includes essential Django and Python libraries installed via pip, as listed in the `requirements.txt` file. Don't forget to create a `.env` file using the provided `.env-sample` as a template.

### Let's Work

To begin, ensure Docker is installed on your system. Then, build the container using the following command and navigate into it:


```
docker-compose up --build
```


Once the application is up, you can access it at: [http://0.0.0.0:8000/](http://0.0.0.0:8000/).

To access the container, use the following command:


```
docker exec -it CONTAINER_NAME sh
```

To find the name of the container, run `docker ps`.

## Database and Migrations

Within the Docker container, create the tables for the database using the follow command:


```
python manage.py migrate
```

## Tips and Tricks

To create an initial user to access the application or authenticate endpoints later, run the command:

```
python manage.py createsuperuser
```
For create a set of database basic data (Brazilian States, Cities), run the command:
```
python manage.py seed_basic_data
```


## Django Administration Area

Access the Django administration area at [http://0.0.0.0:8000/admin](http://0.0.0.0:8000/admin). Inside the admin area, you can manage the tables city and state created by the app *address_manager* to exemplify a Django app. The CRUDs are generated with (insignificantly) code in the *apps/address_manager/admin.py* file.

**Notes**

We create a basic model (apps/core/base_model.py), which contains fields extending the other tables, give a closer look.

## Django Rest Framework

The application is integrated with Django Rest Framework, a powerful tool for constructing APIs in Django applications. We set two basic methods as examples, using SimpleJWT lib, for requesting and refreshing JWT authentication tokens. You can access these two methods to request access tokens for the application at the following URLs:

- [http://0.0.0.0:8000/api/token](http://0.0.0.0:8000/api/token)
- [http://0.0.0.0:8000/api/token/refresh](http://0.0.0.0:8000/api/token/refresh)

You'll need send cpf and password in payload to generate access_token and refresh_token.


### User filtering and save customization
We have included a class (GenericUserViewSet) that inherits from the default ModelViewset of DRF and that inserts a treatment to perform data filtering in the endpoint since there is an FK to the "user" model. Given a table of clients, for example, being this table used by various users to register their clients, as long as there is a column referencing the logged-in user, by inheriting this viewset, it will be responsible for filtering the data referring to the logged-in user, as well as when creating a new record, this viewset takes care of automatically inserting the user into the record. Use this viewset as a starting point whenever it is necessary to relate a table to its owning user.

An example of their use can be observed in the TermAcceptanceViewset within the term_manager app.

## Application Structure

The project follows a modular structure for better organization and maintainability. As Django works with the app construction idea (DRY), we create one app called 'core' which we suggest be used for common code between other apps that the project will need.

We suggest modularizing the app into folders and files as the schema:
- `admin` (folder for admin area scripts)
- `migrations` (migrations generated for the app)
- `models` (we suggest a file for each model in the app)
- `tests` (we suggest a folder for each funcionallity - models, views, apis, etc)
- `views` (folder containing the views created)
- `apis` (optional when the app contains APIs)

Besides the files: `apps.py` (with information for the app) and `urls.py` (specifying the URL for views and APIs of the app).

We also separate, for more intuitive interaction, in the folder `config`, the settings of the application. And inside it, the settings in files independently.

## Custom Admin Theme

We included the Jazzmin Theme for customizing the Admin area in the requirements file.

```
INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    [...]
]
```

For more information about Jazzmin Theme, click [here](https://django-jazzmin.readthedocs.io/).

## Usage

Above some insides to start developing using this project

### Users and Authentication
We modified the default behavior of Django to utilize cpf and password as authentication credentials. To achieve this, we introduced CustomUser and CustomGroup models. From now on, when referencing any application user, always use a foreign key (FK) pointing to the CustomUser table.


### API use with Django Rest Framework

Besides that, we have a couple of apis developed, which can be accessed in a swagger in the follow link:
[swagger](http://0.0.0.0/api/swagger) (must be running the application in DEBUG=True mode)

To access authorized apis use the **access_token** send it in the request header as follows:
```
{ "Authorization": "Bearer <access_token>"}
```

### Usage

As we modify the default app structure of Django, to create new apps in the application run the following commands:


```
cd apps
python ../manage.py NEW_APP_NAME
```

**Important**

You need to change the name in the `NEW_APP/apps.py` file, adding the 'apps' directory prefix in the name variable, as the example:

```
name = "apps.NEW_APP_NAME"
```


## Be Collaborative, My Friend!

Have a great job using our Django Application!

---
This README is provided as a guide to assist in getting started with the Django Application Blueprint. For any further assistance or inquiries, please refer to the official Django [documentation](https://docs.djangoproject.com/en/5.0/) or consult the project's contributors.

---

Feito com ♥
