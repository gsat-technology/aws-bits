#just a backup of deployment script to deploy a Supervisor/Python based Activity Worker for SFN

###
## Install the 'Animate' SFN activity task on Ec2 instance
###

###Sync time
#this command is INTERACTIVE (choose Australia/Hobart)
sudo dpkg-reconfigure  tzdata

#add this to sudo crontab (cleans up /tmp which otherwise collects imagemagick temporary files)
*/5 * * * * find /tmp -maxdepth 1 -mmin +5 -type f -delete

### Enable swap ###
(for very small instance e.g. 512MB RAM)
sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
sudo cp /etc/fstab /etc/fstab.bak
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab


### Virtualenv ###

sudo apt-get update
sudo apt-get install -y python-pip python-dev build-essential
pip install virtualenv virtualenvwrapper
pip install --upgrade pip
printf '\n%s\n%s\n%s' '# virtualenv' 'export WORKON_HOME=~/virtualenvs' \
'source /usr/local/bin/virtualenvwrapper.sh' >> /home/ubuntu/.bashrc
mkdir -p /home/ubuntu/virtualenvs
mkvirtualenv sfn_activity


### Deploy python activity task script ###

mkdir worker

#copy from source animate.py to ~/worker

#install pip requirements
#instal imagemagick
sudo apt-get install libmagickwand-dev

#Configure logging location
sudo mkdir /var/log/animate
sudo chown -R ubuntu:ubuntu /var/log/animate


### Supervisor ###

sudo apt-get install -y supervisor

cat >/tmp/animate.conf <<EOF
[program:animate]
command=/home/ubuntu/virtualenvs/sfn_activity/bin/python animate.py
environment=PATH="/home/ubuntu/virtualenvs/sfn_activity/bin:%(ENV_PATH)s"
directory=/home/ubuntu/worker
autostart=true
autorestart=true
startretries=3
stderr_logfile=/var/log/animate/err.log
stdout_logfile=/var/log/animate/out.log
user=ubuntu
process_name=%(program_name)s_%(process_num)02d
numprocs=1
EOF

sudo cp /tmp/animate.conf /etc/supervisor/conf.d/animate.conf

sudo supervisorctl reload
