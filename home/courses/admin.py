from django.contrib import admin
from .models import course, lesson
from django.utils.html import format_html
from cloudinary import CloudinaryImage
import helper


class lessonInline(admin.StackedInline):
    model= lesson
    extra = 0
    readonly_fields=["updated","created", "public_id", "display_img", "display_video"]
    def display_img(self, obj, *args, **kwargs):
        url=helper.get_cloudinary_image_object(obj, field_name="thumbnail",as_html=False, width=500)
        return format_html(f'<img src="{url}" >')
    display_img.short_description="Image"
    def display_video(self, obj, *args, **kwargs):
        get_html_embed_video=helper.get_cloudinary_video_object(obj, field_name="video",as_html=True, width=550)
        return  get_html_embed_video
    display_video.short_description="Video"

@admin.register(course)
class CourseAdmin(admin.ModelAdmin):
    inlines= [lessonInline]
    list_display=["title", "status", "access"]
    list_filter=["access", "status"]
    fields=["public_id", "title", "description", "image", "status", "access", "display_img"]
    readonly_fields= ["display_img", "public_id"]

    def display_img(self, obj, *args, **kwargs):
        url=obj.image_admin
        # cloudinary_id = str(obj.image)
        # print(cloudinary_id)
        # img_html=CloudinaryImage(cloudinary_id).image(width=300)
        return format_html(f'<img src="{url}" >')
    display_img.short_description="Image"