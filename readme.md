# DIEUDONNE-DASHBOARD-HTML


An app for Visualizing Loan and institutional transactions

## Getting started

These instructions will help get a copy of this project up and running on your local machine in no time.

### Prerequisites

What you will need you will need to run this app successfully:
```
Python 3.7.x

Django 3.0.x

Python SimpleServer (Comes builtin to python)
```

You can get Python [here](https://www.python.org/downloads/release/python-370/) and PostgreSQL [here](https://www.postgresql.org/download/)

### Installation

You can install and setup this project locally using the following steps:

Download the app from the GitHub Repo
```
> git clone https://github.com/dtekluva/DIEUDONE_CRM_ANALYTICS.git

> cd DIEUDONE_CRM_ANALYTICS
```

```
> git clone https://github.com/dtekluva/DIEUDONNE-DASHBOARD-HTML.git

> cd DIEUDONNE-DASHBOARD-HTML
```

### Setup

Update Database values to point new host: 

In settings.py update the following 

```
HOST =     "<HOSTNAME>"
USERNAME = "<USERNAME>"
PASSWORD = "<XXXXXXX>"
DB =       "<DB_NAME>"
```

Start python server: 

```
> python manage.py runserver
```

Start Simple local server (To serve HTML): 

```
> python -m http.server <port-value>
```

### Usage

Visit webpage:

```
localhost:<port_name>
```

