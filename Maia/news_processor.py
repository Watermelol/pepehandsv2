from array import *
from sentiment_analysis import *

class news_info:
    def __init__(self, web_page, sentiment_score, sentiment_classification):
        self.url = web_page["url"]
        self.title = web_page["title"]
        self.body = web_page["body"]
        self.date_published = web_page["datePublished"]
        self.emotion_score = sentiment_score[0]
        self.emotion_strength = sentiment_score[1]
        self.emotion_classification = sentiment_classification

class news_scrape:
    def scrapeNews(self, industry):
        # Imports
        import requests

        # API Token and URL
        URL = "https://rapidapi.p.rapidapi.com/api/search/NewsSearchAPI"
        HEADERS = {
            'x-rapidapi-key': "33f478fa06msh75c086166067598p191012jsn268d98f99935",
            'x-rapidapi-host': "contextualwebsearch-websearch-v1.p.rapidapi.com"
            }

        # Query settings
        query = industry + " industry"
        page_number = 1
        page_size = 30
        auto_correct = True
        safe_search = False
        with_thumbnails = True
        from_published_date = ""
        to_published_date = ""

        # Initialize variable
        querystring = {"q": query,
                    "pageNumber": page_number,
                    "pageSize": page_size,
                    "autoCorrect": auto_correct,
                    "safeSearch": safe_search,
                    "withThumbnails": with_thumbnails,
                    "fromPublishedDate": from_published_date,
                    "toPublishedDate": to_published_date
                    }

        # Running the API
        response = requests.get(URL, headers=HEADERS, params=querystring).json()
        
        # Prints the list of web pages, can be used as reference for the json file
        # for web_page in response["value"]:
            # url = web_page["url"]
            # title = web_page["title"]
            # description = web_page["description"]
            # body = web_page["body"]
            # date_published = web_page["datePublished"]
            # language = web_page["language"]
            # is_safe = web_page["isSafe"]
            # provider = web_page["provider"]["name"]

            # image_url = web_page["image"]["url"]
            # image_height = web_page["image"]["height"]
            # image_width = web_page["image"]["width"]

            # thumbnail = web_page["image"]["thumbnail"]
            # thumbnail_height = web_page["image"]["thumbnailHeight"]
            # thumbnail_width = web_page["image"]["thumbnailWidth"]

            # print("Url: {}. Title: {}. Published Date: {}.".format(url, title, date_published))

        # Returns a dictionary
        return response

    # Stores the dictionary into a flat file
    def store_data(self, dict, industry):
        import pickle

        # Initialize file name to be used
        file_name = industry + ".pkl"

        # Initialize sentiment analyzer
        sentiment_analyzer = sentiment_analysis()

        # Opens the pickle file with exception handling
        try:
            pickle_file = open(file_name, "rb")
            while True:
                try:
                    old_news = pickle.load(pickle_file)
                except EOFError:
                    break
            pickle_file.close()
        except OSError as e:
            print(e)
            print("\nNo existing file, skipping")

        old_news_titles = []

        # Appends all titles from old file to check with new news titles
        try:
            for tempData in old_news:
                old_news_titles.append(tempData.title)
        except UnboundLocalError as e:
            print(e)
            print("\nSince file does not exist, skipping")

        # For all new news data, if not exist in old data, append to new list
        news_list = []

        for web_page in dict["value"]:
            #Checks if new titles are in old titles
            if web_page["title"] not in old_news_titles:
                # Insert news information, sentiment score and classification into class
                news_list.append(news_info(web_page, sentiment_analyzer.run_sentiment_analysis(web_page["body"]), sentiment_analyzer.run_score_classification(sentiment_analyzer.run_sentiment_analysis(web_page["body"]))))

        # Append the list
        try:
            news_list += old_news
        except UnboundLocalError as e:
            print(e)
            print("\nSince file does not exist, skipping")

        # Write new list into pickle
        with open(file_name, 'wb') as output:
            pickle.dump(news_list, output, pickle.HIGHEST_PROTOCOL)