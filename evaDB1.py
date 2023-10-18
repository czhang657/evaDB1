from ast import keyword
import os
import shutil
from typing import Dict, List
from langchain.chat_models import ChatOpenAI
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.document_loaders import UnstructuredURLLoader
from langchain.chains.summarize import load_summarize_chain
import pandas as pd
import streamlit as st, tiktoken

import evadb

MAX_CHUNK_SIZE = 10000

def receive_user_input():
    print(
        '''Welcome! This app lets you to search for your most insterested news and gives you summary and link. You need to provide your Serper API key , OpenAI API key and keywords.'''
    )
    SerperAPI = str(input(
            "Please enter your Serper API key: "))
    url = 'https://api.example.com/data'
    OpenAPI = str(
        input(
            "Please enter your OpenAI API key: "
        )
    )
    keyWord = str(
        input(
            "Please enter your key word: "
        )
    )



    os.environ["SERPER_KEY"] = SerperAPI
    os.environ["OPEN_KEY"] = OpenAPI
    return keyWord

def searchForNews(keyword, cursor):
    search = GoogleSerperAPIWrapper(type="news", tbs="qdr:w1", serper_api_key=os.environ["SERPER_KEY"])
    result_dict = search.results(keyword)
    cursor.drop_table("News111", if_exists=True).execute()
    cursor.drop_table("News", if_exists=True).execute()
    print(cursor.query(
        """CREATE TABLE IF NOT EXISTS News111 (title1 TEXT(50), link TEXT(50), summary TEXT(50));"""
    ).execute())
    cursor.query("INSERT INTO News111 (title1, link, summary) VALUES ('1', '2', '3')").df();
    cursor.query("SELECT * FROM News111").df()
    for news_item in result_dict['news']:
        title = news_item['title']  # Limit the title to 50 characters
        link = news_item['link']    # Limit the link to 50 characters
        loader = UnstructuredURLLoader(urls=[news_item['link']])
        data = loader.load()
        # print(title)
        # print(link)
        llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo', openai_api_key=os.environ["OPEN_KEY"])
        chain = load_summarize_chain(llm, chain_type="map_reduce")
        summary = chain.run(data)
        # print(summary)
        # print(cursor.query("SELECT * FROM News").df())
        cursor.query(f"INSERT INTO News111 (title1, link, summary) VALUES ('{title}', '{link}', '{summary}')").df();
        cursor.query("SELECT * FROM News111").df()

    cursor.query("DROP UDF IF EXISTS Similarity;").execute()
    Similarity_function_query = """CREATE UDF Similarity
                    INPUT (Frame_Array_Open NDARRAY UINT8(3, ANYDIM, ANYDIM),
                           Frame_Array_Base NDARRAY UINT8(3, ANYDIM, ANYDIM),
                           Feature_Extractor_Name TEXT(100))
                    OUTPUT (distance FLOAT(32, 7))
                    TYPE NdarrayFunction
                    IMPL './similarity.py'"""
    
    cursor.query(Similarity_function_query).execute()

    query = f"""
    SELECT Frame_Array_Open, Frame_Array_Base, Feature_Extractor_Name, Similarity(Frame_Array_Open, Frame_Array_Base, Feature_Extractor_Name) AS distance
    FROM News
    ORDER BY distance ASC
    LIMIT 1;
    """

    # Execute the query using the cursor
    print(cursor.query(query).execute())



if __name__ == "__main__":
    user_input = receive_user_input()
    cursor = evadb.connect().cursor()
    searchForNews(user_input, cursor)
