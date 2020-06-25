from config.settings import VERSION, NAME


def default(request):
    """registered context processor"""
    ret = {}
    ret['version'] = VERSION
    ret['version_str'] = '.'.join((str(elem) for elem in VERSION))
    ret['name'] = NAME
    return ret
