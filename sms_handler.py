from firestoreio import FirestoreIO
from twilio.base.exceptions import TwilioRestException
from utils import AuthHolder, ConfigProvider

class TwilioDispatch():

    def __init__(self):
        """
        Twilio Dispatcher. Make this once and use the dispatch() method to send SMS
        """
        self.__auth = AuthHolder()
        self.__config = ConfigProvider()
        self.__twilio_from_phone = self.__config.twilio_from_phone
        self.__tw_auth = self.__auth.get_twil_auth()

    def dispatch(self, to_phone, msg_str):
        """
        Send a twilio SMS message
        :param str to_phone: Phone to send SMS to
        :param str msg_str: Message to send
        """
        try:
            message = self.__tw_auth.messages.create(
                body = msg_str,
                from_ = self.__twilio_from_phone,
                to = to_phone
            )
            message.sid # this line actually sends the message
        except Exception as e:
            print("Twilio sending failure.\n", e)