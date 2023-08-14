from contact.models import Contact

def aggregate_linked_contacts(primary_contact: Contact, secondary_contacts: list[Contact]):
    """
    Returns: dictionary containing all emails and phoneNumbers
        {
            "primaryContactId": 0,
            "emails": ["string"],
            "phoneNumbers": ["string"],
            "secondaryContactIds": ["string"]
        }
    """
    primaryContactId = primary_contact.id
    emails = set([primary_contact.email]) if primary_contact.email else set()
    phoneNumbers = set([primary_contact.phone_number]) if primary_contact.phone_number else set()

    secondaryContactIds = set()
    for contact in secondary_contacts:
        secondaryContactIds.add(contact.id)
        if (contact.email):
            emails.add(contact.email)
        if (contact.phone_number):
            phoneNumbers.add(contact.phone_number)

    return {
        "primaryContactId": primaryContactId,
        "emails": emails,
        "phoneNumbers": phoneNumbers,
        "secondaryContactIds": secondaryContactIds
    }