from datetime import datetime

from django.core.mail import EmailMessage
from django.db.models import F
from django.utils.datastructures import MultiValueDictKeyError

from rest_framework import parsers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from back_end import settings
from documents.contract_docx import check
from product.models import (
    Category,
    Product,
    DesiredList
)
from product.permissions import (
    IsStaffOrReadOnly,
    IsStaffOrOwnerOrShopOrReadOnly
)
from product.serializer import (
    CategoryModelSerializer,
    ProductModelSerializer,
    DesiredListModelSerializer
)
from product.services_view import create_product_image, update_product


class CategoryViewSet(ModelViewSet):
    """View для категорий"""

    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = (IsStaffOrReadOnly,)


class ProductViewSet(ModelViewSet):
    """View для продуктов"""

    queryset = Product.objects.all().annotate(
        price_with_discount=F('price') - F('discount')
    )
    serializer_class = ProductModelSerializer
    permission_classes = (IsStaffOrOwnerOrShopOrReadOnly,)
    parser_classes = (parsers.MultiPartParser, parsers.JSONParser)

    def create(self, request, *args, **kwargs):
        try:
            request.data['images']
        except MultiValueDictKeyError:
            return Response(data={'images': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)
        return super(ProductViewSet, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()
        create_product_image(images=self.request.data.pop('images'))

    def update(self, request, *args, **kwargs):
        try:
            self.request.data['images']
        except MultiValueDictKeyError:
            pass
        else:
            images = self.request.data.pop('images')
            count = update_product(images=images,
                                   product_id=kwargs['pk'])
            if len(images) != count:
                for counter, image in enumerate(images):
                    if counter <= count:
                        pass
                    else:
                        create_product_image(images=images)
        return super(ProductViewSet, self).update(request, *args, **kwargs)


class DesiredListViewSet(ModelViewSet):
    """View для списка желаемого"""

    queryset = DesiredList.objects.all()
    serializer_class = DesiredListModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(user=self.request.user)
        return query_set

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()
