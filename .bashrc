export ANACONDA_ADMIN=igontar@mvd.ru
export MAIL_USERNAME=igontar@mvd.ru
export MAIL_PASSWORD=#Swordfish100
export MAIL_SERVER=post.mvd.ru
export MAIL_PORT=587
export DATABASE_URL=postgresql://postgres:swordfish1@localhost/postgres_product
python manage.py deploy

waitress-serve --host=10.107.123.131 --port=5000 --url-scheme=http manage:app