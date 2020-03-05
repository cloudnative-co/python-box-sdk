import inspect
from inspect import signature


def find_method_args(obj, method_name):
    """
    @brief          メソッドの引数を取得
    @params[in]     obj     対象のオブジェクト

    """
    members = inspect.getmembers(obj, inspect.ismethod)
    for member in members:
        if member[0] == method_name:
            param = inspect.getfullargspec(member[1])
            args = param.args
            del args[0]
            return args
    return []

def find_method_params(obj, method_name):
    members = inspect.getmembers(obj, inspect.ismethod)
    for member in members:
        if member[0] == method_name:
            param = inspect.getfullargspec(member[1])
            return param
    return None

def webhook_response(payload: dict, status=200):
    message = [
        "webhook={}".format(payload["id"]),
        "trigger=NO_ACTIVE_SESSION",
        "source=<file id={id} name=\"{name}\">".format(**payload["source"])
    ]
    message = ", ".join(message)
    return {
        'statusCode': status,
        'headers': {'content-type': 'application/json'},
        'body': message
    }
