from django import forms
from itertools import chain

PHONE_VALIDATION_PATTERN = r"^\d{11}$"


class ConcurrentCallsForm(forms.Form):
    phone_number = forms.CharField(
        label="Phone number",
        widget=forms.TextInput(
            attrs={
                "class": "form-control js-multipliable-field",
                "pattern": PHONE_VALIDATION_PATTERN,
                "placeholder": "1XXXXXXXXXX",
                "data-max-entries": "5",
            }
        ),
        help_text="Enter a phone number to dial",
    )


class ForwardForm(forms.Form):
    phone_number = forms.CharField(
        label="Phone number",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "pattern": PHONE_VALIDATION_PATTERN,
                "placeholder": "1XXXXXXXXXX",
            }
        ),
        help_text="Enter a phone number that calls will be forwarded to",
    )
    action = forms.URLField(
        label="URL",
        widget=forms.URLInput(attrs={"class": "form-control"}),
        help_text="Enter a URL containing further FlexML instructions if the call fails",
        required=False,
    )

    hangupOnStar = forms.ChoiceField(
        label="Call ends when * is pressed",
        widget=forms.Select(attrs={"class": "form-control"}),
        choices=(("true", "Yes"), ("false", "No")),
        required=False,
    )


class SimpleMenuForm(forms.Form):
    instructions = forms.CharField(
        label="Instructions",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        help_text="Enter the message callers will hear",
        initial="Thank you for calling. Please press 0 for customer service.",
    )

    def __init__(self, *args, **kwargs):
        super(SimpleMenuForm, self).__init__(*args, **kwargs)
        for idx in chain(range(0, 10), ("*", "#")):
            self.fields[f"url_{idx}"] = forms.URLField(
                label=f'URL for key "{idx}"',
                widget=forms.TextInput(attrs={"class": "form-control"}),
                required=False,
            )


class VoicemailForm(forms.Form):
    greeting_message = forms.CharField(
        label="Greeting message",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        help_text="Enter the message callers will hear before the recording starts",
        initial="Hello. Please leave a message after the beep.",
    )
    goodbye_message = forms.CharField(
        label="Goodbye message",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        help_text="Enter the message callers will hear after the recording ends",
        initial=".",
    )

    voice_type = forms.ChoiceField(
        label="Voice type",
        widget=forms.Select(attrs={"class": "form-control"}),
        help_text="Select a voice type. The default is male",
        choices=(("man", "Male"), ("woman", "Female")),
    )

    email = forms.EmailField(
        label="Email that will receive voice recording",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "example@somemailservice.com",
            }
        ),
        help_text="This email address will receive a link to the recording",
        required=False,
    )

    email_subject = forms.CharField(
        label="Email subject",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        help_text="Enter the message subject that will be attached to the email",
        required=False,
    )

    containerSid = forms.CharField(
        label="Storage container secure ID",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
                "pattern": r"\w{8}-\w{4}-\w{4}-\w{4}-\w{12}",
            }
        ),
        help_text="Find your container SIDs through the CarrierX Portal",
        required=True,
    )

    fileFormat = forms.ChoiceField(
        label="File format",
        widget=forms.Select(attrs={"class": "form-control"}),
        choices=(("mp3", "MP3"), ("wav", "WAV"), ("ul", "UL")),
        help_text="Select the file format for recordings. The default is MP3",
        required=False,
    )

    finishOnKey = forms.CharField(
        label="DTMF key to end recording",
        widget=forms.TextInput(
            attrs={"class": "form-control", "pattern": r"[\d#*]{1,12}|none"}
        ),
        help_text="Enter the DTMF key callers will press to end the recording. "
        "Values accepted in this field are: 0 , 1,2,3,4,5,6,7,8,9,#, "
        "and *. By default, pressing any valid key will end the recording. "
        'The string value "none" can be passed to disable this feature. '
        "Note that multiple values can be passed into a single string. "
        'For example, if the string "123" is passed, then pressing 1 , 2 , '
        "or 3 will end the recording",
        required=False,
    )

    playBeep = forms.ChoiceField(
        label="Play beep",
        widget=forms.Select(attrs={"class": "form-control"}),
        choices=(("true", "Yes"), ("false", "No")),
        help_text="Select whether or not a beep will be played to indicate that a recording "
        "has started. The default is True, and a beep will play",
        required=False,
    )


class SimpleMessageForm(forms.Form):
    text_or_audio = forms.CharField(
        label="Message or URL containing audio file",
        widget=forms.TextInput(
            attrs={
                "class": "form-control js-multipliable-field",
                "data-max-entries": "10",
            }
        ),
        help_text="Enter a message or an audio file URL",
    )

    voice_type = forms.ChoiceField(
        label="Voice type",
        widget=forms.Select(attrs={"class": "form-control"}),
        help_text="Select a voice type. The default is male",
        choices=(("man", "Male"), ("woman", "Female")),
    )

    notify_on_key = forms.CharField(
        label="DTMF key to send notifications",
        widget=forms.TextInput(
            attrs={"class": "form-control", "pattern": r"[\d#*]{1,12}|none"}
        ),
        help_text="If specified, the email address specified below will be "
        "notified if one of the DTMF keys is entered.  This may be used "
        "to gather confirmation or opt-out information from users.",
        required=False,
    )
    notify_email = forms.EmailField(
        label="Email that will receive notifications",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "example@somemailservice.com",
            }
        ),
        help_text="This email address will receive notifications",
        required=False,
    )
    notify_text_or_audio = forms.CharField(
        label="Message or URL containing audio file to be played after notify",
        widget=forms.TextInput(
            attrs={
                "class": "form-control js-multipliable-field",
                "data-max-entries": "10",
            }
        ),
        help_text="Enter a message or an audio file URL",
        required=False,
    )


class CallTreatmentForm(forms.Form):
    reason = forms.ChoiceField(
        label="Reject reason",
        widget=forms.Select(attrs={"class": "form-control"}),
        help_text="Enter the reason for rejecting a call.",
        choices=(
            ("busy", "Busy"),
            ("busy-here", "Busy here"),
            ("decline", "Decline"),
            ("does-not-exist", "Does not exist"),
            ("forbidden", "Forbidden"),
            ("rejected", "Rejected"),
            ("not-found", "Not found"),
        ),
        initial="rejected",
        required=False,
    )
    text_or_audio = forms.CharField(
        label="Text or URL to answer",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        help_text="Enter the string to say, or the URL to play.",
        required=False,
    )


class RoutingEngineForm(forms.Form):
    api_token = forms.CharField(
        label="API token capable of performing LCR lookup request",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True,
    )
    lcr = forms.ChoiceField(
        label="Order drains using least-cost routing",
        widget=forms.Select(attrs={"class": "form-control"}),
        choices=(("true", "Yes"), ("false", "No")),
        required=False,
    )
    dst = forms.CharField(
        label="Destination trunk_group_sid for outbound calls.  Not required for inbound calls.",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )
    max_rate = forms.CharField(
        label="Maximum drain rate allowed (e.g. 0.01 to limit calls to 1c/mou or less).  Leave blank to disable this feature.",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )
    min_margin_percent = forms.CharField(
        label="Minimum allowed margin if customer rate is provided (e.g. 0 to prevent underwater).  Leave blank to disable this feature.",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )
    min_margin_rate = forms.CharField(
        label="Minimum allowed margin in dollars if customer rate is provided (e.g. -0.01 to allow up to 1c/mou loss).  Leave blank to disable this feature.",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )


class VconProxyForm(forms.Form):
    dst = forms.CharField(
        label="Destination phone number to forward calls to (in e164 format)",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True,
    )
    conserver = forms.CharField(
        label="URL for vCon conserver",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True,
    )
    conserver_api_token = forms.CharField(
        label="Conserver server api token",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True,
    )
    transcribe = forms.ChoiceField(
        label="Transcribe",
        widget=forms.Select(attrs={"class": "form-control"}),
        choices=(("true", "Yes"), ("false", "No")),
        required=False,
    )
    transcribe_api_token = forms.CharField(
        label="OpenAI token, required if transcription is requested",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )
