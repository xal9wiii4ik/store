from product.models import Product, ProductImage
from product.serializer import ProductImageModelSerializer


def create_product_image(images: list) -> None:
    """Создание фотографий продукта"""

    for image in images:
        if _get_validation_of_serializer(serializer=ProductImageModelSerializer,
                                         product_pk=Product.objects.latest('id').id,
                                         image=image):
            ProductImage.objects.create(product=Product.objects.latest('id'),
                                        image=image)


def update_product(images: list, product_id: int) -> int:
    pi = ProductImage.objects.filter(product=product_id)
    counter = 0
    for count, image in enumerate(images):
        if _get_validation_of_serializer(serializer=ProductImageModelSerializer,
                                         product_pk=product_id,
                                         image=image):
            if count < len(pi):
                pi[counter].image = image
                pi[counter].save()
            counter += 1
    counter -= 1
    return counter - 1


def _get_validation_of_serializer(serializer, product_pk, image) -> bool:
    """Вовзращает валидацию сериалайзера"""

    data = {
        'product': product_pk,
        'image': image
    }
    new_serializer = serializer(data=data)
    if new_serializer.is_valid():
        return True
    return False
