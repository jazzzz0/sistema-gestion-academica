from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Devuelve la URL actual con los parámetros GET actualizados.
    Ejemplo de uso: <a href="?{% param_replace page=page_obj.next_page_number %}">
    Mantiene filtros activos como ?search=juan y solo cambia la página.
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()
