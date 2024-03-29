from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['id', 'product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'products', 'positions']

    def create(self, validated_data):

        positions = validated_data.pop('positions')

        stock = super().create(validated_data)
        for position in positions:
            stock_product = StockProduct(stock=stock, **position)
            stock_product.save()
        return stock

    def update(self, instance, validated_data):

        positions = validated_data.pop('positions')

        stock = super().update(instance, validated_data)
        stock_products = StockProduct.objects.all().filter(stock=stock)
        for position in positions:
            stock_products.update_or_create(
                stock=stock,
                product=position['product'],
                defaults={
                        'price': position['price'],
                        'quantity': position['quantity']
                        }
                    )

        return stock
