# Устранение проблемы SSL/TLS подключения (WinError 121)

## Проблема
При запуске бота возникает ошибка `WinError 121` при подключении к `api.telegram.org:443`. Это типичная проблема для Windows, вызванная вмешательством антивируса или фаервола в SSL/TLS соединения.

## Причины ошибки WinError 121
Ошибка "Сертификат захвачен" обычно возникает по следующим причинам:

### 1. Антивирус с функцией SSL-сканирования
- **Kaspersky** - Anti-virus Scan
- **ESET NOD32** - HTTPS scanning
- **Dr.Web** - HTTPS encryption check
- **Avast/AVG** - Web Shield
- **Bitdefender** - Advanced Threat Control

### 2. Корпоративный прокси/фаервол
- MITM (Man-in-the-Middle) сканирование трафика
- Замена сертификатов на корпоративные самоподписанные

### 3. Прокси-настройки Windows
- Системные прокси могут мешать асинхронным запросам

## Решения

### Решение 1: Отключение SSL-сканирования в антивирусе ⭐ РЕКОМЕНДУЕМО

#### Kaspersky:
1. Откройте Kaspersky
2. Нажмите на значок шестеренки (Настройки)
3. Выберите "Дополнительно" → "Сканеры"
4. Найдите "**Антивирусный сканер**"
5. Отключите опцию "**Сканировать защищенные соединения**" или "**Scan encrypted connections**"
6. Перезапустите бота

#### ESET NOD32:
1. Откройте ESET (F5 для перехода в режим продвинутых настроек)
2. Перейдите в "Настройки продукта" → "Детализация настроек"
3. В фильтре найдите "**HTTPS**"
4. Найдите "**Сканировать зашифрованные файлы и HTTPS**"
5. Отключите эту опцию
6. Перезапустите бота

#### Dr.Web:
1. Откройте Dr.Web
2. Настройки → Настройки антивируса
3. Отключите "**Проверять HTTPS-соединения**"
4. Перезапустите бота

#### Avast/AVG:
1. Откройте меню Avast/AVG
2. Меню → Настройки
3. Раздел "Общие" → "Вспомогательные средства"
4. Отключите "**Использовать аппаратное ускорение**" и "**Защищать браузеры**"
5. Или временно отключите "**Веб-щит**"

#### Bitdefender:
1. Откройте Bitdefender
2. Перейдите в "Настройки защиты"
3. Найдите "**Anti-phishing**" или "Web Protection"
4. Отключите "**SSL Scan**" или "**HTTPS Scanning**"

### Решение 2: Добавить исключение в фаервол Windows

```powershell
# Запустить PowerShell от имени администратора

# Добавить правила для Telegram API
New-NetFirewallRule -DisplayName "Telegram API Allow" -Direction Outbound -LocalPort 443 -Protocol TCP -Action Allow

# Также разрешить api.telegram.org явно
Add-WindowsResourcePack -Name "Microsoft.EdgeUpdate.Fallback"
```

### Решение 3: Использовать простой HTTP вместо HTTPS (для тестирования)

Для локального тестирования можно использовать HTTP:

```python
from aiogram import Bot

# Используйте http вместо https для отладки
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, base_url='http://api.telegram.org')
```

### Решение 4: Настройка через переменные окружения

Добавьте эти переменные перед запуском:

```bash
# В Windows (PowerShell)
$env:PYTHONHTTPSVERIFY="False"
$env:REQUESTS_CA_BUNDLE=""

# Запуск бота
python bots/main.py
```

### Решение 5: Использование VPN или альтернативного DNS

Если проблема на уровне сети:

```python
# Добавьте это в начало main.py перед импортами
import socket
socket.setdefaulttimeout(10)

# Или используйте Cloudflare DNS
os.environ['DNS_SERVER'] = '1.1.1.1'
```

## Проверка решения

После применения любого из решений запустите тестовый скрипт:

```bash
cd tg-avito-bot
python test_connection.py
```

Вы должны увидеть сообщение:
```
Testing connection to api.telegram.org...
✓ Successfully connected! Bot ID: XXXXXXXXX
```

## Альтернативные методы запуска

### Метод A: Через Python с принудительным флагом Unicode
```bash
python -u bots/main.py
```

### Метод B: Через Docker (если есть Docker Desktop)
```bash
docker-compose up
```

Docker изолирует сеть и может обойти некоторые проблемы Windows.

### Метод C: Через WSL (Windows Subsystem for Linux)
```bash
wsl
cd /mnt/c/Users/Egorka/Documents/Qoder/2026-09-24/c4b46c5a/tg-avito-bot
python3 bots/main.py
```

WSL использует Linux-сетевой стек, который не подвержен проблемам Windows SSL.

## Для разработчиков: Обходной код в коде

Если никакие другие решения не помогают, можно добавить обработку ошибок SSL в самом коде:

```python
# В main.py добавьте в начале файла:
import ssl
import certifi

ssl_context = ssl.create_default_context(cafile=certifi.where())
```

Также можно временно отключить проверку сертификатов (НЕ ДЛЯ ПРОДАКШНА!):

```python
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

**ВНИМАНИЕ!** Это небезопасно для продакшена, только для локального тестирования.

## Мониторинг логов

Следите за логами для диагностики:

```bash
# Включите детальный логгинг
export PYTHONLOGLEVEL=DEBUG
python bots/main.py 2>&1 | tee bot.log
```

Затем проверьте `bot.log` на наличие сообщений об SSL.

## Контактная информация

Если ничего не помогает:
- Проверьте, работает ли Telegram в браузере через этот же прокси
- Попробуйте другую сеть (телефон как热点)
- Обратитесь к системному администратору (если это корпоративный компьютер)

## Деплой на Render

Проблема WinError 121 актуальна ТОЛЬКО для локальной разработки на Windows. При деплое на Render сервер работает под управлением Linux и не имеет этой проблемы.

---

**Версия документа:** 1.0  
**Дата обновления:** 2026-09-25  
**Актуально для:** Python 3.12+, Windows 10/11
