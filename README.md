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
        'NAME': 'your-database-name',
        'USER': 'your-user-name',
        'PASSWORD': 'your-password',
        'HOST': 'your-localhost',
        'PORT': '5432',

Also add new table to your db using this script
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