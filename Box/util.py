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

HEADER_KEYS = [
    "if_match",
    "if_none_match",
    "x_rep_hints",
    "content_md5",
    "content_range",
    "content_type",
    "content_length",
    "digest",
    "range"
]

def get_arguments(args: dict, keys: list = None, ignores: list = None):
    def snake_to_kebab(key):
        ret = []
        for key in key.split("_"):
            ret.append(key.capitalize())
        return "-".join(ret)

    ret = {}
    for ky in args:
        if ky == "self":
            continue
        if keys is not None:
            if ky not in keys:
                continue
        if ignores is not None:
            if ky in ignores:
                continue
        if args[ky] is None:
            continue
        if args[ky] is not None:
            if isinstance(args[ky], datetime.datetime):
                ret[ky] = args[ky].strftime("%Y-%m-%dT%H:%M:%S%z")
            elif isinstance(args[ky], list):
                ret[ky] = ",".join(args[ky])
            else:
                ret[ky] = args[ky]
        if ky in HEADER_KEYS:
            v = ret.pop(ky)
            ky = snake_to_kebab(ky)
            ret[ky] = v
    return ret
