from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from home.models import People, FooterText


class PeopleModelAdmin(ModelAdmin):
    model = People
    menu_label = 'People'  # ditch this to use verbose_name_plural from model
    menu_icon = 'fa-users'  # change as required
    list_display = ('first_name', 'last_name', 'job_title', 'thumb_image')


class FooterTextAdmin(ModelAdmin):
    model = FooterText