from django.db import models
from cloudinary.models import CloudinaryField
import helper

helper.cloudinary_init()

class AccessRequirement(models.TextChoices):
    ANYONE = 'any', 'Anyone'
    EMAILREQUIRED = 'email', 'Email required'

class PublishStatus(models.TextChoices):
    PUBLISHED = 'pub', 'Published'
    COMMINGSOON = 'cs', 'Comming soon'
    DRAFT = 'dr', 'Draft'
    
def handle_upload(instance,filename):
	return f"{filename}"

class course(models.Model):
    title=models.CharField(max_length=70)
    description = models.TextField(blank=True, null=True)
    # image=models.ImageField(upload_to=handle_upload, null=True, blank=True)
    image=CloudinaryField("image", null=True)
    access=models.CharField(max_length=15, choices=AccessRequirement.choices, default=AccessRequirement.ANYONE)
    status=models.CharField(max_length=15, choices=PublishStatus.choices, default=PublishStatus.DRAFT)

    @property
    def isPubished(self):
        return self.status == PublishStatus.PUBLISHED
    
    @property
    def image_admin(self):
         if not self.image:
            return ""
         image_option={
              "width":500
         }
         url=self.image.build_url(**image_option)
         return url
    
    def set_image_thumbnail(self, as_html=False):
         if not self.image:
            return ""
         image_option={
              "width":300
         }
         if as_html:
             return self.image.image(**image_option)
         url=self.image.build_url(**image_option)
         return url
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

"""
	- Lessons
		- Title
		- Description
		- Video
		- Status: Published, Coming Soon, Draft
"""
class lesson(models.Model):
    course=models.ForeignKey(course, on_delete=models.CASCADE)
    title=models.CharField(max_length=70)
    thumbnail=CloudinaryField("image", blank=True, null=True)
    video=CloudinaryField("video", blank=True, null=True, resource_type="video")
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)
    canPreview = models.BooleanField(default=False, help_text="For users who dont have access")
    status=models.CharField(max_length=15, choices=PublishStatus.choices, default=PublishStatus.PUBLISHED)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['order', "-updated"]