from rest_framework import serializers
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    line_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = "__all__"

    def get_line_total(self, obj):
        return obj.unit_price * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = '__all__'

    def get_total(self, obj):
        return sum(item.unit_price * item.quantity for item in obj.items.all())