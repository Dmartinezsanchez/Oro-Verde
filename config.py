import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', '1980')  # Clave secreta para sesiones y protección CSRF
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '1234')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'tienda_naturista')

