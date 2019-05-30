# Install

```bash
git clone https://github.com/carrierx/carrierx-demo-apps.git
python3.6 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Configuration
In order to get the Voicemail app working you need to add email.ini to the deployment root. The template is provided in the repository root.

# Start the app
```bash
python ./manage.py runserver
```