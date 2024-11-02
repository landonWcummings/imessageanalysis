import csv
import vobject
import re

def clean_phone_number(phone):
    """Remove spaces, hyphens, and parentheses from the phone number and add '1' if too short."""
    # Remove unwanted characters
    cleaned_phone = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Add '1' in front if the cleaned number is less than 10 digits
    if len(cleaned_phone) <= 10:
        cleaned_phone = '1' + cleaned_phone
    
    return cleaned_phone

def vcf_to_csv(vcf_file_path, csv_file_path='contacts.csv'):
    # Step 1: Parse the vCard file and build a list of contacts
    contacts_list = []
    with open(vcf_file_path, 'r') as vcf_file:
        for vcard in vobject.readComponents(vcf_file):
            if hasattr(vcard, 'fn'):  # Check if the vCard has a full name
                full_name = vcard.fn.value.strip()  # Clean whitespace from full name
                
                # Skip entries without a full name
                if not full_name:
                    continue
                
                name_parts = full_name.split()
                
                # Extract first and last names, ensuring there's no index error
                first_name = name_parts[0] if name_parts else ''
                last_name = name_parts[-1] if len(name_parts) > 1 else ''

                # Check if the vCard has a phone number
                if hasattr(vcard, 'tel'):
                    for tel in vcard.tel_list:
                        phone = clean_phone_number(tel.value)  # Clean the phone number
                        contacts_list.append((first_name, last_name, full_name, phone))

    # Step 2: Save to CSV
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['First Name', 'Last Name', 'Full Name', 'Phone Number'])  # Header
        writer.writerows(contacts_list)

    print(f"Contacts exported to {csv_file_path}")


vcf_loc = r"/Users/landon/Downloads/Fuller Adams and 290 others.vcf"
vcf_to_csv(vcf_loc)
