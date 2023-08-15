from contact.models import Contact

def aggregate_linked_contacts(primary_contact: Contact, secondary_contacts: list):
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

    # move primary phone and primary email to the first position
    phoneNumbers.discard(primary_contact.phone_number)
    emails.discard(primary_contact.email)
    
    phoneNumbers = list(phoneNumbers)
    emails = list(emails)

    if primary_contact.phone_number:
        phoneNumbers.insert(0, primary_contact.phone_number)
    
    if primary_contact.email:
        emails.insert(0, primary_contact.email)

    return {
        "primaryContactId": primaryContactId,
        "emails": emails,
        "phoneNumbers": phoneNumbers,
        "secondaryContactIds": secondaryContactIds
    }