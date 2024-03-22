from django.db import models
import uuid


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def save(self, *args, **kwargs):
        self.full_clean()  # validate fields before save
        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class BaseUUIDModel(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # type: ignore

    class Meta:
        abstract = True
