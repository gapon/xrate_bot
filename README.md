## Usage:
/set {figi name} {bottom price} {upper price} – set alarm for USD, CNY or TMOS reaching bottom or upper price

/unset – unset all alarm


Хорошие примеры: https://pythonprogramming.org/making-a-telegram-bot-using-python/


1. Установить зависимости:
```bash
pip install -r requirements.txt
```

2. Добавить переменные окружения в ~/.profile:
```bash
export BOT_ENV=prod
export TG_XRATE_TOKEN=
export TI_SANDBOX_TOKEN=
```

Обновить переменные окружения:
```bash
source ~/.profile
```


## Получить SSL сертификат для домена через Let's Encrypt

Установить
```bash
sudo apt install python3-certbot-nginx
```

Запустить
```bash
sudo certbot --nginx -d your_domain -d www.your_domain
```