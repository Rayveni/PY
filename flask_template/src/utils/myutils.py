import functools
def exception(function):
    """
    A decorator that wraps the passed in function and logs 
    exceptions should one occur
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return (True,),function(*args, **kwargs)
        except Exception as err:
            # log the exception
            err = f"There was an exception in {function.__name__} error {err}"
            return (False,err),None

    return wrapper