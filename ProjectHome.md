pyfsm is a light-weight finite state implementation written in Python. It uses Python decorators to provide an easy to read, flexible interface for writing finite state machines.

States are created through a combination of decorators and free functions. Each state is placed into an over-arching "task". This task can then be retrieved and the state machine can be started.

For example:
```
@state('hello_world') # task 'hello_world'
@transition(1, 'goodbye') # transitions on 1 to the goodbye state
def say_hello(tsk): # state name is say_hello, the task is the second object
    ...
```

Check out the [samples.py](http://code.google.com/p/pyfsm/source/browse/samples.py) file to see more examples.

To install, use the setup.py file included.

```
python setup.py install
```