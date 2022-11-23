from django.utils.text import slugify
import pathlib
import uuid
import datetime

def image_name_path_handler(instance, filename):
    new_uuid = str(uuid.uuid4())
    
    app_name = instance._meta.app_label
    model_class_name = instance._meta.model_name
    
    fpath = pathlib.Path(filename)
    pure_filename = str(fpath.stem)

    return f"{app_name}/{model_class_name}/{pure_filename}-{new_uuid}{fpath.suffix}"

def slugify_title(instance, save=False, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    qs = instance.__class__.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        # auto generate new slug

        todays_date = str(datetime.date.today().strftime("%d-%m-%Y"))
        short_hash = str(uuid.uuid4())[:6]

        slug = f"{slug}-{todays_date}-{short_hash}"
        return slugify_title(instance, save=save, new_slug=slug)

    instance.slug = slug
    if save:
        instance.save()
    return instance