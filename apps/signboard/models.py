from django.db import models
from apps.tools.slugify import slugify
from django.utils.html import format_html
from shawarma_site.settings import HOST


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

    @property
    def signboard_url(self):

        html = f'''
        <input size="35" type="text" value="{HOST + 'signboards/' + self.slug}" id="url-{self.pk}">
        <button class="default" onclick="copyText('url-{self.pk}')">copy</button>
        '''
        return format_html(html)

