handlers = {}

def register(signal_name):
    def inner(func):
        handlers[signal_name] = func
        return func
    return inner

def clear_handlers():
    global handlers
    handlers = {}

