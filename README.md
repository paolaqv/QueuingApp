# QueuingApp
###
```sh
cd QueuingApp
```
### entorno virtual

```sh
python -m venv venv
```
```sh
venv\Scripts\activate
```
### extensiones necesarias

```sh
pip install Flask SQLAlchemy Flask-Migrate psycopg2

pip install PyJWT

pip install simpy numpy pandas matplotlib

```
### crear bd en pgAdmin4 sin agregar tablas

### migraciones de BD

```sh
flask db init
```
```sh
flask db migrate -m "inicializar migraciones"
```
```sh
flask db upgrade
```

###  ejecutar

```sh
flask run
