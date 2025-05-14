# CarWash-qt-design

O'rnatish tartibi:

```sh
sudo apt-get install python3-pyqt5 python3-aiohttp apache2
cd ~
git clone https://github.com/muhiddinov/qt-design.git
sudo cp -r ~/qt-designer/carwash/carwash.service /etc/systemd/system/
sudo cp -r ~/qt-designer/carwash/html/* /var/www/html/
sudo service apache2 restart
sudo systemctl daemon-reload
sudo systemctl enable carwash.service
sudo service carwash restart
```

