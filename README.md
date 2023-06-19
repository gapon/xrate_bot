# Telegram Bot for tracking of USD and BTC exchange rates

## Usage:
/set {bottom price} {upper price} – set alarm for USD reaching bottom or upper price

/unset – unset alarm


Хорошие примеры: https://pythonprogramming.org/making-a-telegram-bot-using-python/


1. Установить зависимости:
```bash
pip install -r requirements.txt
```

2. Добавить переменные окружения в ~/.profile:
```bash
export BOT_ENV=prod
export TG_XRATE_TOKEN=
```

Обновить переменные окружения:
```bash
source ~/.profile
```

3. Создаем Systemd Service файл xrate_bot.service

4. Создать symlinc для xrate_bot.service:
```bash
sudo ln -s /home/ubuntu/xrate_bot/xrate_bot.service /lib/systemd/system/xrate_bot.service
```

5. Enable and Start Service

Reload the Systemd daemon to pick up the new service file:
```bash
sudo systemctl daemon-reload
```

Enable the service to run at startup
```bash
sudo systemctl enable xrate_bot.service
```

Manually start the service
```bash
sudo systemctl start xrate_bot.service
```