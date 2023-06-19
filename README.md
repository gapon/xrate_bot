# Telegram Bot for tracking of USD and BTC exchange rates

## Usage:
/set {bottom price} {upper price} – set alarm for USD reaching bottom or upper price

/unset – unset alarm


Хорошие примеры: https://pythonprogramming.org/making-a-telegram-bot-using-python/


## Automating the bot with Systemd
1. Create a Systemd Service File
sudo nano /lib/systemd/system/xrate_bot.service