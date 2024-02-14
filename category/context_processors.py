#Context processors in Django allow you to make certain data available globally to all templates.
# for displaying all categories on navbar
#The menu_links context processor ensures that the category links are available in all templates.
from .models import Category


def menu_links(request):
    links=Category.objects.all()
    return dict(links=links)