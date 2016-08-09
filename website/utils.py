
from collections import OrderedDict
from .models import Photo


def get_ordered_photos(photos_order):
    """
    It returns photos src by id
    pass any objects order
    """
    photos = Photo.objects.filter(id__in=photos_order.values())
    photo_src = {}

    def src_to_photo(x):
        photo_src.update({str(x.id): x.src})

    for photo in photos:
        src_to_photo(photo)

    ordered = []
    for key in sorted([int(key) for key in photos_order.keys()]):
        ordered.append({
                'id': photos_order[str(key)],
                'src': photo_src[photos_order[str(key)]],
                'order': str(key)})
    return ordered
