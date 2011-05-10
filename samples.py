
import pyfsm
from pyfsm import state, transition

@state('say_hello')
@transition('goodbye', 'goodbye')
def meet_and_greet(self):
    print 'hello, world!'
    @self.callback('hi')
    def print_hello(event):
        print 'hello, again'

@state('say_hello')
def goodbye(self):
    print 'leaving so soon?'

say_hello = pyfsm.Registry.get_task('say_hello')
say_hello.start('meet_and_greet')
say_hello.send('hi')
say_hello.send('dead message')
say_hello.send('hi')
say_hello.send('goodbye')

# custom/mutable event
class message(object):
    """
    An example of a custom event. pyfsm offers no event class
    of its own, but instead hooks into what event system you
    are already using.
    """
    def __init__(self, message):
        self.type = 'message'
        self.message = message

def get_event_type(event):
    return event.type
pyfsm.Registry.set_retrieval_func(get_event_type)

@state('messaging')
@transition('goodbye', 'goodbye')
def start_talking(self):
    self.locals['count'] = 0

    @self.callback('message')
    def print_string(event):
        print self.locals['count'], event.message
        self.locals['count'] += 1 # change local state from callbacks
    @self.atexit
    def cleanup(self):
        # perform actions when we leave this state (cleanup)
        print 'well, it was nice meeting you'
        self.globals['global_info'] = 'globals get kept around between tasks'

@state('messaging')
# we can use the same function name over again
# (as long as the state is different)
def goodbye(self):
    print 'locals variable has been cleared', self.locals.get('count', 0)
    print self.globals['global_info']
    print 'goodbye'

messaging = pyfsm.Registry.get_task('messaging')
messaging.start('start_talking')
messaging.send(message('hello, world'))
messaging.send(message('today is a good day'))
# pyfsm will try to get the key in the following order
# - provided key function for the task
# - provided key function for the registry
# - the event itself
# since the first two fail, it uses the message sent (which is just goodbye)
messaging.send('goodbye')
