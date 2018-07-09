echo -e "stop nginx....\n\n"
sudo /usr/local/nginx/sbin/nginx -s stop
echo -e "stop uwsgi...\n\n"
sudo pkill -f uwsgi -9

echo -e "start uwsgi....\n\n"
/home/pro/python3_venv/bin/uwsgi --ini light_salt_uwsgi.ini &
echo -e "start nginx...\n\n."
sudo /usr/local/nginx/sbin/nginx
