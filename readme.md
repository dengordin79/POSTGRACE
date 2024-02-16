# Проект по работе с PostgreSQL

## Запуск

1. Установить venv (по желанию)
```bash
py -m venv venv
```

2. Установить зависимости
```bash
pip install -r requirements.txt
```

3. Создать файл `.env` и прописать туда константы:
```env
HOST=хост почты
USER=пользователь почты
PASSWORD=пароль от почты
PORT=порт (465 стандартный)
DB=название БД
UDB=пользователь БД
PDB=пароль к БД
HDB=хост БД
PDB=порт БД
```

4. Запустить файл `main.py`