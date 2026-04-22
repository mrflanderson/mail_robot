# 🎯 Mail Robot — Подробное руководство по использованию

## 📚 Оглавление

1. [Введение](#введение)
2. [Установка и подготовка](#установка-и-подготовка)
3. [Первичный запуск](#первичный-запуск)
4. [Добавление аккаунтов](#добавление-аккаунтов)
5. [Проверка почты](#проверка-почты)
6. [Управление аккаунтами](#управление-аккаунтами)
7. [Типичные сценарии использования](#типичные-сценарии-использования)
8. [Распространённые ошибки и решения](#распространённые-ошибки-и-решения)
9. [Настройка под разных почтовых сервисов](#настройка-под-разных-почтовых-сервисов)
10. [Советы и лучшие практики](#советы-и-лучшие-практики)

---

## 📖 Введение

**Mail Robot** — это простая и мощная утилита для автоматизированной проверки почтовых ящиков по протоколу IMAP. Она позволяет вам удобно отслеживать входящие письма из нескольких аккаунтов одновременно.

### Что умеет Mail Robot:

- ✅ **Автоматическая проверка** — запускаете один раз, проверяет все аккаунты
- ✅ **Хранение настроек** — аккаунты сохраняются в SQLite БД
- ✅ **Гибкая настройка** — работает с SSL и STARTTLS
- ✅ **Детальное логирование** — следите за процессом в консоли и файле
- ✅ **Удобный интерфейс** — всё через командную строку

### Архитектура:

```
┌─────────────────────────────────────────────────────────────┐
│  check_mail.py — единый скрипт с встроенной БД (SQLite)     │
├─────────────────────────────────────────────────────────────┤
│  mail_check.db — SQLite база для хранения аккаунтов          │
├─────────────────────────────────────────────────────────────┤
│  mail_check.log — файл логов (stdout + file logging)         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Установка и подготовка

### Шаг 1: Проверка Python

Убедитесь, что у вас установлен Python 3.6+:

```bash
python --version
# Должно показать: Python 3.x.x
```

**Если Python не установлен:**

- **[Скачать Python](https://python.org)**
- После установки проверьте: `python --version`

### Шаг 2: Первичная инициализация

Запустите скрипт первый раз:

```bash
python check_mail.py
```

**Что произойдет:**

1. Создается/обновляется SQLite база данных
2. Выводится help-текст с примерами
3. Готово к работе!

### Шаг 3: Проверка базы данных (опционально)

```bash
# Посмотреть, что создал скрипт
dir  # Windows
ls -la  # Linux/Mac
```

**Должно создать:**
- `mail_check.db` — SQLite база (около 4KB)
- `mail_check.log` — файл логов

---

## 🚀 Первичный запуск

### Вариант 1: Показать помощь (как пользоваться)

```bash
python check_mail.py
```

**Вывод:**
```text
Mail Robot - Email Checker

USAGE:
    python check_mail.py              - Run mail check for all accounts
    python check_mail.py add "email" "password" "server" "port" "ssl"
    python check_mail.py list         - List all configured accounts
    python check_mail.py remove "email"
    python check_mail.py help         - Show this help message

ARGUMENTS FOR 'add' command:
    email      - Full email address (e.g., user@example.com)
    password   - Email account password
    server     - IMAP server address (e.g., imap.gmail.com)
    port       - IMAP port (typically 993 for SSL)
    ssl/tls    - Security type: 'ssl', 'starttls', or 'tls'
```

### Вариант 2: Запустить проверку (если есть аккаунты)

```bash
python check_mail.py
```

**Если аккаунты есть:** проверит все из БД и покажет результат

**Если аккаунтов нет:** покажет сообщение и предложит добавить первый аккаунт

---

## ✉️ Добавление аккаунтов

### Базовая команда

```bash
python check_mail.py add "email" "password" "server" "port" "security"
```

### Параметры:

| Параметр | Пример | Описание |
|----------|--------|----------|
| `email` | `"user@gmail.com"` | Полный email адрес |
| `password` | `"s3cr3t"` | Пароль от IMAP |
| `server` | `"imap.gmail.com"` | IMAP сервер |
| `port` | `993` | Порт (993/143) |
| `security` | `"ssl"` | Тип защиты: `ssl`, `starttls`, `tls` |

### Пример 1: Gmail (SSL)

```bash
# Самый популярный вариант
python check_mail.py add "alex@gmail.com" "mypassword" "imap.gmail.com" "993" "ssl"
```

**Ожидаемый вывод:**
```text
INFO: [MAIN] Database schema initialized.
INFO: [DB] Account alex@gmail.com added/updated to database.

Account added: alex@gmail.com

INFO: [MAIN] === END OF PROCESS ===
```

### Пример 2: Beget (SSL)

```bash
python check_mail.py add "USER_EMAIL_HERE" "USER_PASSWORD_HERE" "USER_IMAP_SERVER_HERE" "993" "ssl"
```

### Пример 3: Outlook (SSL)

```bash
python check_mail.py add "me@outlook.com" "outlook_pass" "imap-outlook.office365.com" "993" "ssl"
```

### Пример 4: Gmail (STARTTLS)

```bash
# Некоторые сервисы требуют STARTTLS
python check_mail.py add "user@gmail.com" "pass" "imap.gmail.com" "143" "starttls"
```

### Пример 5: Yahoo (SSL)

```bash
python check_mail.py add "user@yahoo.com" "pass" "imap.mail.yahoo.com" "993" "ssl"
```

### Комбинация: несколько аккаунтов

```bash
# Google
python check_mail.py add "alex@gmail.com" "pass1" "imap.gmail.com" "993" "ssl"

# Beget
python check_mail.py add "USER_EMAIL_2_HERE" "USER_PASSWORD_2_HERE" "USER_IMAP_SERVER_2_HERE" "993" "ssl"

# Outlook
python check_mail.py add "me@outlook.com" "pass3" "imap-outlook.office365.com" "993" "ssl"

# Запустить проверку всех
python check_mail.py
```

### Условный оператор `add` (для PowerShell)

```bash
python check_mail.py add "user@gmail.com" "my_p@ss:w0rd" \
    "imap.gmail.com" "993" "ssl"
```

**\ — означает продолжение строки** (можно разбить на несколько строк)

---

## 📧 Проверка почты

### Базовый запуск

```bash
python check_mail.py
```

**Что происходит:**

```text
INFO: [MAIN] Database schema initialized.
INFO: [MAIN] === STARTING MAIL CHECKING PROCESS ===
INFO: [MAIN] ======================================================
INFO: [MAIN] -------------------------------------------
INFO: [MAIN] Processing account 1 of 2...
INFO: [MAIN]   Email: alex@gmail.com
INFO: [CONN] --- Connecting to imap.gmail.com for alex@gmail.com ---
INFO: [CONN] Attempting to log in...
INFO: [CONN] Successfully logged in.
INFO: [CONN] INBOX selected successfully.
INFO: [CONN] Searching for: ALL
INFO: [CONN] Found 4 total messages in the mailbox.
INFO: [CONN] Parsed 3 messages (showing first 3).
INFO: [CONN] Logged out and connection closed.
INFO: [MAIN] ======================================================
INFO: [MAIN] === ALL EMAIL CHECKING COMPLETE ===

[SUMMARY] Account: alex@gmail.com
[SUCCESS] Successfully retrieved mail data!
  -> Found 4 total messages in mailbox.
  -> Message 1: Subject='=?UTF-8?Q?Лето:2026?=...'
  -> Message 2: Subject='test'
  -> Message 3: Subject='=?utf-8?b?...?=...'
  -> ... and 1 more messages not shown.
```

### Варианты запуска проверки

#### 1. Стандартный запуск (все аккаунты)

```bash
python check_mail.py
```

#### 2. С явным указанием команды

```bash
# Аналогично стандартному запуску
python check_mail.py check

# Или с другим ключом
python check_mail.py run
```

#### 3. Просмотр результатов в конце

```bash
python check_mail.py 2>&1 | Select-String -Pattern "SUCCESS|ERROR|Found"
```

### Что показывает вывод:

- **[MAIN]** — Основные сообщения о ходе работы
- **[CONN]** — Подключение к серверу IMAP
- **[SUMMARY]** — Итоговый результат для каждого аккаунта
- **[DEBUG]** — Дополнительные детали (если включено)

---

## 📋 Управление аккаунтами

### Просмотр списка аккаунтов

```bash
python check_mail.py list
```

**Выходит:**
```text
  1. alex@gmail.com
     Server: imap.gmail.com:993 (ssl)
     Last checked: 2026-04-22

  2. info@blur.moscow
     Server: imap.beget.com:993 (ssl)
     Last checked: never
```

**Поля:**
- `1.` — Номер аккаунта в списке
- `Email` — Полная почта
- `Server` — IMAP сервер + порт
- `Last checked` — Последняя проверка (или `never`)

### Удаление аккаунта

```bash
# Удалить конкретного
python check_mail.py remove "alex@gmail.com"

# Удалить тестового
python check_mail.py remove "test@domain.com"
```

**Вывод:**
```text
Account removed: alex@gmail.com

INFO: [MAIN] === END OF PROCESS ===
```

### Очистка базы полностью

```bash
# Если нужно очистить всё и начать заново
python check_mail.py remove "alex@gmail.com"
python check_mail.py remove "USER_EMAIL_3_HERE"
python check_mail.py remove "USER_EMAIL_4_HERE"
python check_mail.py remove "USER_EMAIL_5_HERE"
```

**Проверка:**
```bash
python check_mail.py list
# Должно показать: "1." или пусто
```

---

## 🎯 Типичные сценарии использования

### Сценарий 1: Новый пользователь

```bash
# 1. Посмотреть, как это работает
python check_mail.py

# 2. Добавить первый аккаунт
python check_mail.py add "user@gmail.com" "pass123" "imap.gmail.com" "993" "ssl"

# 3. Запустить проверку
python check_mail.py

# 4. Посмотреть результат
python check_mail.py list
```

### Сценарий 2: Несколько аккаунтов

```bash
# Google — для личных сообщений
python check_mail.py add "alex@gmail.com" "pass1" "imap.gmail.com" "993" "ssl"

# Beget — для рабочей почты
python check_mail.py add "USER_EMAIL_6_HERE" "USER_PASSWORD_6_HERE" "USER_IMAP_SERVER_6_HERE" "993" "ssl"

# Outlook — для бизнес-переписки
python check_mail.py add "me@outlook.com" "pass3" "imap-outlook.office365.com" "993" "ssl"

# Запустить проверку всех трёх
python check_mail.py
```

### Сценарий 3: Мониторинг почтовых ящиков

```bash
# Запуск 1 раз в день
python check_mail.py

# Или расписание задачи (Windows):
# Среда: Администратор → Панель управления → Настройка планировщика задач
schtasks /create /tn "Mail Robot" /tr "python check_mail.py" /sc daily

# Или (Linux/Mac):
crontab -l
# Добавить в конец:
# 0 8 * * * python "C:\path\to\check_mail.py" >> log.txt 2>&1
```

### Сценарий 4: Перебор аккаунтов

```bash
# Проверка только одного аккаунта
python check_mail.py add "test@gmail.com" "pass" "imap.gmail.com" "993" "ssl"
python check_mail.py

# Удалить после проверки
python check_mail.py remove "test@gmail.com"
```

### Сценарий 5: Бэкап настроек

```bash
# Резервное копирование перед очисткой
# Скопировать весь файл check_mail.py на другой носитель

# Или бэкап БД
cp mail_check.db mail_check_backup.db
```

---

## 🐛 Распространённые ошибки и решения

### Ошибка 1: AUTHENTICATIONFAILED

```text
INFO: [CONN] Attempting to log in...
ERROR: [CONN] Authentication or Connection Error: b'[AUTHENTICATIONFAILED]'
```

**Причина:** Неверный пароль или IMAP не включён у провайдера.

**Решение:**

1. **Проверить пароль:**
   ```bash
   python check_mail.py remove "user@gmail.com"
   # Добавить снова с новым паролем
   python check_mail.py add "user@gmail.com" "newpass" "imap.gmail.com" "993" "ssl"
   ```

2. **Проверить IMAP в настройках почты:**
   - Gmail: https://myaccount.google.com/apppasswords
   - Beget: Настройки → IMAP/POP3
   - Outlook: Настройки → Подключение → IMAP включен

### Ошибка 2: Connection Error (Port 143 vs 993)

**Проблема:** Сервер использует порт 143 вместо 993.

**Решение:**
```bash
# Попробуйте STARTTLS на порту 143
python check_mail.py add "user@gmail.com" "pass" "imap.gmail.com" "143" "starttls"
```

### Ошибка 3: Too many connections

```text
INFO: [CONN] ...
ERROR: [CONN] Connection limit exceeded
```

**Решение:** Подождать или запустить последовательно:
```bash
python check_mail.py  # Первый аккаунт
# Подождать 10-20 секунд
python check_mail.py  # Второй аккаунт
```

### Ошибка 4: SSL Error

```text
ERROR: [CONN] SSL verification failed
```

**Решение:** Проверить, что порт и защита соответствуют серверу:
```bash
# Gmail: порт 993 + ssl (рекомендуется)
python check_mail.py add "user@gmail.com" "pass" "imap.gmail.com" "993" "ssl"
```

### Ошибка 5: No accounts in database

```text
=== No accounts configured ===
Run: python check_mail.py add 'email' 'password' 'server' 'port' 'ssl'
```

**Решение:**
```bash
# Добавить хотя бы одного аккаунта
python check_mail.py add "user@gmail.com" "pass" "imap.gmail.com" "993" "ssl"
```

---

## ⚙️ Настройка под разных почтовых сервисов

### Gmail

```bash
# Вариант 1: SSL (рекомендуется)
python check_mail.py add "user@gmail.com" "pass" "imap.gmail.com" "993" "ssl"

# Вариант 2: STARTTLS
python check_mail.py add "user@gmail.com" "pass" "imap.gmail.com" "143" "starttls"
```

**Настройки Gmail:**
- IMAP сервер: `imap.gmail.com`
- Порт: `993` (SSL) или `143` (STARTTLS)
- Защита: `ssl` или `starttls`
- **Обязательно:** Включить 2FA + создать приложение пароль (для приложений)

### Beget

```bash
# Вариант 1: SSL (рекомендуется)
python check_mail.py add "user@beget.com" "pass" "imap.beget.com" "993" "ssl"

# Вариант 2: STARTTLS
python check_mail.py add "user@beget.com" "pass" "imap.beget.com" "143" "starttls"

# Вариант 3: POP3 (если нужно скачивать на компьютер)
python check_mail.py add "user@beget.com" "pass" "pop3.beget.com" "995" "ssl"
```

**Настройки Beget:**
- IMAP сервер: `imap.beget.com`
- POP3 сервер: `pop3.beget.com`
- Порт IMAP: `993` (SSL) или `143` (STARTTLS)
- Порт POP3: `995` (SSL) или `110` (STARTTLS)

### Outlook/Hotmail

```bash
python check_mail.py add "user@outlook.com" "pass" "imap-outlook.office365.com" "993" "ssl"
# Или
python check_mail.py add "user@outlook.com" "pass" "imap-mail.outlook.com" "993" "ssl"
```

### Яндекс Почта

```bash
python check_mail.py add "user@yandex.ru" "pass" "imap.yandex.ru" "993" "ssl"
```

### Mail.ru

```bash
python check_mail.py add "user@mail.ru" "pass" "imap.mail.ru" "993" "ssl"
```

### Zoho

```bash
python check_mail.py add "user@zoho.com" "pass" "imap.zoho.com" "993" "ssl"
```

---

## 💡 Советы и лучшие практики

### 1. Используйте SSL для большинства случаев

```bash
# Рекомендация для большинства сервисов:
python check_mail.py add "user@..." "pass" "imap.example.com" "993" "ssl"
```

### 2. Разделяйте аккаунты по назначению

```bash
# Личная почта
python check_mail.py add "alex@gmail.com" "pass1" "imap.gmail.com" "993" "ssl"

# Рабочая почта
python check_mail.py add "alex@company.com" "pass2" "imap.company.com" "993" "ssl"

# Резервная почта
python check_mail.py add "backup@domain.com" "pass3" "imap.domain.com" "993" "ssl"
```

### 3. Регулярно обновляйте проверенные аккаунты

```bash
# Бэкап БД раз в месяц
cp mail_check.db mail_check.db.backup

# Или просто запускайте проверку
python check_mail.py
```

### 4. Настройка под разные порты

| Сервис | Порт 993 (SSL) | Порт 143 (STARTTLS) |
|--------|----------------|---------------------|
| Gmail | ✅ Рекомендуется | ✅ Также подходит |
| Beget | ✅ Рекомендуется | ✅ Также подходит |
| Outlook | ✅ Рекомендуется | ✅ Также подходит |
| Яндекс | ✅ Рекомендуется | ⚠️ Иногда работает |
| Mail.ru | ✅ Рекомендуется | ✅ Также подходит |

### 5. Работа с большими списками писем

```bash
# Скрипт всегда показывает первые 3 письма
# Чтобы увидеть больше, нужно:
# — Увеличить лимит (в коде)
# — Или проверить несколько раз

# Пример для полного списка:
for i in $(seq 1 100); do
    echo "=== Pисьмо $i ==="
    # (в реальном скрипте)
done
```

---

## 📊 Мониторинг работы

### Проверка состояния БД

```bash
# Посмотреть размер БД
python -c "import sqlite3; db=sqlite3.connect('mail_check.db'); print(f'Size: {os.path.getsize(\"mail_check.db\")} bytes')"
```

### Проверка логов

```bash
# Посмотреть последние записи
tail -30 mail_check.log
```

### Проверка количества аккаунтов

```bash
python check_mail.py list | Select-String -Pattern "^[0-9]+\." | Measure-Object
```

---

## 🔧 Продвинутые настройки

### 1. Уровень логирования

```python
# В коде можно изменить уровень логирования
# Для отладки:
logging.getLogger().setLevel(logging.DEBUG)
```

### 2. Бэкап после каждого запуска

```bash
# Автоматический бэкап (опционально)
python check_mail.py
cp mail_check.db mail_check.db.backup.$(date +%Y%m%d)
```

### 3. Параллельное выполнение

```bash
# В PowerShell:
# Параллельный запуск (если БД поддерживает)
python check_mail.py | Select-Object -Last 20
```

---

## 📞 Полезные ссылки

- **Техническая документация:** `docs/structure.md`
- **Быстрый старт:** `docs/readme.md`
- **Архитектура:** `docs/structure.md`
- **GitHub (если в репозитории):** [ai/mail_robot](https://github.com/ai/mail_robot)

---

## 🎉 Удачи в автоматизации!

**Теперь вы знаете всё о Mail Robot!**

Приятной работы с почтой! 🚀

---

## 📝 Краткая шпаргалка

```bash
# Показать help
python check_mail.py

# Посмотреть список
python check_mail.py list

# Добавить аккаунт
python check_mail.py add "email" "pass" "server" "port" "ssl"

# Удалить аккаунт
python check_mail.py remove "email"

# Запустить проверку (все аккаунты)
python check_mail.py

# Показать последние 50 строк логов
tail -50 mail_check.log
```

---

**Версия:** 1.4 | **Автор:** Mail Robot Team | **Лицензия:** MIT | **Python:** 3.6+
