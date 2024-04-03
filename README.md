# Luna_Hydrophonic
Repository cointains CRUD app in Django developed for Luna Scientific recruitment task.


# Installation
```bash
pip install virtualenv
virtualenv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Usage
```bash
cd CRUD
python manage.py runserver
```

## Datebase setup
In <i> settings.py </i> fill required fields
```python
        'NAME': 'your-database-name',
        'USER': 'your-user-name',
        'PASSWORD': 'your-password',
        'HOST': 'your-localhost',
        'PORT': '5432',
```
Also add a new table to your db using this script
```sql
create table sensors (
	user_id INTEGER,
	system_id INTEGER,
	ph VARCHAR(99),
	water_temperature VARCHAR(99),
	TDS VARCHAR(99),
	created_at TIMESTAMP default CURRENT_TIMESTAMP
);
```

### Endpoints

<ul>
    <h5> Green endpoints are login required </h5>
    <h5> / </h5>
    <h6> Renders the home page. </h6>
    <h5> /register </h5>
    <h6> Registers a new user. </h6>
    <h5> /login </h5>
    <h6> Logs in a user.  </h6>
    <h5 style="color:green;"> /dashboard </h5>
    <h6> Renders the dashboard page. </h6>
    <h5 style="color:green;"> /create </h5>
    <h6> Creates a new hydroponic system. </h6>
    <h5 style="color:green;"> /update/pk </h5>
    <h6> Updates an existing hydroponic system. </h6>
    <h5 style="color:green;"> /system/pk </h5>
    <h6> Renders the details of a hydroponic system. </h6>
    <h5 style="color:green;"> /delete/pk </h5>
    <h6> Deletes an existing hydroponic system. </h6>
    <h5> /logout </h5>
    <h6> Logs out the current user. </h6>
    <h5> /stream </h5>
    <h6> Simulates a sensor reading and updates the database with the sensor data. </h6>
</ul>