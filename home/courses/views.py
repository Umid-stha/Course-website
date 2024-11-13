from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from . import services
import helper

# Create your views here.
def course_list(request):
    qs = services.get_published_courses()
    # return JsonResponse({"data":[x.path for x in qs]})
    context = {
        "object":qs
    }
    return render(request, "courses/list.html", context)

def course_detail(request, id):
    course_object = services.get_course_detail(id)
    if course_object is None:
        raise Http404
    lessons_qs = course_object.lesson_set.all()
    context = {
        "object":course_object,
        "lessons_qs":lessons_qs
    }
    # return JsonResponse({"data":course_object.title, "lesson_id":[i.path for i in lessons_qs]})
    return render(request, "courses/detail.html", context)

def lesson_detail(request, c_id, l_id):
    lesson_object = services.get_lesson_detail(c_id, l_id)
    if lesson_object is None:
        raise Http404
    email_id = request.session.get("email_id")
    if lesson_object.requires_email and not email_id:
        print(request.path)
        request.session['next_url']=request.path
        return render(request, "courses/email-required.html", {})
    template_name = "courses/lesson-comming-soon.html"
    context = {
        "object":lesson_object,
    }
    if not lesson_object.is_comming_soon and lesson_object.has_video:
        template_name="courses/lesson.html"
        """Lesson is published, go forward"""
        get_embed_video=helper.get_cloudinary_video_object(
            lesson_object,
            field_name="video",
            as_html=True, 
            width=1250
            )
        context['video']=get_embed_video
    # return JsonResponse({"data":lesson_object.title})
    return render(request, template_name, context)