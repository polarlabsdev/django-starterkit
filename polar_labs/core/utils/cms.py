from django.utils.safestring import mark_safe


THUMB_IMAGE_HEIGHT = 150
THUMB_IMAGE_HEIGHT_TINY = 50


def cms_image_preview(image, tiny=False):
  if not image:
    return mark_safe(f'<p>No image uploaded yet.</p>')  # nosec

  return mark_safe(  # nosec
    f'<img src="{image.url}" '
    f'height="{THUMB_IMAGE_HEIGHT_TINY if tiny else THUMB_IMAGE_HEIGHT}" '
    f'alt="{image.name} (Refresh if not displaying)"/>'
  )
