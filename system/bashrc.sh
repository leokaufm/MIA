# This code can be added to .bashrc

echo Welcome to bot
if ! pgrep python; then
    echo 'Starting bot'
    cd /srv/www/
    cd ALPI-bot
    killall -q pytjon 
    rm -f running.wt
    python Brainstem.py >> brainstem.log &
else
    echo 'Bot is already running.'
fi
