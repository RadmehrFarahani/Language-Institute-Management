from django import template
from ..models import *

register=template.Library()

@register.simple_tag
def total_message():
  return Contact.objects.filter().count()
