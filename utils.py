import json
import yaml
import firebase_admin
from firebase_admin import firestore, storage, credentials
from twilio.rest import Client

def get_date_time():
    """
    Returns the current formatted date and time (standard across our server)
    """

class Singleton(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        """
        Make me your metaclass to be a singleton! It's *magic*
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class AuthHolder(metaclass=Singleton):
    
    def __init__(self):
        """
        Singleton to hold auth/client objects for various APIS so they can be conveniently passed around
        """
        self.__config = ConfigProvider()
        self.__firestore = self.__get_firestore_auth_obj()
        self.__twilio = self.__get_twilio_auth_obj()

    def __get_firestore_auth_obj(self):
        try:
            cred = credentials.Certificate(self.__config.fs_auth_key_filepath)
            firebase_admin.initialize_app(cred)
            return (firestore.client())
        except Exception as e:
            print("A critical error has occured trying to connect to the Firestore database. Please verify your keys / config.yml\n", e)
            exit(1)

    def __get_twilio_auth_obj(self):
        try:
            return(Client(self.__config.twilio_acc_sid, self.__config.twilio_auth_token))
        except Exception as e:
            print("A critical error has occured while trying to connect to the Twilio SMS service. Please verify your keys / config.yml\n", e)
            exit(1)

    def get_fs_auth(self):
        return self.__firestore

    def get_twil_auth(self):
        return self.__twilio

class FileManager:

    _registered_filetypes = {"yml", "json"}

    _filepath = None
    _filetype = None

    def __init__(self, filepath, fm_id="Default"):
        """Constructor for FileManager. Supports YML and JSON formatted files. R/W

        :param str filepath: absolute or relative file path
        :param str fm_id: Optional, defaults to "Default"
        """ 

        self._fm_id = fm_id

        if filepath != None:
            self._filepath = filepath
            self._filetype = self.identify_file(self._filepath)

        self._functional = self.__verify_functionality()


    def __verify_functionality(self):

        if self.read_file() != None:
            # print(f"{self._filepath} of Type {self._filetype} identified")
            return True
        else:
            print(f"{self._fm_id} Cannot Manage {self._filepath} of Type {self._filetype}")
            return False


    def read_file(self):
        """
        Reads a json/yml file into a dict

        :returns dict file: Dict of the file's contents
        """

        file = None

        if self._filetype in self._registered_filetypes:
            try:
                with open(self._filepath) as f:
                    if self._filetype == "yml":
                        file = yaml.load(f, Loader=yaml.FullLoader)
                    elif self._filetype == "json":
                        file = json.load(f)
            except FileNotFoundError as e:
                print(f"File not Found: {self._filepath}\n", e)
            except json.JSONDecodeError as e:
                print(f"Error Decoding {self._filetype} File {self._filepath}:\n", e)
            except yaml.YAMLError as e:
                print(f"Error Decoding {self._filetype} File {self._filepath}:\n", e)
            except Exception as e:
                print(f"Unexpected Error Reading: {self._filepath}\n", e)
        else:
            print(f"Unregistered Filetype Detected: {self._filetype}")

        return file


    def write_file(self, content, output_filepath=None):
        """
        Writes a file

        :param content: What to write to the file. Uses yaml.dump() or json.dump() depending on the output_filepath
        :param str output_filepath: Optional, defaults to None. Sets the location and name of the output file. Should end in .yml or .json 
        """

        filetype = None

        if output_filepath == None:
            output_filepath = self._filepath
            filetype = self._filetype
        else:
            filetype = self.identify_file(output_filepath)

        if filetype in self._registered_filetypes:
            try:
                with open(output_filepath, "w") as f:
                    if self._filetype == "yml":
                        yaml.dump(content, f)
                    elif self._filetype == "json":
                        json.dump(content, f)
            except Exception as e:
                print(f"Error Writing File: {output_filepath}\n", e)
        else:
            print(f"Unregistered Filetype Detected: {filetype}")

        if output_filepath == self._filepath:
            self._functional = self.__verify_functionality()


    def identify_file(self, filepath):
        file_components = filepath.split(".")
        if len(file_components) == 2:
            return file_components[-1]
        else:
            return None


    def is_functional(self):
        return self._functional


def get_key(value, dict):

    key = None

    for k, v in dict.items():
        if v == value:
            key = k

    if key == None:
        print(f"Could not Locate Key for {value} in {dict}")

    return key

class ConfigProvider(metaclass=Singleton):

    def __init__(self):
        """
        Holds immutable data from config.yml
        """
        try:
            self.__config_file = FileManager("config.yml")
            self.__config_dict = self.__config_file.read_file()
            self.fs_auth_key_filepath = self.__config_dict["fs_auth_key_filepath"]
            self.fs_project_name = self.__config_dict["fs_project_name"]
            self.twilio_acc_sid = self.__config_dict["twilio_acc_sid"]
            self.twilio_auth_token = self.__config_dict["twilio_auth_token"]
            self.twilio_from_phone = self.__config_dict["twilio_from_phone"]
        except Exception as e:
            print("ERROR: Some or all of the keys are missing from config.yml or config.yml has not been created from config.yml.TEMPLATE. Please correct this or the server will not start.\n", e)

class InfoProvider(metaclass=Singleton):

    def __init__(self):
        """
        Holds immutable data from info.yml
        """
        try:
            self.__info_file = FileManager("info.yml")
            self.__info_dict = self.__info_file.read_file()
            self.version = self.__info_dict["version"]
            self.license = self.__info_dict["license"]
            self.pretty_name = self.__info_dict["pretty_name"]
            self.authors = self.__info_dict["authors"]
        except Exception as e:
            print("ERROR: Some or all of the keys are missing from info.yml or info.yml has not been created. Please correct this or the server will not start.\n", e)