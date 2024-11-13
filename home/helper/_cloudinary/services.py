from django.template.loader import get_template
from django.conf import settings

def get_cloudinary_image_object(instance, field_name="image", as_html=False, width=200):
    if not hasattr(instance, field_name):
        return None
    image_object=getattr(instance, field_name)
    if not image_object:
            return ""
    image_option={
        "width":width
    }
    if as_html:
          return image_object.image(**image_option)
    url=image_object.build_url(**image_option)
    print(url)
    return url

def get_cloudinary_video_object(instance,
                                field_name="video",
                                as_html=False,
                                width=None,
                                height=None,
                                sign_url=False,
                                fetch_format="auto",
                                quality='auto',
                                controls=True,
                                autoplay=True):
    if not hasattr(instance, field_name):
        return None
    video_object=getattr(instance, field_name)
    if not video_object:
            return ""
    video_option={
        "sign_url":sign_url,
        "fetch_format":fetch_format,
        "quality":quality,
        'controls':controls,
        'autoplay':autoplay
    }
    if width is not None:
          video_option['width']=width
    if height is not None:
          video_option['height']=height
    if height and width:
          video_option['crop']="limit"
    url=video_object.build_url(**video_option)
    print(url)
    cloud_name= settings.CLOUDINARY_NAME
    if as_html:
          template_name="videos/snippets/embed.html"
          tmpl = get_template(template_name)
          _html=tmpl.render({'video_url':url, 'cloud_name': cloud_name})
          return _html
    return url