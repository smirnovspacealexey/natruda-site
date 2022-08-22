from django.db import models
from apps.tools.slugify import slugify


class Signboard(models.Model):
    slug = models.CharField(max_length=200)
    image = models.ImageField('image', upload_to='signboards')
    active = models.BooleanField('active', default=True)

    def __str__(self):
        return self.slug

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.slug)
        if self.active:
            type(self).objects.exclude(pk=self.pk).filter(slug=self.slug).update(active=False)
        super().save()
