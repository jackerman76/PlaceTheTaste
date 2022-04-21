from firestoreio import FirestoreIO
from twilio.base.exceptions import TwilioRestException
from utils import AuthHolder, ConfigProvider
import random

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
        except TwilioRestException as e:
            print("Twilio sending failure.\n", e)

class TwoFactorAuthManager():

    def __init__(self, username):
        """
        Class to handle 2fa functions simply

        :param str username:

        You can always check .functional var to see if the username and phone number you gave were valid

        Function Index:
        init_new_2fa_code(): Generate's a 2FA code for this user and stores it in the database, sends an SMS to the user
        validate_2fa_code(code): Check a 2FA code against a given user to see if that code is valid (hasn't already been used, matches the one on file) 
        """
        self.__fsio = FirestoreIO()
        self.__twil = TwilioDispatch()
        self.functional = True
        self.__DOC_BASE = "/Users"
        self.__username = username
        self.__user_doc = None
        self.__check_valid() # Updates user doc when it calls self.__get_user_doc()
        if self.functional == False:
            print(f"Warning: Unable to instantiate 2FA Manager for user: {self.__username} {self.__phone_number}")

    def __check_valid(self):
        ex = self.__fsio.does_doc_exist(f"{self.__DOC_BASE}/{self.__username}")
        if ex != True:
            print("ERROR: Unable to validate 2fa code with non-functional user. Are you missing information in your object?")
            self.functional = False
            return
        else:
            self.__get_user_doc()
            return
            
    def __get_user_doc(self):
        doc = self.__fsio.read_doc(f"{self.__DOC_BASE}/{self.__username}")
        if doc == None:
            self.functional = False
            return
        else:
            self.functional = True
            self.__user_doc = doc
            return

    def __generate_2fa_code(self):
        """
        Get a code
        """
        num = random.randint(1000000, 9999999)
        return str(num)

    def __update_user_2fa(self, code):
        """
        Log the code and mark the code as valid
        """
        if self.functional != True:
            print("WARNING: Not adding 2fa to database for non-functional user")
            return
        self.__get_user_doc() # Make sure we're up to date
        self.__user_doc["2fa_code"] = str(code)
        self.__user_doc["2fa_valid_now"] = True
        res = self.__write_user()
        return res

    def __write_user(self):
        """
        Write the current user dict to the database
        """
        res = self.__fsio.write_doc(f"{self.__DOC_BASE}/{self.__username}", self.__user_doc)
        if res != True:
            print("ERROR: An error occured writing user to firestore!")
        return res

    def __send_sms(self, code):
        if self.functional != True:
            print("Error: Unable to send SMS from non-functional 2fa object. Check username is valid")
            return
        msg = f"Your One Time Code for Place The Taste is {code}."
        self.__twil.dispatch(self.__user_doc["phone_number"], msg)
        return

    def init_new_2fa_code(self):
        """
        Generates a code, logs it in the database, and texts the user!
        :returns: True if this all worked, False in any other case/error
        """
        if self.functional != True:
            print("ERROR: Unable to init 2fa code on non-functional object")
            return
        
        code = self.__generate_2fa_code() # Generate code
        res = self.__update_user_2fa(code) # Add code to database, mark code as valid, and write user info
        self.__send_sms(code)
        return res

    def validate_2fa_code(self, code):
        """
        Returns true or false
        """
        code = str(code)
        self.__get_user_doc() # Make sure we're up to date
        if self.functional != True:
            print("ERROR: Unable to validate 2fa code with non-functional user. Are you missing information in your object?")
            return False
        else:
            try:
                if code == self.__user_doc["2fa_code"] and self.__user_doc["2fa_valid_now"] == True:
                    self.__user_doc["2fa_valid_now"] = False # We're invalidating it now that it's been used once
                    self.__write_user() # Notify the database that it's invalid
                    return True # Return true because the code was valid
                else:
                    return False
            except:
                return False # This takes care of an edge case where a user file might not have 2fa yet but tries to use 2fa somehow (shouldn't really be possible but better safe than)