# 🚀 Mail Robot — Быстрый старт

## 📖 Описание

**Mail Robot** — программа для автоматической проверки почтовых ящиков IMAP-аккаунтов на наличие новых сообщений.

### **Что умеет:**
- ✅ Автоматически проверяет все настроенные аккаунты
- ✅ Хранит аккаунты в SQLite БД
- ✅ Поддерживает SSL и STARTTLS
- ✅ Логирование в файл и консоль
- ✅ Удобный CLI интерфейс

### **Для чего:**
- Мониторинг писем из разных почтовых ящиков
- Автоматическая загрузка новых писем
- Простая настройка и расширение

---

## ⚡ Быстрый старт

### **1. Установка (если нужно):**

```bash
# Если Python не установлен:
python --version

# Если не установлен:
# Скачать с https://python.org
```

### **2. Первичный запуск (показать help):**

```bash
python check_mail.py
```

**Выводит:**
```text
Mail Robot - Email Checker

USAGE:
    python check_mail.py              - Run mail check for all accounts
    python check_mail.py add "email" "password" "server" "port" "ssl"
    python check_mail.py list         - List all configured accounts
    python check_mail.py remove "email"
    python check_mail.py help         - Show this help message
```

### **3. Добавление первого аккаунта:**

```bash
python check_mail.py add "user@gmail.com" "mypassword" "imap.gmail.com" "993" "ssl"
```

### **4. Проверка почты:**

```bash
# Просто запустить скрипт — он проверит все аккаунты
python check_mail.py
```

### **5. Управление аккаунтами:**

```bash
# Посмотреть список:
python check_mail.py list

# Удалить аккаунт:
python check_mail.py remove "user@gmail.com"
```

---

## 📋 Примеры использования

### **Добавить аккаунт Gmail:**

```bash
python check_mail.py add "alex@gmail.com" "secret123" \
    "imap.gmail.com" "993" "ssl"
```

### **Добавить аккаунт Beget (SSL):**

```bash
python check_mail.py add "USER_EMAIL_HERE" "USER_PASSWORD_HERE" \
    "USER_IMAP_SERVER_HERE" "993" "ssl"
```

### **Добавить аккаунт Beget (STARTTLS):**

```bash
python check_mail.py add "test@domain.com" "secret" \
    "imap.domain.com" "143" "starttls"
```

### **Запуск проверки для всех аккаунтов:**

```bash
python check_mail.py
```

### **Просмотр списка аккаунтов:**

```bash
python check_mail.py list
# Выводит:
#   1. USER_EMAIL_HERE
#      Server: USER_IMAP_SERVER_HERE:993 (ssl)
#      Last checked: 2026-04-22
#   2. USER_EMAIL_2_HERE
#      Server: USER_IMAP_SERVER_2_HERE:993 (ssl)
#      Last checked: 2026-04-22
```

---

## 📁 Структура проекта

```
mail_robot/
├── check_mail.py          # Главный скрипт
├── mail_check.db          # Баз данных (SQLite)
├── mail_check.log         # Логи
└── docs/                  # Документация
    ├── readme.md          # Этот файл
    ├── skill.md           # Гайд по использованию
    └── structure.md       # Техническая документация
```

---

## 🔗 Полезные ссылки

- **Техническая документация:** `docs/structure.md`
- **Руководство по использованию:** `docs/skill.md`
- **Архитектура:** `docs/structure.md`

---

## 🎯 Типичные сценарии

### **Сценарий 1: Начать использовать**

```bash
# 1. Посмотреть help
python check_mail.py

# 2. Добавить аккаунт
python check_mail.py add "user@gmail.com" "pass" "imap.gmail.com" "993" "ssl"

# 3. Запустить проверку
python check_mail.py

# 4. Проверить результат
python check_mail.py list
```

### **Сценарий 2: Добавить несколько аккаунтов**

```bash
# Google
python check_mail.py add "alex@gmail.com" "pass1" "imap.gmail.com" "993" "ssl"

# Beget
python check_mail.py add "USER_EMAIL_2_HERE" "USER_PASSWORD_2_HERE" \
    "USER_IMAP_SERVER_2_HERE" "993" "ssl"

# Outlook
python check_mail.py add "me@outlook.com" "pass3" "imap-outlook.office365.com" "993" "ssl"

# Запустить проверку всех:
python check_mail.py
```

### **Сценарий 3: Мониторинг**

```bash
# Проверка 1 раз в день
python check_mail.py

# или запуск в фоне
# Windows:
schtasks /create /tn "Mail Robot" /tr "python check_mail.py" /sc daily
```

---

## 🐛 Распространённые ошибки

### **Ошибка: AUTHENTICATIONFAILED**

```bash
INFO: [CONN] Attempting to log in...
ERROR: [CONN] Authentication or Connection Error: b'[AUTHENTICATIONFAILED]'
```

**Причина:** Неверный пароль или настройка IMAP для этого аккаунта.

**Решение:**
1. Проверить пароль
2. Убедиться, что IMAP включён в настройках почты
3. Проверить порт (993 для SSL)

---

### **Ошибка: Connection Error (Port 993)**

**Причина:** Сервер использует порт 143 с STARTTLS.

**Решение:**
```bash
python check_mail.py add "user@gmail.com" "pass" "imap.gmail.com" "143" "starttls"
```

---

## 🛠 Настройка под разные почтовые сервисы

### **Gmail**

```bash
# SSL (рекомендуется)
python check_mail.py add "user@gmail.com" "pass" "imap.gmail.com" "993" "ssl"

# STARTTLS
python check_mail.py add "user@gmail.com" "pass" "imap.gmail.com" "143" "starttls"
```

### **Beget**

```bash
# SSL (рекомендуется)
python check_mail.py add "user@beget.com" "pass" "imap.beget.com" "993" "ssl"

# STARTTLS
python check_mail.py add "user@beget.com" "pass" "imap.beget.com" "143" "starttls"
```

### **Outlook/Hotmail**

```bash
python check_mail.py add "user@outlook.com" "pass" "imap-outlook.office365.com" "993" "ssl"
```

---

## 📊 Что происходит при запуске?

### **Без аргументов (default):**

```bash
python check_mail.py
```

**Цикл:**
1. Инициализация БД
2. Чтение всех аккаунтов из `mail_check.db`
3. Для каждого аккаунта:
   - Подключение к IMAP серверу
   - Авторизация
   - Выбор папки INBOX
   - Поиск всех сообщений (`ALL`)
   - Парсинг первых 3 писем
   - Вывод в консоль
4. Обновление `last_checked_date` в БД
5. Выход

---

## 🎉 Удачи!

**Теперь вы знаете основы работы с Mail Robot!**

Наслаждайтесь удобной автоматизацией проверки почты! 🎉