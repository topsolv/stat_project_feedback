Stat project feedback
======

Python script allowing to create lots of weblinks to multiple subfolders of the main folder in Google Drive and put the links into separate files.

Author: Alexander Zasorin <code@zasorin.ru>
DISCLAIMER: this code is not supported

How it works
============

The python script prepares link to each students graded paper in Google Drive.
Script creates local folder with subfolder-per-student structure.
In each student subfolder, one file is put: "feedback.txt" with link to Google Drive folder corresponding to that students graded paper.

This python script should be run locally.
It requires write access to Google account with Google Drive.
It uses OAuth2 connection with Google Drive API v3.

Installation and usage
============

*Required:*
Python 3
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

### Получение доступа к Сервису Google Drive
ATTENTION: Google много где предлагает платный GSuite, и други платные сервисы "попробовать бесплатно с кредитом 300 долларов" - важно случайно не нажать.

1. https://console.developers.google.com/
Создать проект. Войти в проект.

2. Учетные данные -> Создать учетные данные -> Идентификатор клиента OAuth
Тип приложения: Веб-приложение
Разрешенные источники javascript:  http://localhost:8080
Разрешенные UTI перенаправления: http://localhost:8080/
Создать

3. Скачать client_secret_<verylong>.json, переименовать в client_secret.json и положить в папку со скриптом. (то есть там всего 2 файла: сам питоновский скрипт и client_secret.json

### Получение доступа к аккаунту Google Drive

4. Запустить скрипт, и при первом запуске откроется окно браузера, где будет предложено войти в аккаунт Google и выдать доступ к нему проекту, название которого вы указали на первом шаге. Будет сказано, что проект не проверен и это небезопасно -> Разрешить

5. Скрипт дальше срабатывает. Если папки с заданным названием нет или таких папок несколько, ничего больше не происходит: скрипт печатает на экран все найденные папки с данным названием.
Если папка ровно одна найдена, то скрипт отрабатывает до конца.

6. Замечание: если указать createLink=false, то ссылки все равно сохранятся, просто не будут работать, при попытке по ним зайти будет сказано, что нужен запрос доступа.
