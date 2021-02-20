Set Up Local Host DNS:
1) Press Window Key
2) Search for Notepad and run it as admin
3) Press the Windows key.
4) Type Notepad in the search field.
5) In the search results, right-click Notepad and select Run as administrator.
6) From Notepad, open the following file:
7) c:\Windows\System32\Drivers\etc\hosts
8) Add in 127.0.0.2 pepehands.net
9) Save your changes.
10) Restart your pc

Django:
1) Download Google Cloud SDK from https://cloud.google.com/sdk/docs/install
2) Run "gcloud auth application-default login" after setup Google Cloud SDK
3) Download Google Cloud Proxy from "https://cloud.google.com/sql/docs/mysql/connect-admin-proxy#windows-64-bit"
4) Open cmd
5) Go to the folder where you save the proxy using cmd
6) Run "cloud_sql_proxy -instances=poetic-abacus-279809:asia-southeast1:pepehands123=tcp:3306"
7) run "venv\Scripts\activate" to activate virtual env
8) run "python manage.py runsslserver 127.0.0.2:8000 --certificate cert.pem --key key.pem" to run ssl server
9) go to "https//pepehands.net:8000" to access to the web


Database:
1) Login to Google Cloud Platform
2) Go to compute Engine and Select "VM instances"
3) Check if the VM is activated
4) Go to "https://remotedesktop.google.com/" and select Remote Access
5) Select maia-1 and enter 99036 for Pin
6) Open CMD and type "mysql-workbench"
7) select the one thats not root and enter password "bobbytee123"