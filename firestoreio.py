from utils import AuthHolder

class FirestoreIO():

    def __init__(self):
        """
        NEW class for talking to Firestore Database. See the functions for what each does. You can make this object ONCE and use it over and over again.

        :param firebase_auth: An authenticated firebase object. You can get this from the authwrapper module
        
        Functions:
        write_doc(): Writes a document to the Firestore
        read_doc(): Reads a document from the Firestore
        read_docs_by_query(): Searches all docs in a Firestore collection that match a given query. Returns all the matches as dicts in a dict.
        does_doc_exist(): Checks if a document exists on the Firestore
        delete_doc(): Deletes a document and any nested structures
        """
        self.__authy = AuthHolder()
        self.__firebase_auth = self.__authy.get_fs_auth()

    def write_doc(self, path, write_dict):
        """
        Write a document to Firestore database. Supports subcollections/docs. Will construct anything that doesn't exist on the way to writing your document.

        :param str path: The path to the object. Ex: "/Transactions/00001" Must begin in a / and end without one. Your document name should be at the end of your path.
        :param dict write_dict: This is a dict that will be written as the body of your document.


        :returns: True if we executed the write, False if an error occured on the Firestore write command, None if an error occured locally.
        Ex: FirestoreIO.write_doc("/Transactions/00001/Selfies/Selfie_Links", {links: ["https://...", "...", "..."]})
        """
        try:
            doc_name = self.__is_valid_document_path(path)[1]
        except Exception as e:
            print("ERROR: FirestoreIO.write_doc(): Invalid document path. Check your path. Returning None")
            return None
        if(doc_name == ""):
            print("ERROR: FirestoreIO.write_doc(): doc_name is '' Check your path. Returning None")
            return None
        coll_handle = self.__make_coll_handle(path)
        try:
            coll_handle.document(doc_name).set(write_dict, merge=True)
        except Exception as e:
            print(e)
            return False
        return True

    def read_doc(self, path):
        """
        Read a whole document to a dictionary based on the document's path. No search functionality. You must know the document's name and location in advance.

        :param str path: The path to your document. Must begin with / and must not end with /. Ex: "/Transactions/00001" Your doc name must be at the end of your path!

        :returns dict: Your doc's data. If None, you did something wrong or it doesn't exist!

        Example Usage: doc_dict = FirestoreIO.read_doc("/Transactions/00001")
        """
        doc_name = None
        try:
            doc_name = self.__is_valid_document_path(path)[1]
        except Exception as e:
            print("ERROR: FirestoreIO.read_doc(): Invalid document path. Check your path. Returning None")
            return None
        if(doc_name == ""):
            print("ERROR: FirestoreIO.read_doc(): doc_name is ''. Returning None")
            return None
        coll_handle = self.__make_coll_handle(path)
        try:
            doc = coll_handle.document(doc_name).get()
            if(doc.exists):
                return doc.to_dict()
            else:
                print("WARNING: FirestoreIO.read_doc(): Your doc does not exist! Returning None")
                return None
        except Exception as e:
            print("ERROR: FirestoreIO.read_doc(): An error occured trying to read your doc.")
            print(e)
            return None

    def does_doc_exist(self, path):
        """
        Check if a document exists given it's path.

        :param str path: The path to the document

        :returns boolean: True if exists, False otherwise. Will return None if an error occurs. Please accomodate this.
        """
        doc_name = None
        try:
            doc_name = self.__is_valid_document_path(path)[1]
        except Exception as e:
            print("ERROR: FirestoreIO.does_doc_exist(): Invalid document path. Check your path. Returning None")
            return None
        if(doc_name is None or doc_name == ""):
            print("ERROR: FirestoreIO.does_doc_exist(): doc_name is None or ''. Returning None")
            return None
        coll_handle = self.__make_coll_handle(path)
        try:
            doc = coll_handle.document(doc_name).get()
            if(doc.exists):
                return True
            else:
                return False
        except Exception as e:
            print("ERROR: FirestoreIO.does_doc_exist() encountered an unknown error trying to talk to Firestore. Returning None and printing stacktrace")
            print(e)
            return None

    def read_docs_by_query(self, collection_path, query_list):
        """Takes the following params to construct and execute a query on all of the Docs in a Collection:

        :param str collection_path: A String formatted path that must start with a / and end with a / (last folder must always be a collection)
        :param list query_list: A list used for formulating the query.

        :returns dict: A dict where the matching Doc id is the key, and the document's Dict is the Doc's dict. 
        
        Example Usage: query_results = FirestoreIO.read_docs_by_query("/Transactions/", ["phone_num", "==", "412-420-6969"])
        
        Example Results: {'00001-001-1-00001-0-000001': {'name': 'connor alexander', 'phone_num': '412-420-6969', ...}, {...}, ...}
        """
        path = None
        try:
            path = self.__is_valid_collection_path(collection_path)
            if(path is None):
                raise Exception()
        except Exception as e:
            print("ERROR: FirestoreIO.read_docs_by_query(): Collection path is invalid. Returning None")
            return None
        if(path == ""):
            print("ERROR: FirestoreIO.read_docs_by_query(): path was ''. Returning None")
        ## Make coll_handle. Can't use class's self.__make_coll_handle() because it uses __is_valid_document_path()
        coll_handle = None
        try:
            coll_handle = self.__firebase_auth.collection(str(path))
            if(coll_handle is None):
                raise Exception()
        except Exception as e:
            print("ERROR: FirestoreIO.read_docs_by_query(): An Exception occured trying to make the collection handle. Unable to continue. Returning None")
            print(e)
            return None
        ## End make coll_handle
        query_ref = self.__construct_query_ref(coll_handle, query_list)
        if(query_ref is None):
            print("ERROR: FirestoreIO.read_docs_by_query(): Unable to construct a query ref. Returning None")
            return None
        results_dict = self.__execute_query(query_ref)
        if(results_dict is None):
            print("ERROR: An Error occured while trying to execute your query. Returning None")
            return None
        return results_dict

    def delete_doc(self, path):
        """
        Deletes a given document from a path.

        :param str path: The path of the document. Must begin but not end in /

        :returns True: Document is deleted OR document doesn't exist
        :returns False: If error
        """
        if(self.does_doc_exist(path) is False):
            return True
        doc_name = None
        try:
            doc_name = self.__is_valid_document_path(path)[1]
        except Exception as e:
            print("ERROR: FirestoreIO.delete_doc(): Invalid document path. Check your path. Returning None")
            return None
        if(doc_name is None or doc_name == ""):
            print("ERROR: FirestoreIO.delete_doc(): doc_name is None or ''. Returning None")
            return None
        coll_handle = self.__make_coll_handle(path)
        try:
            coll_handle.document(doc_name).delete()
        except Exception as e:
            print("ERROR: FirestoreIO.delete_doc(): An Unknown exception occured trying to tell Firestore to delete your document. Returning False")
            print(e)
            return False
        return True
            
    def copy_doc(self, from_path, to_path, recursive=False, delete_old=False, overwrite_if_exists=False, overwrite_strategy="delete"):
        """
        WARNING: recursive=True IS NOT YET IMPLEMENETED
        Copy a document in the Firestore

        :param str from_path: Path to the document you wish to copy. Must begin in / but not end in it.
        :param str to_path: Path (including name) of the document you want to copy to.
        :param bool recurisve: [OPTIONAL DEF: FALSE] - Recursively copy and documents/collections inside your top level doc.
        :param bool overwrite_if_exists: [OPTIONAL DEF: FALSE] - Should we overwrite an existing document in your to_path location?
        :param str overwrite_strategy: [OPTIONAL DEF: "delete"] - if overwrite_if_exists is true, how should we handle this.
            Strategies:
                "delete" - The default strategy. We will delete the document at to_path, and then write your document there.
                    Please note that if recursive=True, we will handle this by deleting the top level document, and all of its children. It is too complicated to recursively keep track of the documents beneath the surface level.
                "merge" - We will write directly onto the existing document. This will merge, but some data may be lost if there are same keys but different values between the source and destination docs
                    Please note that if recursive=True, we will handle this by writing one document on top of the other. If there are sub docs/colls that are in the dest but not the source, they will remain.

        :returns True: If we can copy the document without error on the Firestore API calls.
        :returns False: If we don't copy the document because of your inputs.
        :returns None: If an error occurs on a Firestore API call
        """
        # Check if our first doc actually exists
        if(self.does_doc_exist(from_path) is False):
            print("ERROR: FirestoreIO.copy_doc(): Trying to copy from a doc that doesn't exist")
            return False
        # Refuse to copy if overwrite_if_exists is False and the document exists
        if(overwrite_if_exists is False):
            if(self.does_doc_exist(to_path)):
                print("ERROR: FirestoreIO.copy_doc(): Trying to copy to a doc that already exists. Default is to not do this. You can change this via overwrite_if_exists=True if you want.")
                return False
            # Base case copy a document non-recursive
            if(recursive is False):
                try:
                    from_doc = self.read_doc(from_path)
                    self.write_doc(to_path, from_doc)
                    return True
                except Exception as e:
                    print("ERROR: FirestoreIO.copy_doc(): An Exception occured while trying to copy your document. Returning None")
                    print(e)
                    return None
            if(recursive is True):
                r_result = self.__recursive_copy(from_path, to_path)
                if(r_result is True and delete_old is True):
                    d_result = self.delete_doc(from_path)
                    if(d_result is not True):
                        print("ERROR: FirestoreIO.copy_doc() An unknown error occured while trying to delete the from_doc. Returning False")
                        return False
                return r_result
        if(overwrite_if_exists is True):
            if(recursive is False):
                if(overwrite_strategy == "delete"):
                    d_results = self.delete_doc(to_path)
                    if(d_results is False or d_results is None):
                        print("ERROR: FirestoreIO.copy_doc(): An Unknown Exception occured while trying to delete your to_document. Cannot continue. Returning False")
                        return False
                from_doc = self.read_doc(from_path)
                if(from_doc is None):
                    print("ERROR: FirestoreIO.copy_doc(): An unknown Exception occured while trying to get your from_doc. Returning False")
                    return False
                w_results = self.write_doc(to_path, from_doc)
                return w_results
            if(recursive is True):
                if(overwrite_strategy == "delete"):
                    d_result = self.delete_doc(to_path)
                    if(d_result is not True):
                        print("ERROR: FirestoreIO.copy_doc() An unknown error occured while trying to delete the to_doc. Returning False")
                        return False   
                r_result = self.__recursive_copy(from_path, to_path)
                if(r_result is True and delete_old is True):
                    d_result = self.delete_doc(from_path)
                    if(d_result is not True):
                        print("ERROR: FirestoreIO.copy_doc() An unknown error occured while trying to delete the from_doc. Returning False")
                        return False
                return r_result
                

    def __recursive_copy(self, from_path, to_path, name_same=False):
        # Populate our values for navigate and R/W
        from_doc_name = self.__is_valid_document_path(from_path)[1]
        if(name_same is False):
            to_doc_name = self.__is_valid_document_path(to_path)[1]
        else:
            to_doc_name = from_doc_name
        from_coll_handle = self.__make_coll_handle(from_path)
        to_coll_handle = self.__make_coll_handle(to_path)
        # Lets see if this document has subcollections
        colls = from_coll_handle.document("from_doc_name")

    #### INTERNAL METHODS START HERE ####

    def __make_coll_handle(self, path):
        """
        INTERNAL METHOD. Make collection handle for write_doc() function

        :param auth: Firebase auth object
        :param str path: Path
        """
        path_chopped = self. __is_valid_document_path(path)[0]
        if(path_chopped == None):
            raise Exception("ERROR: FirestoreIO.__make_coll_handle(): Path is not valid. Cannot continue.")
        else:
            try:
                collection_handle = self.__firebase_auth.collection(path_chopped)
                return collection_handle
            except Exception as e:
                print("ERROR: An FirestoreIO.__make_coll_handle(): An Exception occured when trying to create the collection handle. Stacktrace: ")
                print()
                print(e)

    def __is_valid_document_path(self, path):
        if(path == None or path == ""):
            print(f"WARNING: FirestoreIO.__is_valid_document_path(): Path is null or empty! Your Path: {path}")
            return None
        elif(path[0] != "/"):
            print(f"WARNING: FirestoreIO.__is_valid_document_path(): Path MUST begin with / Your Path: {path}")
            return None
        elif(path[-1] == "/"):
            print(f"WARNING: FirestoreIO.__is_valid_document_path(): Path must not end with / Your Path: {path}")
            return None
        else:
            list_slash_pos = []
            count = 0
            forward_slash_count = 0
            for char in path:
                if(char == "/"):
                    forward_slash_count += 1
                    list_slash_pos.append(count)
                count += 1
            chopped_path = path[1:list_slash_pos[len(list_slash_pos)-1]]
            document_name = path[list_slash_pos[len(list_slash_pos)-1]+1:len(path)]
            if((forward_slash_count % 2 != 0)):
                print("WARNING: FirestoreIO.__is_valid_document_path(): Path has an odd number of /. This means you are trying to operate on an empty collection. BAD!")
                return None
            else:
                return [chopped_path, document_name]

    def __is_valid_collection_path(self, path):
        """Check if a collection path is valid
           :param str path: The path to the collection of choice.

           :returns str None: Returns a str if path is valid and trimmed correctly, otherwise returns None if something goes wrong. 
        """
        if(path == None or path == ""):
            print(f"WARNING: FirestoreIO.__is_valid_collection_path(): Collection Path is null or empty! Your path: {path}")
            return None
        elif(path[0] != "/"):
            print(f"WARNING: FirestoreIO.__is_valid_collection_path(): Collection Path MUST begin with / Your path: {path}")
            return None
        elif(path[-1] != "/"):
            print(f"WARNING: FirestoreIO.__is_valid_collection_path(): Collection Path MUST end with / Your path: {path}")
            return None
        else:
            chopped_path = path[1:len(path)-1]
            return chopped_path;

    def __construct_query_ref(self, collection_handle, query_list):
        """Construct the query reference
           
           :param collection_handle: The collection handle made by __make_collection_handle().
           :param list query_list: A list used for formatting the query.

           :returns: A query reference made with collection_handle.where("", "", "")

           NOTE: If using spaces in your keys (NOT the collection), you must escape them:
           https://stackoverflow.com/a/53048641
        """
        if(len(query_list) > 3):
            print("ERROR: FirestoreIO.__construct_query_ref(): You tried to pass a query_list with more than 3 elements")
            return None
        counter = 0
        while(counter < len(query_list)):
            if(isinstance(query_list[counter], str) is False):
                print("WARNING: FirestoreIO.__construct_query_ref(): You tried to pass something that wasn't a string into your query_list! We will cast for you this time, but please fix it")
                query_list[counter] = str(query_list[counter])
            counter += 1
        try:
            query_ref = collection_handle.where(f'{query_list[0]}', f'{query_list[1]}', f'{query_list[2]}')
            return query_ref
        except Exception as e:
            print("ERROR: FirestoreIO.__construct_query_ref(): An unknown error occured trying to construct your query_ref for you. Please investigate.")
            print(e)
            return None

    def __execute_query(self, query_ref):
        """Execute Firestore read query
           :param query_ref: A query_ref returned by __construct_query_ref()

           :returns dict docs_dicts_dict: Dictionary where keys are doc ids and values are document dictionaries made with doc.to_dict(). If no matches to query, empty. If err, None
        """
        doc_dicts_dict = {}
        docs = None
        try:
            # This said .stream() is preferred to a depreciated .get() https://firebase.google.com/docs/firestore/query-data/queries
            docs = query_ref.stream()
            # Convert from a "generator" obj into a list obj
            docs = list(docs)
        except Exception as e:
            print(f"ERROR: FirestoreIO.__execute_query(): (3)An Exception occured while trying to execute your query! Returning None Stacktrace: \n\n{e}")
            print(e)
            return None
        
        for doc in docs:
            if str(doc.id) in doc_dicts_dict:
                print(f"WARNING: FirestoreIO.__execute_query(): Duplicate key in doc_dicts_dict, this is a firestore data structure issue! Will overwrite previous entry!")
                doc_dicts_dict[f'{doc.id}'] = doc.to_dict()
            else:
                doc_dicts_dict[f'{doc.id}'] = doc.to_dict()
        return doc_dicts_dict

    # For testing purposes TODO: refactor because we need an equivalent to this
    def get_collection(self, collection_name):
        return self.__firebase_auth.collection(collection_name).get()
