from django.db import models

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

    def get_primary(self):
        if self.link_precedence == self.LinkPrecedence.PRIMARY:
            return self
        else:
            return self.primary_contact

    def __str__(self):
        return self.phone_number if self.phone_number else 'NA' + ', ' + self.email if self.email else 'NA'

    class Meta:
        unique_together = ("phone_number", "email")
