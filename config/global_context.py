from config.settings import VERSION, NAME


SYMBOLS = {
        'bid': '<i class="fab fa-wpforms"></i>',
        'close': '<i class="fas fa-times"></i>',
        'forward': '<i class="fas fa-forward"></i>',
        'back': '<i class="fas fa-backward"></i>',
        'detail': '<i class="fas fa-angle-double-right"></i>',
        'delete': '<i class="fas fa-trash-alt"></i>',
        'delete_regular': '<i class="far fa-trash-alt"></i>',
        'update': '<i class="fas fa-edit"></i>',
        'category': '<i class="fas fa-box"></i>',
        'deal': '<i class="fas fa-balance-scale"></i>',
        'user': '<i class="fas fa-user-tie"></i>',
        'users': '<i class="fas fa-users"></i>',
        'market': '<i class="fas fa-compress-arrows-alt"></i>',
        'feedback': '<i class="fas fa-clipboard"></i>',
        'feedback_regular': '<i class="far fa-clipboard"></i>',
        'virtual': '<i class="fas fa-brain"></i>',
        'listing': '<i class="fas fa-file-alt"></i>',
        'bookmark': '<i class="fas fa-bookmark"></i>',
        'search': '<i class="fas fa-search"></i>',
        'message': '<i class="fas fa-comment"></i>',
        'message_regular': '<i class="far fa-comment"></i>',
        'chat': '<i class="fas fa-comments"></i>',
        'chat_regular': '<i class="far fa-comments"></i>',
        'location': '<i class="fas fa-map-marker-alt"></i>',
        'push': '<i class="fas fa-sort-up"></i>',
        'pull': '<i class="fas fa-sort-down"></i>',
        'lobby': '<i class="fas fa-couch"></i>',
    }


def default(request):
    """registered context processor"""
    ret = {}
    ret['version'] = VERSION
    ret['version_str'] = '.'.join((str(elem) for elem in VERSION))
    ret['name'] = NAME
    ret['symbols'] = SYMBOLS
    return ret
