
vcf_loc = r"/Users/landon/Downloads/Fuller Adams and 290 others.vcf"
imes_loc = r"/Users/landon/Desktop/ai proj/imessages_export.csv"
final_save = r"/Users/landon/Desktop/ai proj/actuallylabeledmessages.csv"
conts_loc = r"/Users/landon/Desktop/ai proj/contacts.csv"

import csv

def load_contacts(contacts_file):
    """Load contacts from a CSV file and return a dictionary mapping phone numbers to full names."""
    contacts = {}
    with open(contacts_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Store the full name with the cleaned phone number as the key
            cleaned_phone = row['Phone Number']
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
            # Get the sender's phone number
            sender_number = row['Sender']
            # Match the sender number with the contact name
            full_name = contacts.get(sender_number, sender_number)  # Use number if no match found
            
            # Write the updated row to the new CSV
            writer.writerow({
                'Timestamp': row['Timestamp'],
                'Readable Time': row['Readable Time'],
                'Sender': full_name,  
                'Message': row['Message'],
                'Group Chat': row['Group Chat'],
                'Sent by Me': row['Sent by Me']
            })
    
    print(f"iMessage data converted and saved to {output_file}")


convert_senders_to_names(imes_loc, conts_loc, final_save)

