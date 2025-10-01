# Install

```shell
git clone https://github.com/carrierx/carrierx-demo-apps.git
cd carrierx-demo-apps
python3.6 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
# Configuration settings

## Voicemail App
In order to get the Voicemail app working you need to add email.ini to the deployment root. The template is provided in the repository root.

# Start the app

IMPORTANT - the Django server is a development tool. Do not use the following for production.

```shell
python ./manage.py runserver --settings=flexml_project.settings.base
```
