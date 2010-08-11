from datetime import datetime

from django.db import models
from django.core.urlresolvers import reverse

from uuidfield import UUIDField
from jsonfield import JSONField


class TokenManager(models.Manager):
    def create(self, token_type, data, lifetime=None):
        obj = self.model()
        obj.token_type = token_type
        obj.data = data
        if lifetime is not None:
            obj.valid_to = datetime.now() + lifetime
        return obj


class Token(models.Model):
    objects = TokenManager()

    code = UUIDField()
    valid_to = models.DateTimeField(null=True, blank=True)
    token_type = models.CharField(max_length=40)
    data = JSONField()

    @property
    def full_code(self):
        return str(self.id) + '-' + self.code

    def __unicode__(self):
        return u'%s - %s' % (self.token_type, self.full_code)

    @property
    def url(self):
        return reverse('token_handle', args=[self.full_code])
