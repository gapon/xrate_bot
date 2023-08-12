## Usage:
/set {figi name} {bottom price} {upper price} – set alarm for USD, CNY or TMOS reaching bottom or upper price

/unset – unset all alarm

/chart {ticker} {period} – draws a ticker chart for the period


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

## Отрисовка графиков в Matplotlib

Чтобы отрисовывать графики на бэкэнде нужно указать, чтобы Matplotlib использовал соответствующий бэк:
```python
import matplotlib
matplotlib.use('Agg')
```

Для MacOs нужно установть PyQt5
```bash
pip install PyQt5
```

На Ubunte нужный бэкэнд уже установлен. В случае ошибки его нужно установить:
```bash
sudo apt install python3-tk
```



## TODO
- [ ] Засервить приложение через Gunicorn + systemd. [Пример](https://github.com/gwvsol/flask-telegram-bot/blob/master/gunicorn.conf).
- [ ] Переделать отображение кнопок/диалога.
    - Сейчас первое сообщение может подменять кнопки в прошлом.
    - Диалог "Choose a currency" выглядит ненативно.
- [x] Сделать отображение котировок всех тикеров по одной кнопке/команде.
- [ ] Добавить сравнение котировок h2h, d2d, w2w
- [x] Добавить отрисовку графиков
- [x] Сделать поиск figi по ticker-у
- [x] Улучшить графики, добавить MA50, MA200
- [x] Добавить базу данных и сохранить туда справочник figi-ticker
- [ ] Сделать функцию вывода цены по тикеру
- [ ] Добавить меню
- [ ] Падумать, как отслеживать интересные компании
- [x] Реализовать авторизацию