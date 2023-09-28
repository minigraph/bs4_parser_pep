# Проект парсинга pep
### Описание
Перед Вами проект парсера. Учебный проект Яндекс.Практикум.
Проект ставит перед собой цели получения данных документации с помощью командной строки.
Использовано:
* Python v.3.7.5 (https://docs.python.org/3.7/)
* Beautiful Soup v.4.9.3 (https://beautiful-soup-4.readthedocs.io/en/latest/)
* Requests Cache v.1.0.0 (https://requests-cache.readthedocs.io/en/stable/)
* Tqdm v.4.61.0 (https://tqdm.github.io/)
* Flake 8 v.5.0.4 (https://buildmedia.readthedocs.org/media/pdf/flake8/stable/flake8.pdf)

### Установка:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/minigraph/bs4_parser_pep.git
```

```
cd bs4_parser_pep

```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Обновите PIP, дабы избежать ошибок установки зависимостей:

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

### Документация парсера:
##### Информация о нововведениях
Команда:
```bash
python main.py whats-new
```
Пример вывода:
```bash
Ссылка на статью Заголовок Редактор, автор
https://docs.python.org/3/whatsnew/3.11.html What’s New In Python 3.11¶  Editor Pablo Galindo Salgado  
```
##### Информация о версиях Python
Команда:
```bash
python main.py latest-versions
```
Пример вывода:
```bash
Ссылка на документацию Версия Статус
https://docs.python.org/3.13/ 3.13 in development
https://docs.python.org/3.12/ 3.12 pre-release
```
##### Загрузка документации
Команда:
```bash
python main.py download
```
Пример вывода:
```bash
"21.09.2023 11:48:08 - [INFO] - Парсер запущен!"
"21.09.2023 11:48:08 - [INFO] - Аргументы командной строки: Namespace(clear_cache=False, mode='download', output=None)"
"21.09.2023 11:48:11 - [INFO] - Архив был загружен и сохранён: /home/s_17/bs4_parser_pep/src/downloads/python-3.11.5-docs-pdf-a4.zip"
"21.09.2023 11:48:11 - [INFO] - Парсер завершил работу."
```

Вызов справки по проекту:
```bash
python main.py -h
```

### Автор:
* Михаил Никитин
* * tlg: @minigraf 
* * e-mail: minigraph@yandex.ru; maikl.nikitin@yahoo.com;