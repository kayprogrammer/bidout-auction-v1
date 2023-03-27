from django import template
from django.db.models import Q
from django.utils.safestring import mark_safe
from apps.listings.models import WatchList

register = template.Library()


@register.filter
def modify_watchlist_button(listing, request):
    user = request.user
    watch_list = WatchList.objects.filter(
        Q(user_id=user.pk, session_key=None) | Q(user=None, session_key=user)
    ).filter(listing=listing)
    if watch_list.exists():
        return mark_safe(
            f'<i role="button" data-action="remove" data-listing-slug="{listing.slug}" class="fa fa-2x text-danger fa-solid fa-heart me-3 watchlist-btn"></i>'
        )
    return mark_safe(
        f'<i role="button" data-action="add" data-listing-slug="{listing.slug}" class="fa fa-2x text-secondary fa-solid fa-heart me-3 watchlist-btn"></i>'
    )
