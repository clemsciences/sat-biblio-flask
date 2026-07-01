"""
Vendored subset of arkpy (https://github.com/emsu/arkpy).

The upstream package on PyPI ships an obsolete ``ez_setup.py`` bootstrap that
tries to download setuptools over plain HTTP, which fails under modern pip
build isolation ("403: SSL is required"). Since we only rely on ``mint`` and
``validate`` — a tiny amount of pure-Python code — it is vendored here to
avoid the broken build. Original code is MIT-licensed.
"""

import random


digits = [str(i) for i in range(0, 10)]
xdigits = digits + ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'm', 'n',
                    'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z']


def mint(authority, template, prefix='', bare=True):
    """ mint an ARK within an authority according to a template
    """
    # random template: eeddeeddk
    #   e is an xdigit: 0123456789bcdfghjkmnpqrstvwxz
    #   d is a digit:   0123456789
    #   k is checkchar: special xdigit

    ark_parts = []

    if not bare:
        ark_parts.append('ark:/')

    ark_parts.append(authority)
    ark_parts.append('/')

    if prefix:
        ark_parts.append(prefix)

    ark_parts.append(_generate_name(template))

    ark = ''.join(ark_parts)

    if template[-1] == 'k':
        ark += _generate_check(ark)

    return ark


def _generate_name(template):
    name = ''
    for char in list(template):
        if char == 'e':
            name += random.choice(xdigits)
        elif char == 'd':
            name += random.choice(digits)
        else:
            continue
    return name


def _generate_check(ark):
    ark = _strip_scheme(ark)
    sum = 0
    position = 0
    for char in list(ark):
        try:
            ordinal = xdigits.index(char)
        except ValueError:
            ordinal = 0
        position += 1
        sum += (ordinal * position)
    return xdigits[sum % len(xdigits)]


def _strip_scheme(ark):
    if ark.startswith('ark:/'):
        return ark[5:]
    return ark


def validate(ark):
    return _generate_check(ark[:-1]) == ark[-1]
