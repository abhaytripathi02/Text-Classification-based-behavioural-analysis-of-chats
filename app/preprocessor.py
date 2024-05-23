import re
import pandas as pd


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'     # 24hr
    # pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APap][mM]\s-\s' # 12hr-format

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # convet message_data type
    df['message_date'] = pd.to_datetime(
        df['message_date'], format='%d/%m/%Y, %H:%M - ')  # 24hr

    # df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M %p - ')    #12hr-format
    df.rename(columns={'message_date': 'date'}, inplace=True)
  

    # separate users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user_name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['only_date'] = df['date'].dt.date
    df['day'] = df['date'].dt.day
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['day_name'] = df['date'].dt.day_name()

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df



# Pandas library:
# What is Pandas? Pandas is a Python library used for working with data sets.
# It has functions for analyzing, cleaning, exploring, and manipulating data.

# re library:
# The re library in Python is used for working with regular expressions. Regular expressions are sequences of characters that define a search pattern. The re library allows you to search, match, and manipulate strings based on these patterns.



