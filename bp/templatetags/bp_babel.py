# vim: sw=4 ts=4 expandtab ai
#
# This file is part of Bender's Property
# Copyright (C) 2009 Bender's Property development team. All rights reserved.
#


from django import template
register = template.Library()
from babel.numbers import format_number, format_decimal, format_percent

@register.filter
def bp_numberfmt(value, locale='en'):
    return format_number(value, locale)

@register.filter
def bp_decimalfmt(value, locale='en'):
    return format_decimal(value, locale)

@register.filter
def bp_percentfmt(value, locale='en'):
    return format_percent(value, locale)
