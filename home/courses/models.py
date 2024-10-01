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

class course(models.Model):
    Title=models.CharField(max_length=70)
    Description = models.TextField(blank=True, null=True)
    #image=
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