# Backend

## Prerequisites

- python 
- [Frontend](https://github.com/Vasya-556/TestTaskFrontend)
  
## Setup

1. Create a virtual environment and activate it:

```bash
cd TestTaskBackend
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

2. Install dependencies 
```bash
cd backend
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```

3. Run server
```bash
python manage.py runserver
```

## Postman 

[Postman endpoints](./TestTask.postman_collection.json)