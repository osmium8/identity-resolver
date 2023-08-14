from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

from contact.models import Contact
from contact.serializers import IdentityRequestSerializer, IdentityResponseSerializer
from contact.helpers import aggregate_linked_contacts


class IdentityAPIView(APIView):
    """
    Fetch all linked contacts if exists or creates new
    """

    def post(self, request):
        serializer = IdentityRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_phone = serializer.validated_data["phoneNumber"]
        validated_email = serializer.validated_data["email"]

        if validated_email == "" and validated_phone == "":
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"Atleast one field is required among email and phoneNumber"},
            )

        if validated_phone and validated_email:
            primary_contact = Contact.objects.get_or_create_phone_email(
                validated_phone, validated_email
            )
        elif validated_phone:
            primary_contact = Contact.objects.get_or_create_phone(validated_phone)
        else:
            primary_contact = Contact.objects.get_or_create_email(validated_email)

        secondary_contacts = Contact.objects.filter(
            primary_contact__id=primary_contact.id
        )
        aggregated_contacts = aggregate_linked_contacts(
            primary_contact, secondary_contacts
        )

        data = {"contact": aggregated_contacts}
        response = IdentityResponseSerializer(data=data)
        response.is_valid(raise_exception=True)

        return Response(response.data, HTTP_200_OK)
