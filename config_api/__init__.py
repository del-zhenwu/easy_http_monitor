
class APIMixin(object):
    def __init__(self):
        pass

    @property
    def api_res(self):
        res = {
            "code": 200,
            "msg": "",
            "data": None
        }
        return res


def set_receivers(group):
    receivers = []
    return receivers
