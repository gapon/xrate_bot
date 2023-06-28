## Usage:
/set {figi name} {bottom price} {upper price} – set alarm for USD, CNY or TMOS reaching bottom or upper price

/unset – unset all alarm


Хорошие примеры: https://pythonprogramming.org/making-a-telegram-bot-using-python/

TG + Nging + SSL: https://medium.com/jj-innovative-results/how-to-create-a-simple-telegram-bot-in-python-using-nginx-and-gcp-926f1b0fb16f


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


TODO
- [ ] Засервить приложение через Gunicorn + systemd. [Пример](https://github.com/gwvsol/flask-telegram-bot/blob/master/gunicorn.conf).
- [ ] Переделать отображение кнопок/диалога.
    - Сейчас первое сообщение может подменять кнопки в прошлом.
    - Диалог "Choose a currency" выглядит ненативно.
- [x] Сделать отображение котировок всех тикеров по одной кнопке/команде.
- [ ] Добавить сравнение котировок h2h, d2d, w2w