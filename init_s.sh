sudo /etc/init.d/mysql restart
sudo chown -R www-data /home/box/web

mysql -uroot -e "create database ask"
mysqladmin -u root password pass
cd /home/box/web/ask
./manage.py syncdb

sudo /etc/init.d/nginx stop
sudo python /home/box/web/ask/manage.py runserver 0.0.0.0:80
