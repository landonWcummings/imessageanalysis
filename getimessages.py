import sqlite3
import csv

# Path to your chat.db file
db_path = r'/Users/landon/Library/Messages/chat.db'

# Connect to the database in read-only mode
conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
cursor = conn.cursor()

# Query to get messages with readable timestamps, group chat info, sender info, and contact name
cursor.execute('''
    SELECT
        message.date / 1000000000 + strftime('%s', '2001-01-01') AS timestamp,
        datetime(message.date / 1000000000 + strftime('%s', '2001-01-01'), 'unixepoch', 'localtime') AS readable_time,
        handle.id AS sender,
        handle.ROWID AS sender_id,
        message.text,
        chat.chat_identifier AS group_chat,
        chat.display_name AS group_chat_name,
        message.is_from_me AS sent_by_me,
        handle.id AS contact_identifier  -- This field is the phone number or email of the contact
    FROM message
    JOIN handle ON message.handle_id = handle.ROWID
    LEFT JOIN chat_message_join ON message.ROWID = chat_message_join.message_id
    LEFT JOIN chat ON chat_message_join.chat_id = chat.ROWID
    ORDER BY message.date ASC;
''')

# Fetch all rows
rows = cursor.fetchall()

# Save to CSV with UTF-8 encoding and double quote escaping
with open('imessages_export.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    writer.writerow(['Timestamp', 'Readable Time', 'Sender', 'Sender ID', 'Message', 'Group Chat', 'Group Chat Name', 'Sent by Me', 'Contact Identifier'])
    writer.writerows(rows)

# Close the connection
conn.close()

print("Messages with group chat info, contact identifier, and sent status exported to imessages_export.csv")
