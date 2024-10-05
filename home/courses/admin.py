from django.contrib import admin
from .models import course, lesson
from django.utils.html import format_html
from cloudinary import CloudinaryImage

class lessonInline(admin.StackedInline):
    model= lesson
    extra = 0
    readonly_fields=["updated","created"]

@admin.register(course)
class CourseAdmin(admin.ModelAdmin):
    inlines= [lessonInline]
    list_display=["title", "status", "access"]
    list_filter=["access", "status"]
    fields=["title", "description", "image", "status", "access", "display_img"]
    readonly_fields= ["display_img"]

    def display_img(self, obj, *args, **kwargs):
        url=obj.image_admin
        # cloudinary_id = str(obj.image)
        # print(cloudinary_id)
        # img_html=CloudinaryImage(cloudinary_id).image(width=300)
        return format_html(f'<img src="{url}" >')
    display_img.short_description="Image"