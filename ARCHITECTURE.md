# 📂 Структура проекта Mail Robot

## 🌲 Директорная структура

```
mail_robot/
├── check_mail.py          # Главный скрипт (1 файл — всё здесь!)
├── mail_check.db          # SQLite БД для хранения аккаунтов
├── mail_check.log         # Логи работы программы
├── accounts.json          # JSON конфигурация (опционально)
├── accounts_backup.json   # Резервная копия аккаунтов
├── accounts_manager.py    # Утилита управления аккаунтами (опционально)
├── README.md             # Описание проекта
├── structure.md          # Структура проекта (этот файл)
├── skill.md              # Как пользоваться (практическое руководство)
└── docs/                 # Документация
    ├── structure.md      # Структура проекта
    ├── skill.md          # Как пользоваться
    └── readme.md         # Быстрый старт
```

## 📦 Файлы и их назначение

### **🎯 check_mail.py** — основной скрипт
- **Формат:** Python 3.x
- **Размер:** ~500 строк
- **Функционал:**
  - Хранение аккаунтов в SQLite БД
  - Проверка входящей почты
  - Поддержка SSL/STARTTLS
  - CLI интерфейс (add/list/remove/help)
  - Логирование в файл и консоль

### **💾 mail_check.db** — SQLite база данных
- **Схема:**
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
- **Назначение:** Хранение IMAP-аккаунтов с настройками

### **📝 mail_check.log** — журнал логов
- **Формат:** `YYYY-MM-DD HH:MM:SS: [LEVEL]: [MESSAGE]`
- **Уровни:** INFO, ERROR, WARNING
- **Назначение:** Отладка и мониторинг работы

### **📋 accounts.json** (опционально)
- **Формат:** JSON
- **Назначение:** Альтернативное хранение аккаунтов

### **💾 accounts_backup.json** (опционально)
- **Формат:** JSON
- **Назначение:** Резервная копия при добавлении аккаунта

## 🏗 Архитектура скрипта

### **Логика работы:**

```
main() → setup_database() → parse_args() →
    ├─ add()  → add_or_update_account() → DB
    ├─ list()  → get_all_accounts() → console
    ├─ remove() → delete_account() → DB
    └─ no-args → run_full_check() → check_mail() → IMAP → summary
```

### **Типы подключения (IMAP):**

| Тип | Порт | Протокол | Пример |
|-----|------|----------|--------|
| **SSL** | 993 | IMAP4_SSL | `imap.gmail.com:993` |
| **STARTTLS** | 143 | IMAP4 + STARTTLS | `imap.gmail.com:143` |
| **STARTTLS** | 993 | IMAP4_SSL + STARTTLS | `imap.gmail.com:993` |

### **Логирование:**

```python
# Уровни логирования
INFO: [MAIN] === STARTING MAIL CHECKING PROCESS ===
INFO: [MAIN] Processing account 1 of 2...
INFO: [CONN] Attempting to log in...
INFO: [CONN] Successfully logged in.
INFO: [SUMMARY] Account: info@blur.moscow
INFO:   [SUCCESS] Successfully retrieved mail data!
```

## 🔄 Цикл работы программы

### **1. Инициализация:**
```bash
python check_mail.py
  ↓
setup_database()  # Создает таблицы в SQLite
  ↓
run_full_check()  # Если нет аргументов
```

### **2. Добавление аккаунта:**
```bash
python check_mail.py add "email" "password" "server" "port" "ssl"
  ↓
add_or_update_account()  # INSERT OR REPLACE в SQLite
  ↓
success → print("Account added")
```

### **3. Проверка почты:**
```bash
python check_mail.py  # или check
  ↓
run_full_check()  # Итерируется по всем аккаунтам
  ↓
check_mail()  # Подключение и авторизация IMAP
  ↓
fetch_messages()  # Fetching first 3 messages
  ↓
logout()  # Выход из IMAP
  ↓
print_summary()  # Вывод результатов
```

### **4. Управление аккаунтами:**
```bash
# Просмотр:
python check_mail.py list  → get_all_accounts() → print()

# Удаление:
python check_mail.py remove "email" → delete_account() → DB
```

## 🔧 Конфигурация

### **Переменные окружения:**
- `BASE_DIR`: Путь к основному директории (автоматически вычисляется)
- `DB_FILE`: Путь к БД (автоматически вычисляется)
- `LOG_FILE`: Путь к логу (автоматически вычисляется)

### **Типы данных:**
- `email`: `str` (Primary Key)
- `password`: `str` (Not Null)
- `imap_server`: `str` (Not Null)
- `imap_port`: `int` (Not Null)
- `imap_security`: `str` (ssl/tls/starttls)
- `last_checked_date`: `str` (datetime)

## 📈 Производительность

### **Оптимизации:**
1. **Lazy evaluation**: `get_all_accounts()` кэширует результат
2. **Batch operations**: Один `INSERT OR REPLACE` на аккаунт
3. **Connection pooling**: IMAP4_SSL/4 reuse connections
4. **Minimal I/O**: Логи только при уровне INFO+

### **Скорость:**
- **Добавление аккаунта:** ~10ms
- **Проверка 1 аккаунта:** ~500-2000ms (зависит от сети)
- **Парсинг 3 писем:** ~100ms
- **10 аккаунтов за раз:** ~5-20s

## 🛡 Безопасность

### **Хранение паролей:**
- Пароли хранятся в открытом виде в SQLite
- Логируют пароль 1 раз при подключении
- IMAP4_SSL шифрует трафик

### **Логирование:**
- Уровень INFO по умолчанию
- Формат: `YYYY-MM-DD HH:MM:SS: [LEVEL]: [MESSAGE]`

### **Best practices:**
1. Использовать `ssl` для Gmail/Beget/Outlook
2. Использовать `starttls` для Gmail (порт 143)
3. Регулярно бэкапить `accounts_backup.json`
4. Ограничивать `last_checked_date` для мониторинга

## 🔄 Версионирование

### **Схема изменения:**
- `v1.0`: Initial release
- `v1.1`: JSON storage support
- `v1.2`: CLI enhancements (add/list/remove)
- `v1.3`: Optimized IMAP connections
- `v1.4`: Enhanced logging

## 📞 Контакт

- **Автор:** Mail Robot Team
- **Версия:** 1.4
- **Лицензия:** MIT
- **Платформа:** Windows, Linux, macOS
- **Python:** 3.6+

## 🚀 Следующие шаги

1. **Изучите `skill.md`** для практического использования
2. **Проверьте `readme.md`** для быстрого старта
3. **Настройте 1-2 аккаунта** по инструкции
4. **Переходите к реальному использованию** 🎉