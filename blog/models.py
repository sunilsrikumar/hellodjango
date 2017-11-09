# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.db import models
from django.shortcuts import redirect, render

from django.contrib import messages

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase

from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel 
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel


class BlogPeopleRelationship(Orderable, models.Model):
    page = ParentalKey(
        'BlogPage', related_name='blog_person_relationship'
    )
    people = models.ForeignKey(
        'home.People', related_name='person_blog_relationship'
    )
    panels = [
        SnippetChooserPanel('people')
    ]


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        context = super(BlogIndexPage, self).get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='tagged_items')

class BlogTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super(BlogTagIndexPage, self).get_context(request)
        context['blogpages'] = blogpages
        return context
        

class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Blog information"),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]



class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]

@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'blog categories'
