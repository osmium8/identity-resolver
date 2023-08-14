from django.db import models


class ContactManager(models.Manager):
    def get_or_create_phone_email(self, phone_number: str, email: str) -> object:
        """
        Returns the primary contact for given phone_number/email
        after performing identity resolution

        Creates secondary contacts for new phone_number/email

        Creates new primary contact if identity is not resolved
        """
        contact_phone = Contact.objects.filter(phone_number=phone_number).first()
        contact_email = Contact.objects.filter(email=email).first()

        if contact_phone and contact_email:
            primary_phone = contact_phone.get_primary()
            primary_email = contact_email.get_primary()
            if primary_phone.id != primary_email.id:
                # Conflict! Primary contact must be unique for an individual
                return self.merge_primary(primary_phone, primary_email)
            else:
                return primary_phone

        elif contact_phone:
            primary_contact = contact_phone.get_primary()
            self.create_secondary_contact(phone_number, email, primary_contact)

        elif contact_email:
            primary_contact = contact_email.get_primary()
            self.create_secondary_contact(phone_number, email, primary_contact)

        else:
            primary_contact = Contact.objects.create(
                phone_number=phone_number,
                email=email,
                link_precedence=Contact.LinkPrecedence.PRIMARY,
            )

        return primary_contact

    def create_secondary_contact(
        self, phone_number: str, email: str, primary_contact: object
    ):
        return Contact.objects.create(
            phone_number=phone_number,
            email=email,
            link_precedence=Contact.LinkPrecedence.SECONDARY,
            primary_contact=primary_contact,
        )

    def merge_primary(self, primary_1, primary_2):
        """
        Merge two given primary contacts
        Older contact is preserved as primary

        Returns:
            Contact: primary contact
        """
        if primary_1.created_at < primary_2.created_at:
            self.convert_to_secondary(primary_2, primary_1)
            return primary_1
        else:
            self.convert_to_secondary(primary_1, primary_2)
            return primary_2

    def convert_to_secondary(self, old_primary_contact, new_primary_contact):
        """
        Convert a given primary contact to secondary contact

        Args:
            old_primary_contact (Contact): The primary contact to be marked secondary
            new_primary_contact (Contact): The primary contact to be linked
        """

        # Mark as secondary
        old_primary_contact.link_precedence = Contact.LinkPrecedence.SECONDARY
        old_primary_contact.primary_contact = new_primary_contact
        old_primary_contact.save()

        # Update children
        Contact.objects.filter(primary_contact=old_primary_contact).update(
            primary_contact=new_primary_contact
        )


class Contact(models.Model):
    class LinkPrecedence(models.TextChoices):
        PRIMARY = "primary", "primary"
        SECONDARY = "secondary", "secondary"

    phone_number = models.CharField(
        max_length=15, db_index=True, unique=False, null=True
    )
    email = models.EmailField(db_index=True, unique=False, null=True)
    primary_contact = models.ForeignKey(  # linked_id
        "contact.Contact", on_delete=models.CASCADE, null=True
    )
    link_precedence = models.CharField(
        max_length=9,
        choices=LinkPrecedence.choices,
        default=LinkPrecedence.PRIMARY,
        editable=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    deleted_at = models.DateTimeField(null=True, editable=False)
    objects = ContactManager()

    def get_primary(self):
        if self.link_precedence == self.LinkPrecedence.PRIMARY:
            return self
        else:
            return self.primary_contact

    def __str__(self):
        return (
            self.phone_number
            if self.phone_number
            else "[null]" + ", " + self.email
            if self.email
            else "[null]"
        )

    class Meta:
        unique_together = ("phone_number", "email")
