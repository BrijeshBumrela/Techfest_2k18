from threading import Thread


def run_in_background(func):
    def decorator(*args, **kwargs):
        t = Thread(target=func, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()

    return decorator
