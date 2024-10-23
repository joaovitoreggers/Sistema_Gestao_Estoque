from rest_framework import serializers

from .models import ServiceProvision

class ServiceProvisionSerializer(serializers.ModelSerializer):

   class Meta:
      model = ServiceProvision
      fields = '__all__'