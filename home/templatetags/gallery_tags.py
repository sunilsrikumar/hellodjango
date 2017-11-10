from django import template

from wagtail.wagtailimages.models import Image

register = template.Library()

@register.inclusion_tag('tags/gallery.html', takes_context=True)
def gallery(context, gallery):
    images = Image.objects.filter(collection=gallery)

    return {
        'images': images,
        'request': context['request'],
    }