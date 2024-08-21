# serializers.py
from rest_framework import serializers
from home.models import Book ### to be replaced by my models

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # Or specify fields you want to include
