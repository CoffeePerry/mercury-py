![Mercury release](https://img.shields.io/badge/Current%20Mercury%20Version-Emailer-red?style=for-the-badge)

![mercury-py logo](https://github.com/CoffeePerry/mercury-py/blob/master/art/mercury.png?raw=true)

![GitHub release (latest by date)](https://img.shields.io/github/v/release/CoffeePerry/mercury-py)
![PyPI](https://img.shields.io/pypi/v/mercury-py?logo=PyPI&logoColor=white)
![PyPI - Status](https://img.shields.io/pypi/status/mercury-py)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mercury-py?logo=Python&logoColor=white)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/mercury-py)

[![Flask](https://img.shields.io/badge/framework-Flask-black?logo=Flask&logoColor=white)](https://github.com/pallets/flask/)

[![GitHub license](https://img.shields.io/github/license/CoffeePerry/mercury-py)](https://github.com/CoffeePerry/mercury-py/blob/master/LICENSE)

[![GitHub issues](https://img.shields.io/github/issues/CoffeePerry/mercury-py)](https://github.com/CoffeePerry/mercury-py/issues)

# mercury-py
**mercury-py** (*Mercury for Python*) is a Python based microservice that allow to manage scheduled notifications'
sending.

## Introduction
The project consists of a *Flask-based* **RESTful Web API**, through which it is possible to manage the scheduling
of notifications.

*SQLite* database is used internally.

*MongoDB* database is used to store scheduled notifications.

The dispatch of notifications is managed by *Celery-based* submodules:
- A **Celery Beat** that acts as an activator for the **Workers**.
- A **Celery Worker** for each category of notification, who takes care of managing the specific type of dispatch.

*RabbitMQ* message-broker is used for interprocess communications.

## Notifications Categories
The categories of notifications that can currently be sent are:
- Email.

Categories will be implemented:
- SMS;
- Push notification - *Firebase Cloud Messaging* (*FCM*);
- *Telegram* message.

## Setup instructions

### Getting it
To download mercury, either fork this *GitHub* repo or simply download it from *PyPI* via *pip*:
~~~
pip install mercury-py
~~~

### Install Dependencies
Mercury needs:
- *MongoDB*: get it from the official site (*https://www.mongodb.com/*) or from the official
repository of your Linux distro, for example, on *Debian-like* systems:
~~~
sudo apt install mongodb
~~~
- *RabbitMQ*: get it from the official site (*https://www.rabbitmq.com/*) or from the official
repository of your Linux distro, for example, on *Debian-like* systems:
~~~
sudo apt install rabbitmq-server
~~~

After that, to use Mercury, we need to create a *RabbitMQ* user, a virtual host and allow that user access to that virtual host:

From terminal, type (substitute in appropriate values for [MYUSER] and [MYPASSWORD] below):

~~~
sudo rabbitmqctl add_user [MYUSER] [MYPASSWORD]
sudo rabbitmqctl add_vhost mercury
sudo rabbitmqctl set_permissions -p mercury [MYUSER] ".*" ".*" ".*"
~~~
See the *RabbitMQ* *Admin Guide* for more information about access control
(*http://www.rabbitmq.com/admin-guide.html#access-control*).

### Setting up

Copy and paste file **config-\*.py**, from folder **configs**, into folder **mercury-instance**
and modify it according to your needs.

#### Configure the Secret Key
SECRET_KEY should be changed to some random bytes in production.

You can use the following command to output a random secret key:
~~~
$ python -c 'import os; print(os.urandom(16))'
~~~

Then place returned value into your **config.py**.

### Starting **Celery Worker** Alternative

[Source](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html#starting-the-scheduler)

You can also embed beat inside the worker by enabling the workers -B option, this is convenient if you’ll never run more than one worker node, but it’s not commonly used and for that reason isn’t recommended for production use:
~~~
celery -A mercury.app.celery worker -B --logfile=instance\logs\celery.log --pidfile=instance\celerybeat\celery.pid --schedule=instance\celerybeat\celery-schedule.db --loglevel=DEBUG
~~~

### **Note**: *Windows* Systems

On *Windows* systems, an additional dependency must be installed in order for Celery-based submodules to function
properly.

Download and install *Gevent* from *PyPI* via *pip*:
~~~
pip install gevent
~~~
And run (**Celery Beat** and **Celery Workers**) from terminal:
~~~
celery -A mercury.app.celery worker --logfile=instance/logs/celeryworker.log --loglevel=DEBUG --pool=gevent
celery -A mercury.app.celery beat --logfile=instance/logs/celerybeat.log --loglevel=DEBUG --pidfile=instance/celerybeat/celerybeat.pid --schedule=instance/celerybeat/celerybeat-schedule.db
~~~
