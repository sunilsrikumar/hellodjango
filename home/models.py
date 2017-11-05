from __future__ import absolute_import, unicode_literals

from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
)

from wagtail.wagtailcore.models import Page

from wagtail.wagtailcore.models import Page, Collection
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet

@register_snippet
class People(ClusterableModel):
	first_name = models.CharField("First name", max_length=254)
	last_name = models.CharField("Last name", max_length=254)
	job_title = models.CharField("Job title", max_length=254)
	
	image = models.ForeignKey(
	    'wagtailimages.Image',
	    null=True,
	    blank=True,
	    on_delete=models.SET_NULL,
	    related_name='+'
	)

	panels = [
	    FieldPanel('first_name', classname="col6"),
	    FieldPanel('last_name', classname="col6"),
	    FieldPanel('job_title'),
	    ImageChooserPanel('image')
	]

	search_fields = Page.search_fields + [
	    index.SearchField('first_name'),
	    index.SearchField('last_name'),
	]

	@property
	def thumb_image(self):
	    try:
	        return self.image.get_rendition('fill-50x50').img_tag()
	    except:
	        return ''

	def __str__(self):
	    return '{} {}'.format(self.first_name, self.last_name)

	class Meta:
	    verbose_name = 'Person'
	    verbose_name_plural = 'People'


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]