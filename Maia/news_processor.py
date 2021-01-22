class news_info:
    def __init__(self, web_page, sentiment_score, sentiment_classification):
        self.url = web_page["url"]
        self.title = web_page["title"]
        self.body = web_page["body"]
        self.date_published = web_page["datePublished"]
        self.emotion_score = sentiment_score[0]
        self.emotion_strength = sentiment_score[1]
        self.emotion_classification = sentiment_classification