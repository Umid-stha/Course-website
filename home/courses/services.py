from .models import course, PublishStatus, lesson

def get_published_courses():
    return course.objects.filter(status=PublishStatus.PUBLISHED)

def get_course_detail(c_id=None):
    if c_id is None: 
        return None
    try:
        obj = course.objects.get(status=PublishStatus.PUBLISHED, public_id=c_id)
    except:
        pass
    return obj

def get_lesson_detail(course_obj):
    lessons = lesson.objects.none()
    if not isinstance(course_obj, course):
        return lessons
    lessons = course_obj.objects.filter(course__status=PublishStatus.PUBLISHED, status__in=[PublishStatus.PUBLISHED, PublishStatus.COMMINGSOON])

def get_lesson_detail(c_id=None, l_id=None):
    if l_id is None: 
        return None
    try:
        obj = lesson.objects.get(course__public_id=c_id, course__status= PublishStatus.PUBLISHED, status__in=[PublishStatus.PUBLISHED, PublishStatus.COMMINGSOON], public_id=l_id)
    except:
        pass
    return obj
