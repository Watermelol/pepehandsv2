from google.cloud import storage
from threading import Timer
import os

client = storage.Client.from_service_account_json(json_credentials_path="Maia/GCScredential.json")
bucket = client.get_bucket('maia_report_1')

def uploadReport(fileName):
    file_name = bucket.blob(fileName)
    file_name.upload_from_filename(fileName)

    deleteReportFromLocal(fileName)
    return "File Uploaded"

def deleteReportFromLocal(fileName):
    if os.path.exists(fileName):
        os.remove(fileName)