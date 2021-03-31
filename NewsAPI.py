'''
Due to module operation problems, we directly use third-party package as a replacement.
The installation command is as follows：
           $ python -m pip install newsapi-python
Source: mattlisiv/newsapi-python (https://github.com/mattlisiv/newsapi-python)
'''

from newsapi import NewsApiClient    # According to github description, import the client class into project
import pandas as pd


def CreateDF(JsonArray,columns):
    dfData = pd.DataFrame()

    for item in JsonArray:
        itemStruct = {}

        for cunColumn in columns:
            itemStruct[cunColumn] = item[cunColumn]

        dfData = dfData.append(itemStruct,ignore_index=True)

    return dfData


def main():
    api = NewsApiClient('b48b0f4fc3ef4ff68c4ee996b058ea84')

    # get  news form api
    news =api.get_everything(q='SNP election 2021', language='en',sort_by='relevancy',page_size = 100)
    columns = ['author', 'publishedAt', 'title', 'description', 'content', 'url']
    columns_2 = ['title']
    df = CreateDF(news['articles'], columns)
    title = CreateDF(news['articles'], columns_2)
    df.to_csv('SNP Election.csv')
    title.to_csv('SNP Election - title.csv')


main()