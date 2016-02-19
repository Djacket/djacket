from django import template

register = template.Library()


@register.filter(name='obj_name')
def obj_name(value, arg):
    """
        Returns object name from an absolute path seperated by provided 'arg'.

        e.g.
            For a path seperated by '/' like '/pa/th/to/file.ext' it returns 'file.ext'.
    """

    return value.split(arg)[-1]


@register.filter(name='obj_ext')
def obj_ext(value):
    """
        Returns extention of an object.

        e.g.
            For an object with name 'somecode.py' it returns 'py'.
    """

    return value.split('.')[-1]


@register.filter(name='ellipsize')
def ellipsize(value, limit=32):
    """
    Truncates a string after a given number of chars keeping whole words.

    Usage:
        {{ string|ellipsize }}
        {{ string|ellipsize:50 }}
    """

    if len(value) <= limit:
        return value
    else:
        value = value[:limit]
        words = value.split(' ')[:-1]
        return ' '.join(words) + '...'
