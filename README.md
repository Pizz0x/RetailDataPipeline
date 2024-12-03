# RetailDataPipeline

### Virtual Environment Configuration:

Upgrade the Python's package installer to its latest version: `python.exe -m pip install --upgrade pip`

Installing Pandas library: `pip install pandas`
<br>

Installing SQLAlchemy library: `pip install sqlalchemy psycopg2`
<br>

Initiate the virtual environment: `source airflow_env/bin/activate`
You need it to run postgres and airflow operation, do it every time you work on the project.
<br>

Start PostgreSQL : `sudo service postgresql start`


### Installation of AirFlow Apache:

Install pip: 
`sudo apt install python3-pip`
<br>

Install the virtual environment:
`sudo pip3 install virtualenv`
<br>

Install airflow:
`pip3 install apache-airflow[gcp,sentry]`
<br>

` airflow db init`

Create an airflow user:
`airflow users create --username admin --password admin --firstname admin --lastname admin --role Admin --email filippo.pizzo@vub.be`
<br>

`airflow users list`
<br>

Install the necessary dependencies for interacting with PostgreSQL databases: `pip install apache-airflow-providers-postgres`

Run the scheduler: `airflow scheduler`
<br>

Run the web server: `airflow webserver -p 8080`

### Installation of Postgres:

`sudo sh -c 'echo "deb [signed-by=/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc] https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'`
<br>

`wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -`
<br>

`sudo apt-get -y install postgresql`




