from django import template
from mychurch.models import LSCH007M

register = template.Library()

@register.inclusion_tag('mychurch/menu.html')
def side_menu(*args, **kwargs):
    #To-Do : request.user.church_no로 대체
    menu_list = LSCH007M.objects.filter(
            church_no=1
        ).order_by('menu_order')
    return {'menu_list':menu_list}
