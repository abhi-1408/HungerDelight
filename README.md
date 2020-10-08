# Hunger Delight

Created a Webapp in Django for managing store, item, merchant, order and performing crud operations on these entities.

## Tech Stack Used

- Backend
  - Django 3.1
  - MySql 8.0
  - Django RestFramework 3.12
  - PyTest
  - Celery
  - RabbitMQ

  - StructLog
  - Silk Profiling
  - Locust


## Features

- Ability to add, update, delete, view(list & detail) for merchant, item, store, order
- Ability to view
  - all items belonging to a merchant
  - all orders placed for a specific merchant
  - all stores linked with a specific merchant
  - all items linked with a specific store
  - all orders placed for a specific store


## Getting Started

To get a local copy up and running, follow these simple steps.

### Installation

```sh
- git clone https://github.com/abhi-1408/HungerDelight
- virtualenv venv
- source venv/bin/activate
- pip install -r requirements.txt
  
  For mac:
  - brew install rabbitmq

- cd HungerDelight
- python manage.py migrate
- python manage.py collectstatic
- python manage.py runserver
```

### For Testing

```
cd HungerDelight/hungerDelight

Before running test
  - in settings.py change CELERY_TASK_ALWAYS_EAGER = True
- In the Terminal
	- pytest (to run the test suite)

- after running test make CELERY_TASK_ALWAYS_EAGER = False again
```

## API DOCS Links

Refer [API DOCS](https://github.com/abhi-1408/HungerDelight/blob/master/README_API.md).
