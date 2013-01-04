# coding:utf-8
from django.http import HttpResponse
from django.utils import simplejson as json
from django.views.generic import View
from django.conf import settings
import threading
import redis
import uuid


class RealtimeTicketError(Exception):
    pass


class RedisConnection(object):

    _connection = None

    _lock = threading.Lock()

    @classmethod
    def connection(cls, host='localhost', port=6379, db=0, password=None, socket_timeout=None, connection_pool=None):
        options = getattr(settings, 'REALTIME_TICKET_REDIS', {})
        if not cls._connection:
            with cls._lock:
                if not cls._connection:
                    cls._connection = redis.StrictRedis(
                        host=options.get('host', host),
                        port=options.get('port', port),
                        db=options.get('db', db),
                        password=options.get('password', password),
                        socket_timeout=options.get(
                            'socket_timeout', socket_timeout),
                        connection_pool=connection_pool
                    )
        return cls._connection

    @classmethod
    def set(cls, key, value, expire):
        try:
            cls.connection().set(key, value)
            cls.connection().expire(key, expire)
        except redis.ConnectionError, e:
            raise RealtimeTicketError(e)


class RealtimeTicket(object):

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

    def set(self, connection):
        """
        set ticket using provided connection
        """
        key = self.ticket_key()
        value = self.ticket_value()
        expire = self.ticket_expire()
        connection.set(key, value, expire)
        return key

    def ticket_expire(self):
        """
        return ticket expiration time.
        """
        return getattr(settings, 'REALTIME_TICKET_EXPIRE', 5)

    def ticket_key(self):
        """
        return ticket key which will be used in authorization request
        to asynchronous backend.
        """
        return str(uuid.uuid4())

    def ticket_value(self):
        """
        provide some additional information
        about user(connection) as ticket key's value.
        """
        if hasattr(self.request, 'user') and self.request.user.is_authenticated():
            userid, username = self.request.user.id, self.request.user.username
        else:
            raise RealtimeTicketError('user not authenticated')
        return json.dumps({'id': userid, 'username': username})


class RealtimeTicketFactory(object):

    # class which creates ticket
    ticket_class = RealtimeTicket
    # class which saves ticket
    connection_class = RedisConnection

    def __init__(self, ticket_class=None, connection_class=None):
        if ticket_class:
            self.ticket_class = ticket_class
        if connection_class:
            self.connection_class = connection_class

    def create_ticket_info(self, request):
        try:
            key = self.create_ticket(request)
        except RealtimeTicketError, e:
            message = 'error while creating ticket'
            if settings.DEBUG:
                message += ': %s' % str(e)
            context = {'status': 'error', 'message': message}
        else:
            context = {'status': 'ok', 'message': key}
        return context

    def create_ticket(self, request):
        ticket = self.ticket_class(request)
        key = ticket.set(self.connection_class)
        return key


class RealtimeTicketView(RealtimeTicketFactory, View):

    def post(self, request):
        context = self.create_ticket_info(request)
        return HttpResponse(json.dumps(context), mimetype="application/json")
