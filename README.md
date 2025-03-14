# Assignment8-IST105-0313

```bash
sudo dnf update -y
sudo dnf install -y httpd
sudo dnf install python3 -y
sudo dnf install -y php
sudo dnf -y install git
cd /var/www/html
sudo git clone https://github.com/itouoti12/Assignment8-IST105-0313.git .
sudo chmod +x /var/www/html/network_config.py
sudo systemctl start httpd

```

# need ad authorization for apache user  
```bash
sudo chown apache:apache lease_database.json
sudo chmod 664 lease_database.json
```
