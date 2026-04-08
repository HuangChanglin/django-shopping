from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from .models import CartItem
from .serializers import CartItemSerializer, CartItemUpdateSerializer, CartItemDeleteSerializer


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update':
            return CartItemUpdateSerializer
        return CartItemSerializer

    @action(detail=False, methods=['get'])
    def summary(self, request):
        cart_items = self.get_queryset()
        total_count = cart_items.count()
        total_amount = cart_items.aggregate(
            total=Sum('product__price' * 'quantity')
        )['total'] or 0
        total_quantity = cart_items.aggregate(
            total=Sum('quantity')
        )['total'] or 0
        
        return Response({
            'total_count': total_count,
            'total_quantity': total_quantity,
            'total_amount': total_amount
        })

    @action(detail=False, methods=['post'])
    def clear(self, request):
        self.get_queryset().delete()
        return Response({'message': '购物车已清空'})

    @action(detail=False, methods=['post'])
    def batch_delete(self, request):
        serializer = CartItemDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        ids = serializer.validated_data['ids']
        deleted, _ = self.get_queryset().filter(id__in=ids).delete()
        
        return Response({'message': f'已删除 {deleted} 个商品'})
