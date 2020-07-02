from config.settings import VERSION, NAME


SYMBOLS = {
        'detail': '<i class="fas fa-angle-double-right"></i>',
        'delete': '<i class="fas fa-trash-alt"></i>',
        'delete_regular': '<i class="far fa-trash-alt"></i>',
        'update': '<i class="fas fa-edit"></i>',
        'category': '<i class="fas fa-box"></i>',
        'deal': '<i class="fas fa-balance-scale"></i>',
        'user': '<i class="fas fa-user-tie"></i>',
        'guild': '<i class="fas fa-users"></i>',
        'feedback': '<i class="fas fa-clipboard"></i>',
        'feedback_regular': '<i class="far fa-clipboard"></i>',
        'virtual': '<i class="fas fa-brain"></i>',
        'listing': '<i class="fas fa-file-alt"></i>',
        'bookmark': '<i class="fas fa-bookmark"></i>',
        'search': '<i class="fas fa-search"></i>',
        'chat': '<i class="fas fa-comments"></i>',
        'chat_regular': '<i class="far fa-comments"></i>',
        'location': '<i class="fas fa-compress-arrows-alt"></i>',
    }


def default(request):
    """registered context processor"""
    ret = {}
    ret['version'] = VERSION
    ret['version_str'] = '.'.join((str(elem) for elem in VERSION))
    ret['name'] = NAME
    ret['symbols'] = SYMBOLS
    return ret
