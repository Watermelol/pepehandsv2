Django:
1) Download Google Cloud Proxy from "https://cloud.google.com/sql/docs/mysql/connect-admin-proxy#windows-64-bit"
2) Open cmd
3) Go to the folder where you save the proxy using cmd
4) Run "cloud_sql_proxy -instances=poetic-abacus-279809:asia-southeast1:pepehands123"
5) run "venv\Scripts\activate" to activate virtual env
6) run "python manage.py runsslserver --certificate cert.pem --key key.pem" to run ssl server
7) go to "https//:localhost:8000" to access to the web


Database:
1) Login to Google Cloud Platform
2) Go to compute Engine and Select "VM instances"
3) Check if the VM is activated
4) Go to "https://remotedesktop.google.com/" and select Remote Access
5) Select maia-1 and enter 99036 for Pin
6) Open CMD and type "mysql-workbench"
7) select the one thats not root and enter password "bobbytee123"