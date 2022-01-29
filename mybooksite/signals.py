from django.db.models.signals import pre_save
from django.dispatch import receiver
from io import BytesIO
from django.core.files.base import ContentFile

from PIL import Image
from mybooksite.models import Book

@receiver(pre_save, sender=Book)
def create_thumbnail(sender, instance, **kwargs):
    if instance.img:
        img = Image.open(instance.img)
        size = (200,200)

        img.thumbnail(size, Image.ANTIALIAS)

        temp_thumb = BytesIO()

        img.save(temp_thumb, "JPEG")

        temp_thumb.seek(0)
        
        # set save=False, otherwise it will run in an infinite loop
        instance.thumbnail.save(
            instance.img.name,
            ContentFile(temp_thumb.read()),
            save=False
        )
        temp_thumb.close()
    else:
        pass

        
        
       
        