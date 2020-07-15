from config.settings import VERSION, NAME


SYMBOLS = {
        # Basic symbols
        'close': '<i class="fas fa-times"></i>',
        'back': '<i class="fas fa-backward"></i>',
        'forward': '<i class="fas fa-forward"></i>',
        'detail': '<i class="fas fa-angle-double-right"></i>',
        'delete': '<i class="fas fa-trash-alt"></i>',
        'delete_regular': '<i class="far fa-trash-alt"></i>',
        'deleted': '<i class="fas fa-minus-circle"></i>',
        'update': '<i class="fas fa-edit"></i>',
        'bookmark': '<i class="fas fa-bookmark"></i>',
        'seen': '<i class="fas fa-eye"></i>',
        'unseen': '<i class="fas fa-eye-slash"></i>',
        'hidden': '<i class="fas fa-smog"></i>',

        # Model Objects
        'search': '<i class="fas fa-search"></i>',
        'bid': '<i class="fas fa-gavel"></i>',
        'category': '<i class="fas fa-box"></i>',
        'deal': '<i class="fas fa-balance-scale"></i>',
        'user': '<i class="fas fa-user-tie"></i>',
        'users': '<i class="fas fa-users"></i>',
        'market': '<i class="fas fa-compress-arrows-alt"></i>',
        'feedback': '<i class="fas fa-star"></i>',
        'virtual': '<i class="fas fa-brain"></i>',
        'listing': '<i class="fas fa-file-alt"></i>',
        'message': '<i class="fas fa-comment"></i>',
        'message_regular': '<i class="far fa-comment"></i>',
        'chat': '<i class="fas fa-comments"></i>',
        'chat_regular': '<i class="far fa-comments"></i>',
        'location': '<i class="fas fa-map-marker-alt"></i>',
        'push': '<i class="fas fa-sort-up"></i>',
        'pull': '<i class="fas fa-sort-down"></i>',
        'lobby': '<i class="fas fa-couch"></i>',
        'calculator': '<i class="fas fa-calculator"></i>',
    }


def default(request):
    """registered context processor"""
    context = {}
    context['name'] = NAME
    context['symbols'] = SYMBOLS
    context['version'] = VERSION
    context['version_str'] = '.'.join((str(elem) for elem in VERSION))
    return context
