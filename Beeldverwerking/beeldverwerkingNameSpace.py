from socketIO_client import BaseNamespace

class BeeldverwekingNameSpace(BaseNamespace):
    def __init__(self,*args,**kwargs):
        super(BeeldverwekingNameSpace, self).__init__(*args,**kwargs)
        self.awaiting_events = {}

    def on_update_route_description(self, params):
        global current_route_description
        current_route_description = params

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
        print "powers set!"