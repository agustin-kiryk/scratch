import os
import secrets
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
TWILIO_VERIFICATION_SID = os.getenv('TWILIO_VERIFICATION_SID')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_verification_sms(to_phone_number):
    verification = client.verify \
        .v2 \
        .services(TWILIO_VERIFICATION_SID) \
        .verifications \
        .create(to_phone_number, channel='sms')

    print(verification.status)
    return verification.status


def verify_sms(to_phone_number, code):

        code_str = str(code)
        verification_check = client.verify \
            .v2 \
            .services(TWILIO_VERIFICATION_SID) \
            .verification_checks \
            .create(to=to_phone_number, code=code_str)
    
        print(verification_check.status)
        return verification_check.status


"""
  NO USAMOS STEEP 1 DE TWILIO
   """

"""   output speared  STEEP 2
{
    "sid": "VEXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "service_sid": "VAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "account_sid": "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "to": "+15017122661",
    "channel": "sms",
    "status": "pending",
    "valid": false,
    "date_created": "2015-07-30T20:00:00Z",
    "date_updated": "2015-07-30T20:00:00Z",
    "lookup": {},
    "amount": null,
    "payee": null,
    "send_code_attempts": [
        {
            "time": "2015-07-30T20:00:00Z",
            "channel": "SMS",
            "attempt_sid": "VLXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        }
    ],
    "sna": null,
    "url": "https://verify.twilio.com/v2/Services/VAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Verifications/VEXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
}  """

"""   output speared  STEEP 3  
{
  "sid": "VEXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "service_sid": "VAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "account_sid": "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "to": "+15017122661",
  "channel": "sms",
  "status": "approved",
  "valid": true,
  "amount": null,
  "payee": null,
  "sna_attempts_error_codes": [],
  "date_created": "2015-07-30T20:00:00Z",
  "date_updated": "2015-07-30T20:00:00Z"
}  """
