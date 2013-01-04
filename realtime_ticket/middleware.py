# coding: utf-8
from .views import RealtimeTicketFactory, RealtimeTicketError


class RealtimeTicketMiddleware(object):

    def process_template_response(self, request, response):
        ticket_factory = RealtimeTicketFactory()
        try:
            ticket = ticket_factory.create_ticket(request)
        except RealtimeTicketError:
            ticket = None
        response.context_data['realtime_ticket'] = ticket
        return response