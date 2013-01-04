REALTIME TICKET
===============

Important
---------
This is an experimental project. Please, be careful to use it in production. Be sure that you understand how it really works. 

Overview
--------
Django and realtime are not friends. You should use Tornado, Twisted, Cyclone, Gevent, Nodejs together with Django to create realtime web-applications. This app helps to authorize your 
Django users in asynchronous backend using expiring tickets. By default, this app uses Redis to 
create such expiring tickets. Before create connection to async backend you insert ticket in Redis. After this you should append this ticket to connection request. In async backend you should check that this key exists in Redis, get additional user information (key's value) if you need it, then delete this key from Redis.


Using
-----

```bash
pip install git+git://github.com/FZambia/django-realtime-ticket.git
```

Add `realtime_ticket` to your `INSTALLED_APPS`

Add `realtime_ticket.urls` to your app's urlpatterns:
```
url(r'', include('realtime_ticket.urls'))
```

And then you can create new ticket making POST request on url `/ticket/`.
If everything is OK you will receive json:
```python
{'status': 'ok', 'message': "NEW_TICKET_FOR_USER"}
```

Use this ticket to create authorization request to your async backend. Do not forget to delete this key from Redis after successful authorization.


Configuration
-------------

You can configure app's behaviour in your `settings.py`:
```python

# time (in seconds) after that ticket will expire
REALTIME_TICKET_EXPIRE = 10

# redis connection settings
REALTIME_TICKET_REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'socket_timeout': 1
}
```
