README
=====================

Этот README документирует все шаги, необходимые для создания и запуска веб-приложения.

<h4>Реализованная функциональность</h4>
<ul>
    <li>Скрипты для сбора данных с xls и импортирование их в БД;</li>
    <li>API для работы фронтенда;</li>
    <li>Построение маршрута от точки до точки с учетом экологичности пути;</li>
</ul> 
<h4>Особенность проекта в следующем:</h4>
<ul>
 <li>Добавление и учет таких новых метрик, от которых будет зависеть построение маршрута, как наличие пробок на дороге, наличие широкополосных дорог рядом с построенным маршрутом, и.т.д;</li>
 <li>Учет статистический значений экологических коэффициентов в зависимости от текущего дня недели и времени суток;</li>
 </ul>
<h4>Основной стек технологий:</h4>
<ul>
    <li>Python.</li>
	<li>Django, Django Rest Framework</li>
	<li>PostgreSQL.</li>
	<li>fabric.</li>
	<li>Docker, docker-compose.</li>
	<li>Poetry.</li>
	<li>Git, Github.</li>
  
 </ul>
<h4>Демо</h4>
<p>Демо сервиса доступно по адресу: https://greenway2.herokuapp.com/ </p>


СРЕДА ЗАПУСКА
------------
1) развертывание сервиса производится на ubuntu-like linux (ubuntu 16+);
2) требуется установленный docker и docker-compose для разворачивания проекта;
3) требуется установленный интерпретатор Python 3.8+ и пакет fabric.

УСТАНОВКА
------------
### Настройки Docker

##### Установка

* [Подробное руководство по установке](https://docs.docker.com/engine/install/ubuntu/)

##### Команды для запуска docker без sudo (для локалки)

* `sudo groupadd docker`
* `sudo gpasswd -a ${USER} docker`
* `newgrp docker`
* `sudo service docker restart`

##### Проверка работоспособности docker без sudo

* `docker run hello-world`

### Настройки Docker-compose

##### Установка

* [Подробное руководство по установке](https://docs.docker.com/compose/install/)

##### Команда для запуска docker-compose без sudo (для локалки)

* `sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose`

### Fabric

Файл `fabfile.py` содержит ряд функций, которые помогают при локальной разработке.

##### Установка

* `sudo pip install Fabric3`

##### Команды fabric

* `fab dev` - запустить локально веб приложение
* `fab makemigrations` - создать файл миграций
* `fab migrate` - применить миграции
* `fab createsuperuser` - создать супер пользователя
* `fab shell` - зайти в shell django приложения
* `fab bash` - зайти в bash контейнера server
* `fab kill` - остановить все запущенные контейнеры

### Локальная разработка

##### Команды для первого запуска

* `docker-compose build` - создать контейнеры docker
* `fab dev` - запустить веб приложение
* `fab migrate` - применить миграции

##### Команды для последующего запуска

* `fab dev` - зупустить веб приложение
* `fab migrate` - применить миграции

**Примечание**: при добавлении каких-либо зависимостей в проект или изменении Dockerfile, необходимо пересобрать контейнер с веб-приложением `docker-compose build server`

##### Доступ

* http://localhost:8000

### Развертывание веб-приложения на сервере (работа с nginx)

##### Команды

* `docker-compose -f docker-compose.prod.yml build` - сборка контейнеров 
* `docker-compose -f docker-compose.prod.yml up` - запуск контейнеров 

### Примечания

* При разработке можно убрать или добавить зависимости
    
    `docker-compose run server poetry remove req_name`<br>
    `docker-compose run server poetry add req_name`


РАЗРАБОТЧИКИ

<h4>Крикунова Ольга backend https://t.me/@tykva43 </h4>