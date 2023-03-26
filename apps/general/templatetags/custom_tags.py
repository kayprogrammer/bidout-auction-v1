from django import template
from apps.general.models import SiteDetail

register = template.Library()


@register.inclusion_tag("footer.html", takes_context=True)
def footer(context):
    site = SiteDetail.objects.get()
    return {"site": site}
