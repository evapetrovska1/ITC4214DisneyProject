from django import template
from django.db.models import Avg

register = template.Library()

@register.filter
def avg_rating(ratings_queryset):
    """Calculate average rating from a ratings queryset"""
    if ratings_queryset.exists():
        return ratings_queryset.aggregate(Avg('stars'))['stars__avg']
    return 0

@register.filter
def get_user_rating(ratings_queryset, user):
    """Get user's rating for a product"""
    try:
        return ratings_queryset.filter(user=user).first()
    except:
        return None