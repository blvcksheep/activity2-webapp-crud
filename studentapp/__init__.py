from flask_mysqldb import MySQL
from flask import Flask

app = Flask(__name__)
app.secret_key = "secreto-sa-pato"

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'studentapp'

mysql = MySQL(app)

from studentapp import routes