from django.db import models
from cloudinary.models import CloudinaryField
from django.utils.text import slugify
import helper
import uuid

helper.cloudinary_init()

class AccessRequirement(models.TextChoices):
    ANYONE = 'any', 'Anyone'
    EMAILREQUIRED = 'email', 'Email required'

class PublishStatus(models.TextChoices):
    PUBLISHED = 'pub', 'Published'
    COMMINGSOON = 'cs', 'Comming soon'
    DRAFT = 'dr', 'Draft'

def get_public_id(instance, *args, **kwargs):
    title=instance.title
    unique_id=str(uuid.uuid4()).replace("-","")
    if title is None:
        return unique_id
    slug=slugify(title)
    return f"{slug}-{unique_id[:5]}"
    

def get_public_id_prefix(instance, *args, **kwargs):
    if hasattr(instance, 'path'):
        path=instance.path
        if path.startswith("/"):
            path=path[1:]
        if path.endswith('/'):
            path=path[:-1]
        return path
    public_id=instance.public_id
    model_class=instance.__class__
    model_name=model_class.__name__
    model_name_slug=slugify(model_name)
    if not public_id:
        return f'{model_name_slug}'
    return f"{model_name_slug}/{public_id}"

def get_display_name(instance):
    if hasattr(instance, 'get_display_name'):
        return instance.get_display_name()
    elif hasattr(instance, 'title'):
        return instance.title
    model_class=instance.__class__
    model_name=model_class.__name__
    return f"{model_name} upload"

    
def handle_upload(instance,filename):
	return f"{filename}"

class course(models.Model):
    title=models.CharField(max_length=70)
    description = models.TextField(blank=True, null=True)
    public_id = models.CharField(max_length=150, null=True, blank=True, db_index=True)
    # image=models.ImageField(upload_to=handle_upload, null=True, blank=True)
    image=CloudinaryField("image", null=True, public_id_prefix=get_public_id_prefix,
                          display_name=get_display_name, tags=["course"])
    access=models.CharField(max_length=15, choices=AccessRequirement.choices, default=AccessRequirement.ANYONE)
    status=models.CharField(max_length=15, choices=PublishStatus.choices, default=PublishStatus.DRAFT)

    def save(self, *args, **kwargs):
        #before save
        if self.public_id=="" or self.public_id is None:
            self.public_id=get_public_id(self)
        super().save(*args, **kwargs)
        #after save

    @property
    def path(self):
        return f"/courses/{self.public_id}"

    @property
    def isPubished(self):
        return self.status == PublishStatus.PUBLISHED
    
    @property
    def image_admin(self):
        return helper.get_cloudinary_image_object(self, 
                                           field_name="image", 
                                           as_html=False, 
                                           width=500)
    
    def set_image_thumbnail(self, as_html=False):
        return helper.get_cloudinary_image_object(self,
                                                  field_name="image",
                                                  as_html=as_html,
                                                  width=200)
    
    def get_display_name(self):
        return f"{self.title}-course"
    
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
    thumbnail=CloudinaryField("image", blank=True, null=True, public_id_prefix=get_public_id_prefix,
                          display_name=get_display_name, tags=["Thumbnail"])
    video=CloudinaryField("video", blank=True, null=True,public_id_prefix=get_public_id_prefix,
                          display_name=get_display_name, resource_type="video",
                           type='private', tags=['video'])
    description = models.TextField(blank=True, null=True)
    public_id = models.CharField(max_length=150, null=True, blank=True, db_index=True)
    order = models.IntegerField(default=0)
    canPreview = models.BooleanField(default=False, help_text="For users who dont have access")
    status=models.CharField(max_length=15, choices=PublishStatus.choices, default=PublishStatus.PUBLISHED)
    updated = models.DateTimeField(auto_now=True) 
    created = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):
        #before save
        if self.public_id=="" or self.public_id is None:
            self.public_id=get_public_id(self)
        super().save(*args, **kwargs)
        #after save

    class Meta:
        ordering = ['order', "-updated"]

    @property
    def path(self):
        course_path=self.course.path
        if course_path.endswith("/"):
            course_path = course_path[ :-1]
        return f"{course_path}/lessons/{self.public_id}"
    
    def get_display_name(self):
        return f"{self.title}-{self.course.get_display_name()}"
    
    @property
    def is_comming_soon(self):
        self.status = PublishStatus.COMMINGSOON

    @property
    def has_video(self):
        return self.video is not None
    
    @property
    def requires_email(self):
        return self.course.access == AccessRequirement.EMAILREQUIRED