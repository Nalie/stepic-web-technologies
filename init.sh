sudo mkdir /home/box/web/public
sudo mkdir /home/box/web/public/img
sudo mkdir /home/box/web/public/css
sudo mkdir /home/box/web/uploads

sudo ln -s /home/box/web/etc/nginx.conf  /etc/nginx/sites-enabled/test.conf
sudo /etc/init.d/nginx restart