sudo /etc/init.d/mysql restart

sudo mkdir /home/box/web/public/img
sudo mkdir /home/box/web/public/css
sudo mkdir /home/box/web/uploads

sudo chown -R www-data /home/box/web

#sudo ln -sf /home/box/web/etc/nginx.conf  /etc/nginx/sites-enabled/default
#sudo /etc/init.d/nginx restart

#sudo ln -s /home/box/web/etc/gunicorn.conf   /etc/gunicorn.d/test
# sudo /etc/init.d/gunicorn restart
cd /home/box/web
#sudo gunicorn -c /etc/gunicorn.d/test hello:app &
cd ask
#sudo gunicorn --bind 0.0.0.0:8000 ask.wsgi:application &

mysql -uroot -e "create database ask"
mysqladmin -u root password pass
./manage.py syncdb

sudo /etc/init.d/nginx stop
sudo python /home/box/web/ask/manage.py runserver 0.0.0.0:80
