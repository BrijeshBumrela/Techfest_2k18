from django import template

register = template.Library()


@register.filter
def strtoslug(incoming):
    """
    Converts an incoming string to slug. Also converts full to lowercase. Used to get event url
    :param incoming: Incoming string that is full event name
    :return: slug form of the same string
    """
    incoming = str(incoming)
    incoming = incoming.lower()
    incoming = incoming.replace(' ', '-')
    return incoming
