from django import template
from apps.main.models import Point

register = template.Library()


@register.simple_tag(name='get_points')
def get_points():
    print('---')
    print(Point.objects.all())
    return Point.objects.all()



