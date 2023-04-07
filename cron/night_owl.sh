#! /bin/bash
cd /var/www/coin_village
source venv_cv/bin/activate


for i in {1..12}; do

    python /var/www/coin_village/cron/night_owl.py &

    sleep 5;
done
