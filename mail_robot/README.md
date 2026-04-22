# 📧 Mail Robot — Автоматизированный Проверщик Почты

**Mail Robot** — это мощная утилита для автоматизированной проверки IMAP-аккаунтов на наличие новых сообщений. Поддерживает SSL/TLS, хранит аккаунты в SQLite БД и имеет удобный CLI интерфейс.

![Python](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![SQLite](https://img.shields.io/badge/databases-SQLite-brightgreen.svg)
![IMAP](https://img.shields.io/badge/protocol-IMAP-brightgreen.svg)

---

## ⚡ Быстрый запуск

```bash
# 1. Первичный запуск (показать help)
python check_mail.py

# 2. Добавить аккаунт
python check_mail.py add "email@gmail.com" "pass123" "imap.gmail.com" "993" "ssl"

# 3. Запустить проверку (для всех аккаунтов)
python check_mail.py -get

# 4. Получить непрочитанные письма как JSON
python check_mail.py -check

# 5. Список аккаунтов
python check_mail.py list
```

**Вывод:**
```text
INFO: [MAIN] === STARTING MAIL CHECKING PROCESS ===
INFO: [CONN] Successfully logged in.
INFO: [CONN] Found 2 new messages in the mailbox.
[DB] INSERTed new email: UID=123, Subject='=?UTF-8?Q?TEST_SUBJECT=...'
[SUMMARY] Account: email@gmail.com
  -> Found 2 total messages in mailbox.
  -> Message 1: Subject='TEST_SUBJECT...'
  -> Message 2: Subject='Other Subject'
INFO: [MAIN] === ALL EMAIL CHECKING COMPLETE ===
```

---

## 🎯 Возможности

- ✅ **Инкрементальная загрузка:** Обновляется только новые письма (UID > last_uid), экономит трафик
- ✅ **Декодирование заголовков:** Поддержка RFC 2047 (Q/ BASE64 encoding)
- ✅ **Хранение в SQLite:** Аккаунты и письма сохраняются в `mail_check.db`
- ✅ **Логирование:** Вывод в консоль и файл `mail_check.log`
- ✅ **CLI интерфейс:** 6 команд для управления
- ✅ **JSON вывод:** Для программной обработки (`-check`, `-read`)

---

## 📋 Команды

| Команда | Описание | Пример |
|---------|----------|--------|
| `-get` | Синхронизация + обновление БД | `python check_mail.py -get` |
| `-check` | Получить непрочитанные письма (JSON) | `python check_mail.py -check` |
| `-read [id]` | Получить полное письмо по ID (JSON) | `python check_mail.py -read 1` |
| `-mark-read [id]` | Помечает письмо как прочитанное | `python check_mail.py -mark-read 1` |
| `list` | Список настроенных аккаунтов | `python check_mail.py list` |
| `remove "email"` | Удалить аккаунт | `python check_mail.py remove "email"` |

**Default (без флагов):** Синхронизация всех аккаунтов (`run_full_check()`)

---

## 🏗️ Архитектура

```
mail_robot/
├── check_mail.py              # Главный скрипт
├── mail_check.db              # SQLite база данных
├── mail_check.log             # Файл логов
└── README.md                  # Документация
```

### База данных (SQLite)

**Таблица `accounts`:**
```sql
CREATE TABLE accounts (
    email TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    imap_server TEXT NOT NULL,
    imap_port INTEGER NOT NULL,
    imap_security TEXT NOT NULL,
    last_checked_date TEXT
);
```

**Таблица `emails`:**
```sql
CREATE TABLE emails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_email TEXT NOT NULL,
    uid INTEGER NOT NULL,
    subject TEXT,
    sender TEXT,
    body TEXT,
    received_date TEXT,
    is_read BOOLEAN DEFAULT 0,
    has_attachment BOOLEAN DEFAULT 0,
    UNIQUE(account_email, uid),
    FOREIGN KEY (account_email) REFERENCES accounts(email)
);
```

---

## 🔄 Принцип работы

1. **Запуск:** Инициализация БД и чтение аргументов
2. **Синхронизация:** Подключение к IMAP серверам по очереди
3. **Поиск новых:** `UID {last_uid + 1}:*` — только новые письма
4. **Парсинг:** Извлечение заголовков (subject, sender, date)
5. **Декодирование:** UTF-8 + Q/ BASE64 (RFC 2047)
6. **Хранение:** `INSERT OR IGNORE` в БД
7. **Логирование:** Вывод в консоль и файл
8. **Завершение:** Обновление `last_checked_date`

---

## 🌐 Поддерживаемые IMAP-серверы

| Сервис | Порт (SSL) | Порт (STARTTLS) | Пример |
|--------|------------|-----------------|--------|
| Gmail | ✅ 993 | ✅ 143 | `imap.gmail.com` |
| Beget | ✅ 993 | ✅ 143 | `imap.beget.com` |
| Outlook/Hotmail | ✅ 993 | ✅ 143 | `imap-outlook.office365.com` |
| Яндекс Почта | ✅ 993 | ✅ 143 | `imap.yandex.ru` |
| Mail.ru | ✅ 993 | ✅ 143 | `imap.mail.ru` |
| Zoho | ✅ 993 | ✅ 143 | `imap.zoho.com` |

---

## 🐛 Типичные ошибки

### AUTHENTICATIONFAILED

**Причина:** Неверный пароль или IMAP не включён у провайдера.

**Решение:**
```bash
python check_mail.py remove "email@gmail.com"
python check_mail.py add "email@gmail.com" "newpass" "imap.gmail.com" "993" "ssl"
```

### Connection Error (Port 143 vs 993)

**Причина:** Сервер использует порт 143 с STARTTLS.

**Решение:**
```bash
python check_mail.py add "email@gmail.com" "pass" "imap.gmail.com" "143" "starttls"
```

---

## 💡 Примеры использования

### Сценарий 1: Новый пользователь

```bash
# 1. Посмотреть help
python check_mail.py

# 2. Добавить первый аккаунт
python check_mail.py add "alex@gmail.com" "pass123" "imap.gmail.com" "993" "ssl"

# 3. Запустить проверку
python check_mail.py -get

# 4. Посмотреть результат
tail -50 mail_check.log
```

### Сценарий 2: Несколько аккаунтов

```bash
# Google
python check_mail.py add "alex@gmail.com" "pass1" "imap.gmail.com" "993" "ssl"

# Beget
python check_mail.py add "alex@beget.com" "pass2" "imap.beget.com" "993" "ssl"

# Outlook
python check_mail.py add "alex@outlook.com" "pass3" "imap-outlook.office365.com" "993" "ssl"

python check_mail.py -get
```

### Сценарий 3: Мониторинг

```bash
# Запуск 1 раз в день
python check_mail.py -get

# Или расписание задачи (Windows):
schtasks /create /tn "Mail Robot" /tr "python check_mail.py -get" /sc daily
```

---

## 🔧 Продвинутые настройки

### Уровень логирования

```python
# Для отладки:
logging.getLogger().setLevel(logging.DEBUG)
```

### Бэкап

```bash
python check_mail.py -get
cp mail_check.db mail_check.db.backup.$(date +%Y%m%d)
```

---

## 📊 Мониторинг работы

### Проверка состояния БД:

```bash
python -c "import sqlite3; db=sqlite3.connect('mail_check.db'); print(f'Size: {os.path.getsize('mail_check.db')} bytes')"
```

### Проверка логов:

```bash
tail -30 mail_check.log
```

---

## 📞 Полезные ссылки

- **Детальная документация:** `USAGE.md`
- **Быстрый старт:** `QUICK_START.md`
- **Архитектура:** `ARCHITECTURE.md`

---

## 🎉 Удачи в автоматизации!

Приятной работы с почтой! 🚀

---

## 📝 Версия

**Версия:** 1.4  | **Автор:** Mail Robot Team  | **Лицензия:** MIT  | **Python:** 3.6+
