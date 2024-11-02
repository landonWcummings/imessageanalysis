import csv
import re
import pandas as pd

def clean_phone_number(phone):
    """Clean up the phone number by removing spaces, hyphens, and parentheses."""
    return re.sub(r'[\s\-\(\)]', '', phone)

def load_contacts(contacts_file):
    """Load contacts from a CSV file into a dictionary mapping cleaned phone numbers to full names."""
    contacts = {}
    with open(contacts_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cleaned_phone = clean_phone_number(row['Phone Number'])
            contacts[cleaned_phone] = row['Full Name']
    return contacts

# File paths
imes_loc = r"/Users/landon/Desktop/ai proj/imessages_export.csv"
conts_loc = r"/Users/landon/Desktop/ai proj/contacts.csv"
final_save = r"/Users/landon/Desktop/ai proj/actuallylabeledmessages.csv"

# Load contacts into a dictionary
contacts_dict = load_contacts(conts_loc)

# Load iMessage export into a DataFrame
dataframe = pd.read_csv(imes_loc)

# Clean the Sender column and map to contact names
dataframe['Cleaned Sender'] = dataframe['Sender'].apply(clean_phone_number)
dataframe['Sender'] = dataframe['Cleaned Sender'].map(contacts_dict).fillna('Unknown')

# Drop the temporary Cleaned Sender column
dataframe.drop(columns=['Cleaned Sender'], inplace=True)

# Save the updated DataFrame to a new CSV file
dataframe.to_csv(final_save, index=False, encoding='utf-8')

print(f"Updated iMessage data saved to {final_save}")
