import streamlit as st
import preprocessor
import utils
import matplotlib.pyplot as plt
import seaborn as sns
import time

from streamlit_lottie import st_lottie
import json




st.sidebar.title("Whatsapp Chat Analyzer")

#-------------------------------------------------------------------------------------
with open("animation.json") as source:
    animation = json.load(source)

st_lottie(animation, loop=True, width=300, height=300)


#-------------------------------------------------------------------------------------


def generate_pdf():
    # JavaScript to trigger printing
    js_script = """
    <script>
    window.print();
    </script>
    """
    # Display JavaScript to trigger printing
    st.components.v1.html(js_script)

# Function to create download button and trigger PDF generation
def download_and_print_pdf():
    if st.button('Download PDF'):
        generate_pdf()



# Call function to create download button and trigger PDF generation
download_and_print_pdf()

#-------------------------------------------------------------------------------------
# spinner 
# with st.spinner('Wait for it...'):
#                     time.sleep(4)
#                     st.success('Done!')

# progress bar 
# txt ="% completed"
# my_bar = st.progress(0, text=txt)
# for pr in range(99):
#     time.sleep(0.1)
#     my_bar.progress(pr+2, text = f"{pr + 2}% completed")

# time.sleep(1)
# my_bar.empty()
    

# progress_text = "Operation in progress. Please wait."
# my_bar = st.progress(0, text=progress_text)
# for percent_complete in range(100):
#      time.sleep(0.05)
#      my_bar.progress(percent_complete + 1, text=progress_text)

# time.sleep(1)
# my_bar.empty()




uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # df -> dataframe of dataSet -> preprocessing of data
    df = preprocessor.preprocess(data)

    # st.dataframe(df)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    # select user from list of users(selected_user)
    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    if st.sidebar.button('Start Analysis'):
        
        # progress bar 
        txt ="% completed"
        my_bar = st.progress(0, text=txt)
        for pr in range(99):
            time.sleep(0.1)
            my_bar.progress(pr+2, text = f"{pr + 2}% completed")

        time.sleep(1)
        my_bar.empty()
        
        st.balloons()

        # fetching the filtered dataframe based on selected user or overall analysis (from utils.py)
        num_messages, words, num_media_shared, num_links = utils.fetch_stats(selected_user, df)

        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Total Message')
            st.title(num_messages)
        with col2:
            st.header('Total Words')
            st.title(words)
        with col3:
            st.header('Media Shared')
            st.title(num_media_shared)
        with col4:
            st.header('Links Shared')
            st.title(num_links)

        # timekine analysis
        # monthly timeline
        st.title('Monthly Timeline')
        timeline = utils.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical', color='red')
        st.pyplot(fig)

        # daily timeline
        st.title('Daily Timeline')
        daily_timeline = utils.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],
                daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical', color='red')
        st.pyplot(fig)

        # user activity map
        st.title('Users Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header('Most busy day')
            busy_day = utils.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical', color='red')
            st.pyplot(fig)

        with col2:
            st.header("User's Month Activity")
            month_act = utils.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(month_act.index, month_act.values, color='orange')
            plt.xticks(rotation='vertical', color='red')
            st.pyplot(fig)

        # User_Heatmap
        st.title('Weekly Activity Map')
        user_heatmap = utils.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the busiest users in the group(Group Level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            # function calling
            x, new_df = utils.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='cyan')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                new_df.index += 1
                st.dataframe(new_df)

        # WordCloud
        st.title('Word Cloud')
        df_wc = utils.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = utils.most_common_words(selected_user, df)
        st.title('Most commmon words')
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # emoji analysis
        emoji_df = utils.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        fig, ax = plt.subplots()
        ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
        ax.set_aspect('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.rcParams['font.sans-serif'] = ['Segoe UI Emoji']  # Set the default font to use in Matplotlib
        st.pyplot(fig)
    
        # Rename the column before displaying the DataFrame   
        emoji_df_renamed = emoji_df.rename(columns={0: "Emoji", 1: "Frequency"})
        # Start the index from 1
        emoji_df_renamed.index += 1
        
        st.dataframe(emoji_df_renamed, width=600, height=500)
      
      
      
      
      
      
        #sentiment analysis 
        # import numpy as np
        # URLPATTERN = r'(https?://\S+)'
        # df['url_count'] = df['message'].apply(lambda x: re.findall(URLPATTERN, x)).str.len()
        # links = np.sum(df.url_count)
        
        # link_message = df[df['url_count']>0]
        # deleted_message = df[(df['message'] == 'You deleted this message')| (df['message'] == 'This message was deleted.')]
        # media_message_df = df[(df['message'] == '<Media omitted>') | (df['message'] == 'image omitted') | (df['message'] == 'video omitted') | (df['message']=='sticker omitted')]    
        # only_message = df.drop(media_message_df.index)
        # only_message = only_message.drop(deleted_message.index)
        # only_message = only_message.drop(link_message.index) 

        # from nltk.sentiment.vader import SentimentIntensityAnalyzer 
        # import nltk
        # nltk.download('vader_lexicon')
        # sentiments = SentimentIntensityAnalyzer()
        # data = df.dropna()
        # data["positive"] = [sentiments.polarity_scores(i)["pos"] for i in data['message']]
        # data["negative"] = [sentiments.polarity_scores(i)["pos"] for i in data['message']]
        # data["neutral"] = [sentiments.polarity_scores(i)["pos"] for i in data['message']]
        # data.head() 
        # # Plotting
        # fig, ax = plt.subplots()
        # ax.plot(df['date'], data['positive'], label='Positive', color='green')
        # ax.plot(df['date'], data['negative'], label='Negative', color='red')
        # ax.plot(df['date'], data['neutral'], label='Neutral', color='blue')
        # plt.xticks(rotation='vertical')
        # plt.legend()
        # plt.title("Sentiment Analysis Over Time")
        # plt.xlabel("Date")
        # plt.ylabel("Sentiment Score")
      
      
       
       
       
# import streamlit as st
# from io import BytesIO
# from reportlab.pdfgen import canvas

# def generate_pdf():
#     # Create a BytesIO buffer to hold the PDF
#     buffer = BytesIO()

#     # Create a new PDF
#     pdf = canvas.Canvas(buffer)

#     # Add content to the PDF
#     pdf.drawString(100, 750, "Hello, this is a PDF created with Streamlit!")

#     # Save the PDF
#     pdf.save()

#     # Move the buffer cursor to the beginning
#     buffer.seek(0)
    
#     return buffer

# # Main Streamlit code
# st.title("PDF Download Example")

# # Generate PDF and create a download button
# pdf_buffer = generate_pdf()
# st.download_button(label="Download PDF", data=pdf_buffer, file_name="example.pdf", mime="application/pdf", key="pdf-download")


