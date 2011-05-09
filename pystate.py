
class task_registry(object):
    def __init__(self):
        self.tasks = {}
        self.getattr = None

    def set_getter(self, getter):
        self.getattr = getter
    def get_getter(self):
        return self.getattr

    def get_task(self, name):
        return self.tasks.setdefault(name, task(name))
Registry = task_registry()

class task(object):
    warn_msg = 'warning: multiple instances of state %s in task %s'
    def __init__(self, name):
        self.name = name
        self.current_state = None
        self.states = {}
        self.getattr = None

        self._locals = {}
        self._globals = {}
        self.callbacks = {}
        self.exit = []
        class callback(object):
            def __init__(callback, key):
                self.key = key
            def __call__(callback, func):
                if not self.callbacks.has_key(self.key):
                    self.callbacks[self.key] = []
                self.callbacks[self.key].append(func)
                return func
        self.callback = callback

        def atexit(func):
            self.exit.append(func)
            return func
        self.atexit = atexit

    def start(self, name):
        for x in self.exit:
            x(self)

        self.current_state = self.states[name]
        self.callbacks = {}
        self.exit = []
        self._locals = {}
        self.current_state.enter(self)

    def send(self, event):
        assert self.current_state, 'state machine is not running'

        # recover the key for this event
        for getattr in (self.getattr, Registry.getattr, lambda x: x):
            try:
                key = getattr(event)
            except:
                pass
            else:
                break

        # check callbacks first
        callback = self.callbacks.get(key, [])
        for x in callback:
            x(event)

        # if a transition exists, change the state
        trans = self.current_state.transitions.get(key, None)
        if trans:
            self.start(trans)

    def add_state(self, name, state):
        if self.states.has_key(name):
            print task.warn_msg % (name, self.name)
        self.states[name] = state

    def get_name(self):
        return self.name

    @property
    def locals(self):
        return self._locals
    @property
    def globals(self):
        return self._globals

class transition(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value
    def __call__(self, func):
        trans = getattr(func, 'transitions', {})
        trans[self.key] = self.value
        setattr(func, 'transitions', trans)
        return func

class state(object):
    def __init__(self, name):
        self.task = Registry.get_task(name)
        self.transitions = {}
    def __call__(self, func):
        self.func = func
        self.transitions.update(getattr(func, 'transitions', {}))
        self.task.add_state(func.__name__, self)
        return self
    def enter(self, task):
        self.func(task)
