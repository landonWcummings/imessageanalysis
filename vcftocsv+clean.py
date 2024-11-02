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

def load_contacts(contacts_file):
    """Load contacts from a CSV file and return a dictionary mapping cleaned phone numbers to full names."""
    contacts = {}
    with open(contacts_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Clean phone number and store with full name
            cleaned_phone = clean_phone_number(row['Phone Number'])
            contacts[cleaned_phone] = row['Full Name']
    return contacts

def convert_senders_to_names(imessage_file, contacts_file, output_file):
    """Convert sender phone numbers in iMessage data to corresponding full contact names."""
    contacts = load_contacts(contacts_file)
    
    with open(imessage_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=['Timestamp', 'Readable Time', 'Sender', 'Message', 'Group Chat', 'Sent by Me'])
        
        writer.writeheader()
        
        for row in reader:
            # Clean the sender's phone number
            sender_number = clean_phone_number(row['Sender'])
            # Match the cleaned sender number with the contact name
            full_name = contacts.get(sender_number, sender_number)  # Use number if no match found
            
            # Write the updated row to the new CSV
            writer.writerow({
                'Timestamp': row['Timestamp'],
                'Readable Time': row['Readable Time'],
                'Sender': full_name,  # Replace number with full name
                'Message': row['Message'],
                'Group Chat': row['Group Chat'],
                'Sent by Me': row['Sent by Me']
            })
    
    print(f"iMessage data converted and saved to {output_file}")

def vcf_to_csv(vcf_file_path, csv_file_path='contacts.csv'):
    """Parse a vCard file and export to CSV format."""
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

# File paths
vcf_loc = r"/Users/landon/Downloads/Fuller Adams and 290 others.vcf"
imes_loc = r"/Users/landon/Desktop/ai proj/imessages_export.csv"
final_save = r"/Users/landon/Desktop/ai proj/actuallylabeledmessages.csv"
conts_loc = r"/Users/landon/Desktop/ai proj/contacts.csv"

# Convert vCard to CSV
vcf_to_csv(vcf_loc, conts_loc)

# Convert iMessage senders to contact names
convert_senders_to_names(imes_loc, conts_loc, final_save)
