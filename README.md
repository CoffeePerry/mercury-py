![mercury-py logo](https://github.com/CoffeePerry/mercury-py/blob/master/art/mercury.png)

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
repository of your Linux disto, for example, on *Debian-like* systems:
~~~
sudo apt install mongodb
~~~
- *RabbitMQ*: get it from the official site (*https://www.rabbitmq.com/*) or from the official
repository of your Linux disto, for example, on *Debian-like* systems:
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

Create a folder called **Instance**, copy and paste file **config.py**, from **config-template**, and modify it
according to your needs.

### **Note**: *Windows* Systems

On *Windows* systems, an additional dependency must be installed in order for Celery-based submodules to function
properly.

Download and install *Gevent* from *PyPI* via *pip*:
~~~
pip install gevent
~~~
And run (**Celery Beat** and **Celery Workers**) from terminal:
~~~
beat --app=mercury.app.celery --logfile=instance/logs/celerybeat.log --loglevel=DEBUG --pidfile=instance/celerybeat/celerybeat.pid --schedule=instance/celerybeat/celerybeat-schedule.db
worker --app=mercury.app.celery --logfile=instance/logs/celeryworker.log --loglevel=DEBUG --pool=gevent
~~~
