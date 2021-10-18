from django import template
from django.utils.safestring import mark_safe

register = template.Library()


# 将字符串过滤成列表
@register.filter
def to_list(value):
    return eval(value)