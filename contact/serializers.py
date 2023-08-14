from rest_framework import serializers
from django.core.validators import RegexValidator


class IdentityRequestSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField(required=False, default='', allow_blank=True, max_length=15, validators=[RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format '+123456789'. Up to 15 digits allowed."
    ),])
    email = serializers.EmailField(required=False, default='', allow_blank=True)

    class Meta:
        fields = ('phone_number', 'email')
        extra_kwargs = {
            'phone_number': {'required': False},
            'email': {'required': False}
        }


class AggregatedContactsSerializer(serializers.Serializer):
    primaryContactId = serializers.IntegerField()
    emails = serializers.ListField()
    phoneNumbers = serializers.ListField()
    secondaryContactIds = serializers.ListField()


class IdentityResponseSerializer(serializers.Serializer):
    contact = AggregatedContactsSerializer(many=False)
