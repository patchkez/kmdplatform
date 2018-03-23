# recharge.py install

As root:
```
apt install python3
pip3 install requests
cd /opt
git clone https://github.com/Emmanux/kmdplatform.git
cd kmdplatform/iguana/tools
cp recharge.ini.example recharge.ini
cp cron.recharge.iguana /etc/cron.d/rechargeiguana
service cron reload
vim recharge.ini
```
Change your rpcuser and rpcpassword and save the file.

You can configure default parameters for all coins ("DEFAULT" label) or individually, under each coin label.

You can test it now:
```
./recharge.py
```

The installed cron.d file will take care of running the script every 10 minutes.
