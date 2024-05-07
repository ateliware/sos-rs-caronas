# Django Application Blueprint

Welcome to the Django Application Blueprint, a quick starter template for Django applications. This blueprint follows modularization and best practices as suggested by the acclaimed book [Two Scoops of Django 3.X](https://www.feldroy.com/books/two-scoops-of-django-3-x).

For comprehensive documentation about Django, visit the [Django Project Page](https://www.djangoproject.com/).

## Getting Started

This Django Application Blueprint runs within a Docker container, utilizing a PostgreSQL database. The project includes essential Django and Python libraries installed via pip, as listed in the `requirements.txt` file. Don't forget to create a `.env` file using the provided `.env-sample` as a template.

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

This Blueprint is integrated with Django Rest Framework, a powerful tool for constructing APIs in Django applications. We set two basic methods as examples, using SimpleJWT lib, for requesting and refreshing JWT authentication tokens. You can access these two methods to request access tokens for the application at the following URLs:

- [http://0.0.0.0:8000/api/token](http://0.0.0.0:8000/api/token)
- [http://0.0.0.0:8000/api/token/refresh](http://0.0.0.0:8000/api/token/refresh)

You'll need send email and password in payload to generate access_token and refresh_token.


### User filtering and save customization
We have included a class (GenericUserViewSet) that inherits from the default ModelViewset of DRF and that inserts a treatment to perform data filtering in the endpoint since there is an FK to the "user" model. Given a table of clients, for example, being this table used by various users to register their clients, as long as there is a column referencing the logged-in user, by inheriting this viewset, it will be responsible for filtering the data referring to the logged-in user, as well as when creating a new record, this viewset takes care of automatically inserting the user into the record. Use this viewset as a starting point whenever it is necessary to relate a table to its owning user.

An example of their use can be observed in the TermAcceptanceViewset within the term_manager app.

## Blueprint Structure

The project follows a modular structure for better organization and maintainability. As Django works with the app construction idea (DRY), we create one app called 'core' which we suggest be used for common code between other apps that the project will need.

We suggest modularizing the app into folders and files as the schema:
- `admin` (folder for admin area scripts)
- `migrations` (migrations generated for the app)
- `models` (we suggest a file for each model in the app)
- `tests` (we suggest a folder for each funcionallity - models, views, apis, etc)
- `views`
- `apis` (optional when the app contains APIs)

Besides the files: `apps.py` (with information for the app) and `urls.py` (specifying the URL for views and APIs of the app).

We also separate, for more intuitive interaction, in the folder `config`, the settings of the application. And inside it, the settings in files independently.

## Custom Admin Theme

We included the Jazzmin Theme for customizing the Admin area in the requirements file. If you want to use this theme, you need to add it at the top of the INSTALLED_APPS variable, as shown below:

```
INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    [...]
]
```

For more information about Jazzmin Theme, click [here](https://django-jazzmin.readthedocs.io/).

## Usage and examples 

Above some insides to start developing using this blueprint

### Examples

We provide some examples of how to use Django basically, in the sample app called **address_manager**.
**WIP Section**

### Users and Authentication
We modified the default behavior of Django to utilize email and password as authentication credentials. To achieve this, we introduced CustomUser and CustomGroup models. From now on, when referencing any application user, always use a foreign key (FK) pointing to the CustomUser table.

### Django for Monolithic Applications

We included an example of template creation, where Django serves the data directly to the client renderer. To access this, visit [http://0.0.0.0:8000/city/](http://0.0.0.0:8000/city/). We used Class-Based Views (CBVs) to create this sample, offering a streamlined approach for common CRUD operations.

To explore further, check the view file (apps/address_manager/views/city_view.py) for a closer look at this example.

For enhanced control over view logic, consider overriding class methods to maintain architectural consistency.

### API use with Django Rest Framework

Besides that, we demonstrate examples of how to use the REST framework for the models created in the address app.

We used (and recommend) CBVs to streamline the development of simple CRUD endpoints (file: apis/state_viewset.py), and override methods where greater control and logical handling were necessary (file: apis/city_viewset.py). Additionally, we've created an example where the endpoint is not associated with any specific table (file: apis/fake_cities_viewsets.py).

We've built two sets of routes (api/states/ and api/cities/) that encapsulate the main REST methods used for basic applications. Both sets of routes have authenticated access via [token JWT](#django-rest-framework). The **access_token** should be sent in the request header as follows:
```
{ "Authorization": "Bearer <access_token>"}
```

Consider the endpoint http://0.0.0.0:8000/api/states/

The GET method returns a list of all registered states, along with pagination information, as shown in the following example:
```
{
	"count": 2,
	"next": null,
	"previous": null,
	"results": [
		{
			"id": 2,
			"name": "São Paulo",
			"code": "SP",
			"created_at": "2024-03-06T17:15:12.688117-03:00",
			"updated_at": "2024-03-06T17:15:12.688147-03:00",
			"is_active": true
		}
	]
}
```
To create a new state, simply send a POST request to the same endpoint with the following payload:
```
{
	"name": "São Paulo",
	"code": "sp"
}
```
To retrieve the details of a state, update, or delete it, simply append the primary key to the end of the endpoint, like so: http://0.0.0.0:8000/api/states/2/

In the endpoint for creating cities (http://0.0.0.0:8000/api/cities/), a modification was made to the default creation logic, where you must send the city name and the state code:"
```
{
	"name": "Campinas",
	"state_code": "SP"
} 
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

**Notes**

If the apps **address_manager** and **term_manager** does not make sense for your application, just revert its migration and drop the folders.
To revert the specific migration, run the command:

```
python manage.py migrate address_manager zero
python manage.py migrate term_manager zero
```

You must also remove the routes for address_manager and term_manager in the file config/urls.py and remove the app lines from the file config/settings/installed_apps.py.

## Be Collaborative, My Friend!

Have a great job using the Django Blueprint. Feel free to explore and modify this blueprint to fit your project requirements!

---
This README is provided as a guide to assist in getting started with the Django Application Blueprint. For any further assistance or inquiries, please refer to the official Django [documentation](https://docs.djangoproject.com/en/5.0/) or consult the project's contributors.
# sos-rs-caronas
