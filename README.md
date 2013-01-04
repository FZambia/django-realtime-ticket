REALTIME TICKET for DJANGO
==========================
Authorize [Django](https://www.djangoproject.com/) users in realtime (asynchronous) backends using [Redis](http://redis.io/) expiring tickets.

Ticket in this case is just a key-value pair. Key is a unique string, value - json of additional information about user (id, username).

Important
---------
This is an experimental project. Please, be careful to use it in production. Be sure that you understand how it really works. 

Overview
--------
Django and realtime are not friends.

You should use [Tornado](https://github.com/facebook/tornado), [Twisted](http://twistedmatrix.com/trac/), [Cyclone](https://github.com/fiorix/cyclone), [Gevent](https://github.com/SiteSupport/gevent) or [Nodejs](https://github.com/joyent/node) or something else together with Django to create realtime web-applications.

This app helps to authorize your Django users in asynchronous backend using expiring tickets.

By default, this application uses Redis to create such expiring tickets.

This is a sequence of actions you need to do to authorize user using this technique:

* before creating connection to async backend insert user ticket into Redis.
* After this append inserted ticket to connection request.
* In async backend check that ticket from request exists in Redis, get additional user information (key's value) if necessary.
* Delete key from Redis to prevent multiple connections with single key.

This app simplifies only first point of list. The rest of work is up to you! You should choose one of async servers, implement ticket check logic and (the most difficult part) append ticket for every connection request to those async server.

Install
------

```bash
pip install git+git://github.com/FZambia/django-realtime-ticket.git
```

Add `realtime_ticket` to your `INSTALLED_APPS`

Add `realtime_ticket.urls` to your app's urlpatterns:
```
url(r'', include('realtime_ticket.urls'))
```

Using
-----

After install you can create new ticket making POST javascript(jquery) request on url `/ticket/` (do not forget about `csrf_token`).
If everything is OK you will receive json:
```python
{'status': 'ok', 'message': "NEW_TICKET_FOR_USER"}
```

Use this ticket in POST callback to create authorization request to your async backend. Do not forget to delete this key from Redis after successful authorization.

If you don't want to make such javascript calls you can use middleware provided by this application - it inserts
variable with name `realtime_ticket` into your template context. So you just use template as usually. You must use
those middleware on per-view basis to avoid creating tickets on every request to your site. Here is an example:

```python
from django.views.generic import TemplateView
from django.utils.decorators import decorator_from_middleware
from django.utils.decorators import method_decorator
from realtime_ticket import RealtimeTicketMiddleware


class ChatView(TemplateView):

    @method_decorator(decorator_from_middleware(RealtimeTicketMiddleware))
    def dispatch(self, *args, **kwargs):
        return super(ChatView, self).dispatch(*args, **kwargs)

	def get(request, *args, **kwargs):
		# YOUR APPLICATION CODE HERE
```

Now in your template you have `{{realtime_ticket}}`. If this variable is None - something went wrong (broken Redis connection, unauthenticated user etc.)


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
