from rest_framework import serializers

from .models import Inflow

class InflowSerializer(serializers.ModelSerializer):

   class Meta:
      model = Inflow 
      fields = ['supplier', 'product', 'quantity', 'description']