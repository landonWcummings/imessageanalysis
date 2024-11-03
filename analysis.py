import pandas as pd
import matplotlib.pyplot as plt

messages_location = r"c:\Users\lndnc\Downloads\cleanedimessages.csv"
messages = pd.read_csv(messages_location)

messages['Readable Time'] = pd.to_datetime(messages['Readable Time'])

sent_mes = messages[messages['Sent by Me'] == 1]
rec_mes = messages[messages['Sent by Me'] == 0]
group_chats = messages[messages['Group Chat'] == 1]
individual_messages = messages[messages['Group Chat'] == 0]

if True: # time activity analysis
    if True: # lifetime activity analysis
        groupingsize = 10
        sent_counts = sent_mes.set_index('Readable Time').resample(f'{groupingsize}D').size()
        rec_counts = rec_mes.set_index('Readable Time').resample(f'{groupingsize}D').size()

        # Create a DataFrame for both sent and received message counts
        activity_df = pd.DataFrame({'Sent': sent_counts, 'Received': rec_counts}).fillna(0)
        activity_df['Total'] = activity_df['Sent'] + activity_df['Received']  # Calculate total messages

        # Plot the data
        plt.figure(figsize=(12, 6))
        plt.plot(activity_df.index, activity_df['Sent'], label='Sent Messages', color='blue')
        plt.plot(activity_df.index, activity_df['Received'], label='Received Messages', color='orange')
        plt.plot(activity_df.index, activity_df['Total'], label='Total Messages', color='green')
        plt.xlabel('Date')
        plt.ylabel('Number of Messages')
        plt.title(f'Lifetime Activity: Messages Sent, Received, and Total in {groupingsize}-Day Intervals')
        plt.legend()
        plt.tight_layout()
        plt.show()

        average_sent = sent_counts.mean()

        # Plot the data for sent messages with an average line
        plt.figure(figsize=(12, 6))
        plt.plot(sent_counts.index, sent_counts, label='Sent Messages', color='blue')
        plt.axhline(average_sent, color='red', linestyle='--', label=f'Average ({average_sent:.2f})')
        plt.xlabel('Date')
        plt.ylabel('Number of Sent Messages')
        plt.title(f'Total Messages Sent in {groupingsize}-Day Intervals')
        plt.legend()
        plt.tight_layout()
        plt.show()



    if True: # 24 hour analysis
        timegroup = 20
        if True:  # sent and received time chart
            sent_mes['x_min_segment'] = sent_mes['Readable Time'].dt.floor(f'{timegroup}T').dt.time
            rec_mes['x_min_segment'] = rec_mes['Readable Time'].dt.floor(f'{timegroup}T').dt.time

            # Count the messages in each 20-minute segment
            sent_counts = sent_mes['x_min_segment'].value_counts().sort_index()
            rec_counts = rec_mes['x_min_segment'].value_counts().sort_index()

            # Combine sent and received counts into a single DataFrame
            activity_counts = pd.DataFrame({'Sent': sent_counts, 'Received': rec_counts}).fillna(0)

            # Plot the data
            activity_counts.plot(kind='bar', width=0.8, stacked=False, figsize=(14, 6))
            plt.xlabel(f'Time of Day ({timegroup}-minute segments)')
            plt.ylabel('Number of Messages')
            plt.title(f'Message Activity by {timegroup}-Minute Segments (Sent vs. Received)')
            plt.xticks(rotation=90)
            plt.legend(['Sent', 'Received'])
            plt.tight_layout()
            plt.show()
        if True: #(sent+received) time chart
            messages['x_min_segment'] = messages['Readable Time'].dt.floor(f'{timegroup}T').dt.time
            
            activity_counts = messages['x_min_segment'].value_counts().sort_index()

            plt.figure(figsize=(12, 6))
            activity_counts.plot(kind='bar', width=0.8)
            plt.xlabel(f'Time of Day ({timegroup}-minute segments)')
            plt.ylabel('Number of Messages')
            plt.title(f'Message Activity by {timegroup}-Minute Segments')
            plt.xticks(rotation=90)
            plt.tight_layout()
            plt.show()
        if True: #sent time chart
            sent_mes['x_min_segment'] = sent_mes['Readable Time'].dt.floor(f'{timegroup}T').dt.time
            
            activity_counts = sent_mes['x_min_segment'].value_counts().sort_index()

            plt.figure(figsize=(12, 6))
            activity_counts.plot(kind='bar', width=0.8)
            plt.xlabel(f'Time of Day ({timegroup}-minute segments)')
            plt.ylabel('Number of Sent Messages')
            plt.title(f'Number of Sent Messages by {timegroup}-Minute Segments')
            plt.xticks(rotation=90)
            plt.tight_layout()
            plt.show()

if True: # GC analysis
    topnumGC = 30
    group_chat_counts = group_chats['Group Chat Name'].value_counts().head(topnumGC)
    print(group_chat_counts)
    if True:
        participation_rates = {}

        # Calculate participation rate for each of the top group chats
        for name in group_chat_counts.index:
            gc_messages = messages[messages['Group Chat Name'] == name]
            sent_gc_messages = sent_mes[sent_mes['Group Chat Name'] == name]
            
            # Calculate participation rate as sent messages / total messages
            participation_rate = sent_gc_messages.shape[0] / gc_messages.shape[0] if gc_messages.shape[0] > 0 else 0
            participation_rates[name] = participation_rate

        # Convert participation rates to a DataFrame for easy sorting and plotting
        participation_df = pd.DataFrame(list(participation_rates.items()), columns=['Group Chat Name', 'Participation Rate'])
        participation_df = participation_df.sort_values(by='Participation Rate', ascending=False).head(topnumGC)

        # Plot the top group chats by participation rate
        plt.figure(figsize=(15, 8))
        plt.barh(participation_df['Group Chat Name'], participation_df['Participation Rate'], color='skyblue')
        plt.xlabel('Participation Rate')
        plt.ylabel('Group Chat Name')
        plt.title(f'Top {topnumGC} Group Chats by Participation Rate')
        plt.gca().invert_yaxis()  # Invert y-axis to have the highest rate at the top
        plt.tight_layout()
        plt.show()




    if True: # Group chat analysis
        if False:
            group_chat_counts.index = range(topnumGC)

        plt.figure(figsize=(14, 6))
        group_chat_counts.plot(kind='bar')
        plt.xlabel('Group Chat Name')
        plt.ylabel('Number of Messages')
        plt.title(f'Top {topnumGC} Group Chats by Number of Messages')
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()

if True: # all dms analysis
    contactstolookat = 30
    contact_counts = individual_messages['To'].value_counts().head(contactstolookat)
    if True: # dms
        

        # Combine sent and received counts for each contact
        

        # Plot the top 30 contacts by total messages (sent and received)
        plt.figure(figsize=(12, 8))
        plt.barh(contact_counts.index, contact_counts.values, color='skyblue')
        plt.xlabel('Total Messages')
        plt.ylabel('Contact')
        plt.title(f'Top {contactstolookat} Contacts by Total Direct Messages')
        plt.gca().invert_yaxis()  # Invert y-axis for descending order
        plt.tight_layout()
        plt.show()




    if True: # all messages including GCs
        dm_counts = individual_messages['To'].value_counts()

        # Calculate the group chat messages sent by each contact
        group_chat_counts = messages[(messages['Group Chat'] == 1)]['Sender'].value_counts()
        
        # Calculate group chat messages you sent, where each contact also participated
        # First, identify all unique group chat names that each contact has sent a message in
        contact_group_chats = messages[messages['Group Chat'] == 1].dropna().groupby('Sender')['Group Chat Name'].unique()
        print(contact_group_chats)
        # Initialize a dictionary to store total interactions for each contact
        total_interactions = {}

        for contact in dm_counts.index:
            # Sum of direct messages with this contact
            dm_total = dm_counts.get(contact, 0)

            # Sum of group chat messages sent by this contact
            group_chat_total = group_chat_counts.get(contact, 0)

            # Sum of group chat messages you sent where this contact also participated
            contact_chat_groups = contact_group_chats.get(contact, [])
            group_chat_me_total = messages[(messages['Sender'] == "Me") & (messages['Group Chat Name'].isin(contact_chat_groups))].shape[0]

            # Calculate total interactions for this contact
            total_interactions[contact] = dm_total + group_chat_total + group_chat_me_total

        # Convert total interactions to a DataFrame and get the top contacts
        total_interactions_df = pd.DataFrame.from_dict(total_interactions, orient='index', columns=['Total Messages'])
        top_contacts = total_interactions_df.nlargest(contactstolookat, 'Total Messages')

        # Plot the top 30 contacts by total interactions
        plt.figure(figsize=(12, 8))
        plt.barh(top_contacts.index, top_contacts['Total Messages'], color='skyblue')
        plt.xlabel('Total Messages')
        plt.ylabel('Contact')
        plt.title(f'Top {contactstolookat} Contacts by Total Interactions (includes group chats)')
        plt.gca().invert_yaxis()  # Invert y-axis for descending order
        plt.tight_layout()
        plt.show()

if True: # specific GC analysis
    targetGC = "XC Juniors"
    group_chat_messages = messages[messages['Group Chat Name'] == targetGC]

    # Count the number of messages sent by each person in the group chat
    message_counts_by_sender = group_chat_messages['Sender'].value_counts()

    # Function to format the pie chart labels with both percentage and raw count
    def format_autopct(pct, all_values):
        absolute = int(round(pct / 100. * sum(all_values)))
        return f"{pct:.1f}%\n({absolute} msgs)"

    # Plot as a pie chart
    plt.figure(figsize=(12, 12))
    plt.pie(
        message_counts_by_sender,
        labels=message_counts_by_sender.index,
        autopct=lambda pct: format_autopct(pct, message_counts_by_sender),
        startangle=140
    )
    plt.title(f'Message Distribution by Sender in Group Chat: {targetGC}')
    plt.show()

if True: # specific person analysis
    target = "Augie Bunting"
    groupingsize = 10
    common_start_date = messages['Readable Time'].min()

    # Filter for direct messages with the target
    dm_messages = individual_messages[individual_messages['To'] == target]

    # Filter for group chat messages sent by the target
    group_chat_messages_from_target = messages[(messages['Sender'] == target) & (messages['Group Chat'] == 1)]

    # Identify group chats where the target has participated
    target_group_chats = group_chat_messages_from_target['Group Chat Name'].dropna().unique()
    # Filter for messages you sent in those identified group chats
    group_chat_messages_from_me = messages[(messages['Sender'] == "Me") & (messages['Group Chat Name'].isin(target_group_chats))]

    # Group each type of message by the specified interval with a common start date
    dm_counts = dm_messages.set_index('Readable Time').resample(f'{groupingsize}D', origin=common_start_date).size()
    group_chat_target_counts = group_chat_messages_from_target.set_index('Readable Time').resample(f'{groupingsize}D', origin=common_start_date).size()
    group_chat_me_counts = group_chat_messages_from_me.set_index('Readable Time').resample(f'{groupingsize}D', origin=common_start_date).size()

    # Combine all counts for total interactions
    total_interactions = dm_counts.add(group_chat_target_counts, fill_value=0).add(group_chat_me_counts, fill_value=0)

    # Plot the data
    plt.figure(figsize=(12, 6))
    plt.plot(dm_counts.index, dm_counts, label=f'DM Messages with {target}', color='blue')
    plt.plot(total_interactions.index, total_interactions, label=f'Total Interactions with {target} (including groupchats)', color='green', linestyle='--')
    plt.xlabel('Date')
    plt.ylabel(f'Number of Messages in {groupingsize}-Day Intervals')
    plt.title(f'Message Activity with {target} Over Time in {groupingsize}-Day Intervals')
    plt.legend()
    plt.tight_layout()
    plt.show()

