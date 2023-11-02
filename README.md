# evaDB1
evaDB project 1 CS 4420: New Search And Summary

Introduction and Expected Input and Output
For this project, I initially tried to make an application which can summarize academic
papers from pdf using ChatGPT. However, the pdf loading part became a problem and I
could not have my pdf loader running. Thus, I tried another project which is able to search
news for customers by keywords and then extract the most related news and summarize
them. In this project, I took a look at the code from the third example topic from the topic
list given to us, especially on the python file “streamlit_app.py”. I basically used the similar
method but made some changes. The input of this project are the Serper API key, OpenAI
API key, and the keyword input from the customers. The output of the project is the title,
link, and the summary of the news searched from Google and summarized by ChatGPT. In
the implementation stage, I chose to use LangChain to approach to the Google searching
as well as to the OpenAI. After getting the title, link, and summaries from the news, I used
the similarity approach to extract the result of news that is the best fit for the customers’
keywords and use the title, link and summaries as my output. For sample inputs and
outputs, I listed them here in the following:
After the first time of extraction, the news are stored in the table created by the cursor.
The table has three columns: title, link and summary.

Then I tried to use the similarity function into the data stored in evaDB cursor. I call the
similarity function to find the most related article to the keyword provided by the user and
show it to the user.