#file extension practice 2
#playing around with file extensions to get this to work
# note_types = [ {"name": "Scan Type", "radio_name": "Scan Type", "file_location": "ScanTypeNotes", "table_col_settings":[{"column": "polygon id", "wraplength":10, "side": "left", "width": 10, "fill": False, "btns": None},
#                                                                                                                                     {"column": "user", "wraplength":100, "side": "left", "width": 15, "fill": False, "btns": None},
#                                                                                                                                     {"column": "note", "wraplength":285, "side": "left", "width": 40, "fill": False, "btns": None},
#                                                                                                                                     {"column": "date", "wraplength":100, "side": "left", "width": 10, "fill": False, "btns": None},
#                                                                                                                                     {"column": "time", "wraplength":30, "side": "left", "width": 10, "fill": False, "btns": None}
#                                                                                                                                     ],
#                                                                                                                                     "details_required": ['note', 'username', 'year', 'patient', 'date', 'time'],
#                                                                                                                                     # "file_sub_extension": {"validator_key": "scantype notes", "validator_val": "[]", "key_val_to_append_to": "scantype notes", "level": None}
#                                                                                                                                     "file_sub_extension": {"validator_key": "scantype notes", "validator_val": False, "key_val_to_append_to": "scantype notes", "level": None}
#                                                                                                                                     },
#                     {"name": "Slice", "radio_name": "Current Slice", "file_location": "slice_name" + "Polygon & Slice Notes", "table_col_settings":[{"column": "user", "wraplength":100, "side": "left", "width": 15, "fill": False, "btns": None},
#                                                                                                                                     {"column": "note", "wraplength":285, "side": "left", "width": 40, "fill": False, "btns": None},
#                                                                                                                                     {"column": "date", "wraplength":100, "side": "left", "width": 10, "fill": False, "btns": None},
#                                                                                                                                     {"column": "time", "wraplength":30, "side": "left", "width": 10, "fill": False, "btns": None}
#                                                                                                                                     ],
#                                                                                                                                     "details_required": ['note', 'username', 'year', 'patient', 'scan_type', 'date', 'time'],
#                                                                                                                                     # "file_sub_extension": {"slice notes": "slice notes", "key_append": "slice notes", "level": None}
#                                                                                                                                     "file_sub_extension": {"validator_key": "slice notes", "validator_val": False, "key_val_to_append_to": "slice notes", "level": None}
#                                                                                                                                     },
#                     {"name": "Polygon", "radio_name": "Selected Polygon", "file_location": "slice_name" + "Polygon & Slice Notes", "table_col_settings":[{"column": "user", "wraplength":100, "side": "left", "width": 15, "fill": False},
#                                                                                                                                     {"column": "note", "wraplength":285, "side": "left", "width": 40, "fill": False},
#                                                                                                                                     {"column": "date", "wraplength":100, "side": "left", "width": 10, "fill": False},
#                                                                                                                                     {"column": "time", "wraplength":30, "side": "left", "width": 10, "fill": False}
#                                                                                                                                     ],
#                                                                                                                                     "details_required": ['note', 'username', 'date', 'time'],
#                                                                                                                                     # "file_sub_extension": {"polygon data": "polygon data", "key_append": "polygon data", "level": {"id": 1, "key_append": "notes", "level": None}
#                                                                                                                                     "file_sub_extension": {"validator_key": "polygon data", "validator_val": False, "key_val_to_append_to": "polygon data", "level": {"validator_key": "id", "validator_val": 2, "key_val_to_append_to": "notes", "level": None}}
#                                                                                                                                     }] #if validator value is false then just append to validator key

# note_details_example = {'id': 0, 'note': 'Another Note', 'username': None, 'year': '2018', 'patient': 'PR150', 'date': '19-08-2020', 'time': '15:57'}
# note_details = {'id': 0, 'note': 'Another Note', 'username': None, 'year': '2018', 'patient': 'PR150', 'date': '19-08-2020', 'time': '15:57'}
#
# # data = [{"scantype notes": [note_details_example]}]
# data = [{"polygon data": [{
#                             "id": 1,
#                             "tag": "Suspicious: pi-rad 4",
#                             "slice": "PR150_01_0006_002_t2-axial",
#                             "co-ordinates": [
#                         [
#                             33.09374999999999,
#                             108.88125
#                         ],
#                         [
#                             33.09374999999999,
#                             74.75
#                         ],
#                         [
#                             56.47499999999999,
#                             53.78750000000001
#                         ],
#                         [
#                             80.39374999999998,
#                             54.59375
#                         ],
#                         [
#                             80.39374999999998,
#                             86.84375
#                         ],
#                         [
#                             66.14999999999998,
#                             103.2375
#                         ],
#                         [
#                             46.79999999999999,
#                             109.41875
#                         ]
#                     ]
#                     },
#                     {
#                                                 "id": 2,
#                                                 "tag": "Suspicious: pi-rad 4",
#                                                 "slice": "PR150_01_0006_002_t2-axial",
#                                                 "co-ordinates": [
#                                             [
#                                                 33.09374999999999,
#                                                 108.88125
#                                             ],
#                                             [
#                                                 33.09374999999999,
#                                                 74.75
#                                             ],
#                                             [
#                                                 56.47499999999999,
#                                                 53.78750000000001
#                                             ],
#                                             [
#                                                 80.39374999999998,
#                                                 54.59375
#                                             ],
#                                             [
#                                                 80.39374999999998,
#                                                 86.84375
#                                             ],
#                                             [
#                                                 66.14999999999998,
#                                                 103.2375
#                                             ],
#                                             [
#                                                 46.79999999999999,
#                                                 109.41875
#                                             ]
#                                         ], "notes": [note_details_example]
#                                         }],
#                     }]
# data = []

##This functionality below looks to add a note at different depths of a JSON file that also requires validation. The depths are given by a
#dict such as the notetypes dict that has a key that is structured in a particular way
#eg. "file_sub_extension": {"validator_key": "polygon data", "validator_val": False, "key_val_to_append_to": "polygon data", "level": {"validator_key": "id", "validator_val": 2, "key_val_to_append_to": "notes", "level": None}}
#to explain the above the validator key is always looked for in the json and if found is then validated against the validator value if the validator value IS NOT false.
# if the validator key is not found it is created & the note is appended to a list that become's that key's value
# if the validator key is found then the key to append is also looked for & if that is found, the note is appended to that value UNLESS there is a deeper level i.e the level is NOT None
# if level is not None, then the function continues recursively
# A lot of the time the key to append to is the same as the validator key

class jsonNoteAdder:
    def __init__(self, sub_extension, note, data):
        self.sub_extension = sub_extension
        self.note = note
        self.data = data

        if self.sub_extension == None: #if there is no extension  - this isn't the case in my code
            self.data.append(self.note)
        elif self.sub_extension != None: #if there is extension
            # file_extension_dict = self.sub_extension
            if len(self.data) == 0: #if the file is empty then add an empty dictionary to allow the function to run
                print("WHAT IS LENGTH", self.data)
                self.data.append({})
            self.add_to_data_file(self.data, self.sub_extension, self.note) #call the function

    #Function below creates a list, and adds the note, basically where the key was not present in the dict yet
    def create_list(self, item, new_key, note):
        list = []
        item[new_key] = list
        item[new_key].append(self.add_id_0(note)) #add an id of 0 as only come in here if the case

    #Function below provides the id by taking the last item in the list of the key to append the note too and increments it. This means the id will always be unique
    def add_id(self, item, key, note):
        print(item)
        print(key)
        if len(item[key]) > 0:
            last_item = item[key][len(item[key]) - 1]
            note['id'] = last_item['id'] + 1
        elif len(item[key]) == 0: #if there are no notes in the list but the list is already present
            note['id'] = 0


    #Function just add an id of 0 to a note
    def add_id_0(self, note):
        note['id'] = 0
        return note

    #Function below looks to see if the key to append the note too is in the dict, if so it then checks to see if there is another level of dictionary to go into, it calls the find id function also
    def find_if_val_present_in_dict(self, item, file_extension_dict, note):
        if file_extension_dict['key_val_to_append_to'] in item:
            # print("Value to append present in dict")
            if file_extension_dict['level'] == None:
                self.add_id(item, file_extension_dict['key_val_to_append_to'], note) #find id & add to note
                item[file_extension_dict['key_val_to_append_to']].append(note) #append the note to the item

            else:
                new_file_extension_dict = file_extension_dict['level']
                self.add_to_data_file(item[file_extension_dict['key_val_to_append_to']], new_file_extension_dict, note) #recursively call function to go again

        else:
            # print("Value to append to not present in dict")
            self.create_list(item, file_extension_dict['key_val_to_append_to'], note) #add the note in a list that is newly added as the key to append to wasnt available so needs to be added itself

    def add_to_data_file(self, list_of_dicts, file_extension_dict, note):
        for item in list_of_dicts:
            if file_extension_dict['validator_key'] in item: #checks if the validation key is present, this may be the same as the key to append to but not always
                print("validation key present")

                if file_extension_dict['validator_val'] != False: #if there is a validation needed for the note to be added eg if the polygon id needs to be found
                    #find validation
                    if item[file_extension_dict['validator_key']] == file_extension_dict['validator_val']:
                        print("VALIDATION CORRECT")
                        #valiadation correct
                        self.find_if_val_present_in_dict(item, file_extension_dict, note)
                    else:
                        print("VALIDATION NOT CORRECT")
                        #will go to next item to then validate
                else:
                    #no validation needed, find if key to append to is present
                    self.find_if_val_present_in_dict(item, file_extension_dict, note)

            else:
                print("Validation key not present in dict ")
                #HERE I AM ADDING THE NOTE TO THE VALIDATION KEY NOT KEY TO APPEND TO
                self.create_list(item, file_extension_dict['validator_key'], note) #add the note in a list that is newly added as the key the validation key wasnt available so needs to be added itself

class jsonNoteShow:
    def __init__(self, sub_extension, data):
        self.sub_extension = sub_extension
        self.data = data
        self.returned_data = None

        if self.sub_extension == None: #if there is no extension  - this isn't the case in my code
            self.returned_data = None
        elif self.sub_extension != None: #if there is extension
            if len(self.data) == 0:
                self.returned_data = None
            else:
                self.show_notes(self.data, self.sub_extension)
    #Function below looks to see if the key to append the note too is in the dict, if so it then checks to see if there is another level of dictionary to go into, it calls the find id function also
    def get_values(self, item, file_extension_dict):
        if file_extension_dict['key_val_to_append_to'] in item:
            if file_extension_dict['level'] == None:
                formatted_data = []
                print("HERR", item[file_extension_dict['key_val_to_append_to']])
                for record in item[file_extension_dict['key_val_to_append_to']]:
                    formatted_data.append(record)
                self.returned_data = formatted_data
            else:
                new_file_extension_dict = file_extension_dict['level']
                self.show_notes(item[file_extension_dict['key_val_to_append_to']], new_file_extension_dict) #recursively call function to go again
        else:
            self.returned_data = None #if not the case then have to return None

    def show_notes(self, list_of_dicts, file_extension_dict):
        for item in list_of_dicts:
            if file_extension_dict['validator_key'] in item: #checks if the validation key is present, this may be the same as the key to append to but not always
                print("validation key present")

                if file_extension_dict['validator_val'] != False: #if there is a validation needed for the note to be added eg if the polygon id needs to be found
                    #find validation
                    if item[file_extension_dict['validator_key']] == file_extension_dict['validator_val']:
                        print("VALIDATION CORRECT")
                        #valiadation correct
                        self.get_values(item, file_extension_dict)
                        break #if validation found then can break the loop & return
                    else:
                        self.returned_data = None
                        print("VALIDATION NOT CORRECT")
                        #will go to next item to then validate
                else:
                    #no validation needed, find if key to append to is present
                    self.get_values(item, file_extension_dict)

            else:
                print("Validation key not present in dict ")
                #HERE I AM ADDING THE NOTE TO THE VALIDATION KEY NOT KEY TO APPEND TO
                self.returned_data = None

class jsonNoteEdit:
    def __init__(self, sub_extension, data, new_note, note_id):
        self.sub_extension = sub_extension
        self.data = data
        self.new_note = new_note
        self.note_id = note_id

        if self.sub_extension == None: #if there is no extension  - this isn't the case in my code
            print("NOTHING TO BE EDITED")
        elif self.sub_extension != None: #if there is extension
            if len(self.data) == 0:
                print("NOTHING TO BE EDITED")
            else:
                self.validate_presence(self.data, self.sub_extension)
    #Function below looks to see if the key to append the note too is in the dict, if so it then checks to see if there is another level of dictionary to go into, it calls the find id function also
    def edit_values(self, item, file_extension_dict):
        if file_extension_dict['key_val_to_append_to'] in item:
            if file_extension_dict['level'] == None:
                located = False
                for record in item[file_extension_dict['key_val_to_append_to']]:
                    if record['id'] == self.note_id: #locate by the passed in id
                        located = True
                        record['note'] = self.new_note #replace note with new note
                        record['user'] = record['user'] + " (ed.)" #to let the user know that the note was edited
                if not located:
                    print("EDIT HAS NOT BEEN MADE, RECORD NOT FOUND")
            else:
                new_file_extension_dict = file_extension_dict['level']
                self.validate_presence(item[file_extension_dict['key_val_to_append_to']], new_file_extension_dict) #recursively call function to go again
        else:
            self.returned_data = None

    def validate_presence(self, list_of_dicts, file_extension_dict):
        for item in list_of_dicts:
            if file_extension_dict['validator_key'] in item: #checks if the validation key is present, this may be the same as the key to append to but not always
                print("validation key present")

                if file_extension_dict['validator_val'] != False: #if there is a validation needed for the note to be added eg if the polygon id needs to be found
                    #find validation
                    if item[file_extension_dict['validator_key']] == file_extension_dict['validator_val']:
                        print("VALIDATION CORRECT")
                        #valiadation correct
                        self.edit_values(item, file_extension_dict)
                    else:
                        print("VALIDATION NOT CORRECT")
                        #will go to next item to then validate
                else:
                    #no validation needed, find if key to append to is present
                    self.edit_values(item, file_extension_dict)

            else:
                print("Validation key not present in dict.")

class jsonNoteDelete:
    def __init__(self, sub_extension, data, note_id):
        self.sub_extension = sub_extension
        self.data = data
        self.note_id = note_id

        if self.sub_extension == None: #if there is no extension  - this isn't the case in my code
            print("NOTHING TO BE DELETED")
        elif self.sub_extension != None: #if there is extension
            if len(self.data) == 0:
                print("NOTHING TO BE DELETED")
            else:
                self.validate_presence(self.data, self.sub_extension)
    #Function below looks to see if the key to append the note too is in the dict, if so it then checks to see if there is another level of dictionary to go into, it calls the find id function also
    def remove_values(self, item, file_extension_dict):
        if file_extension_dict['key_val_to_append_to'] in item:
            if file_extension_dict['level'] == None:
                located = False
                item[file_extension_dict['key_val_to_append_to']] = [rec for rec in item[file_extension_dict['key_val_to_append_to']] if rec['id'] != self.note_id]
                for record in item[file_extension_dict['key_val_to_append_to']]:
                    if record['id'] == self.note_id:
                        located = True
                    #delete
                if located:
                    print("DELETION HAS NOT BEEN MADE")

            else:
                new_file_extension_dict = file_extension_dict['level']
                self.validate_presence(item[file_extension_dict['key_val_to_append_to']], new_file_extension_dict) #recursively call function to go again
        else:
            print("key_val_to_append_to key not present, Deletion not made")

    def validate_presence(self, list_of_dicts, file_extension_dict):
        for item in list_of_dicts:
            if file_extension_dict['validator_key'] in item: #checks if the validation key is present, this may be the same as the key to append to but not always
                print("validation key present")

                if file_extension_dict['validator_val'] != False: #if there is a validation needed for the note to be added eg if the polygon id needs to be found
                    #find validation
                    if item[file_extension_dict['validator_key']] == file_extension_dict['validator_val']:
                        print("VALIDATION CORRECT")
                        #valiadation correct
                        self.remove_values(item, file_extension_dict)
                    else:
                        print("VALIDATION NOT CORRECT")
                        #will go to next item to then validate
                else:
                    #no validation needed, find if key to append to is present
                    self.remove_values(item, file_extension_dict)

            else:
                print("Validation key not present in dict.")




# for notetype in note_types:
#     if notetype['name'] == "Polygon": #the type of note to be added
#         jsonNoteAdder(notetype['file_sub_extension'], note_details, data)

# print(data)
