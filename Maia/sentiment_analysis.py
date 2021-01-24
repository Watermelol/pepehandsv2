# Imports
from google.cloud import language_v1
import csv

# Function takes a string to analyze the sentiment then returns
# an array = [score, magnitude], can be used in run_score_classification
def run_sentiment_analysis(newstext):

    # Instantiates a client
    client = language_v1.LanguageServiceClient()

    # The text to analyze
    text = newstext

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Specify language
    language = "en"
    document = {"content": text, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})

    # Return overall sentiment
    sentiment_score = [response.document_sentiment.score, response.document_sentiment.magnitude]
    return sentiment_score

# Takes in an array [score, magnitude] to classify the score
# Returns a string containing the emotion of the score
def run_score_classification(score):
    classification = ''

    # Assign emotion strength
    if score[1] >= 10:
        classification = "Clearly "
    elif score[1] >= 1:
        classification = "Strongly "

    # Assign score emotion
    if score[0] >= 0.25:
        classification += "Positive "
    elif score[0] <= -0.25:
        classification += "Negative "
    else:
        classification += "Neutral "
    return classification