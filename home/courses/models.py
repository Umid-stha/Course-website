from django.db import models

"""
    - Courses:
	- Title
	- Description
	- Thumbnail/Image
	- Access:
		- Anyone
		- Email required
        - Purchase required
		- User required (n/a)
	- Status: 
		- Published
		- Coming Soon
		- Draft
"""
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
    image=models.ImageField(upload_to=handle_upload, null=True, blank=True)
    access=models.CharField(max_length=15, choices=AccessRequirement.choices, default=AccessRequirement.ANYONE)
    status=models.CharField(max_length=15, choices=PublishStatus.choices, default=PublishStatus.DRAFT)

    @property
    def isPubished(self):
        return self.status == PublishStatus.PUBLISHED

"""
	- Lessons
		- Title
		- Description
		- Video
		- Status: Published, Coming Soon, Draft
"""