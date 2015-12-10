from socketIO_client import BaseNamespace

current_route_description = []
is_started = False


class BeeldverwekingNameSpace(BaseNamespace):
    def __init__(self,*args,**kwargs):
        super(BeeldverwekingNameSpace, self).__init__(*args,**kwargs)
        self.awaiting_events = {}

    def on_connect(self):
        super(BeeldverwekingNameSpace, self).on_connect()
        ## print "yeay connected"

    def on_update_route_description(self, params):
        global current_route_description,is_started
        current_route_description = params
        if is_started is False:
            for command in current_route_description:
                if command["commandName"] == "start":
                    is_started = True
                    break

    def on_event_confirmation(self, params):
        if params['succes']:
            del self.awaiting_events[params['id']]
        else:
            if params.get('id', False):
                self.finish_command(params['id'])

    def finish_command(self, command_id):
        self.awaiting_events[command_id] = True
        self.emit('command_finished', {'id': command_id})

    def set_powers(self, left, right):
        self.emit("set_power", {"left": left, "right": right})
        print "powers set to:",left,",",right