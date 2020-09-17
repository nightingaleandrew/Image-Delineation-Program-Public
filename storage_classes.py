#This file contains the storage classes for json files & db. jsonFileReaderWriter is the new class that creates a json file or can add records to the json file etc

#imports
import os, json

# #OLD Class for json filesaver
# class jsonFileWriter:
#     def __init__(self, filename, data, slice_name):
#         self.filename = filename
#         self.data = data
#         # print("data pn load", self.data)
#         self.slice = slice_name
#         self.note_keys = ["user", "note", "date", "time"]
#
#         #I have not done a try / except here but outside the class when the class is called instead as combines other methods
#         needcreate = not os.path.exists(self.filename)
#         if needcreate:
#             # print("File needed to be created.")
#             if self.data == None: #if passes through None then just add a []
#                 self.data = []
#             self.create_json_file(self.data) #create the file if one doesn't already exist
#
#             if self.slice != None:
#                 self.transform_dict() #change the dictionary so it can accept notes
#
#     # function to create the json file - only do this once
#     def create_json_file(self, data):
#         with open(self.filename,'w') as f:
#             # print(data)
#             json.dump(data, f, indent=4)
#
#     #read the file
#     def read_file(self):
#         try:
#             with open(self.filename) as f:
#                 currentdata = json.load(f)
#             return currentdata
#         except:
#             print("ERROR reading file.")
#             return []


#NEW FileWriterWrappers for Polygons, Notes & Tags. This is the new improved JsonFileWriter that overtakes the previous one
class jsonFileReaderWriter:
    def __init__(self, filename, datakey):
        self.filename = filename #filename of the file
        self.datakey = datakey #the first key within the json file
        self.data = {self.datakey: []} #structure of what would be initially put into the file if it needs to be created

    #Check & Create method to check if the file exists and if not, create it
    def check_and_create(self):
        needcreate = not os.path.exists(self.filename)
        if needcreate: #File needs to be created
            self.create_json_file(self.data) #create the file if one doesn't already exist

    #create file method
    def create_json_file(self, data):
        with open(self.filename,'w') as f:
            json.dump(data, f, indent=4) #use json.dump

    #add record method to the file
    def add_record(self, dict):
        try:
            self.check_and_create() #check if the json file exists - if not create it
            data = self.read_file() #read it
            data[self.datakey].append(dict) #append to appropiate datakey
            self.create_json_file(data) #create file
        except:
            print("Record could not be added.")

    #read the contents of the file
    def read_file(self):
        try:
            if os.path.exists(self.filename): #if the file exists, open it
                with open(self.filename) as f:
                    currentdata = json.load(f)
                    # print("FILE DATA", currentdata)
                    if self.datakey not in currentdata:
                        currentdata[self.datakey] = [] #all files have a datakey to append the data too.
                    return currentdata
            else:
                print("File does not exist")
                return None #return none if not exist
        except:
            return None #return none if could not be read
            print("ERROR, File could not be read.")

    #Method that returns the key data that is within the specified key
    def read_key_data(self):
        data = self.read_file()
        return data[self.datakey]

    def write_file(self, data):
        self.create_json_file({self.datakey: data})

    #sort the file by a particular value, may become defficent once I start using IDs
    def sort_file(self, data, sort_key, sort_val):
        try:
            sorted_data = []
            for item in data[self.datakey]:
            # for item in data:
                if item[sort_key] == sort_val:
                    sorted_data.append(item)
            return sorted_data
        except:
            return [] #return an empty list
            print("ERROR, File could not be sorted.")

    #Used for Updating the file such as changing a tag
    def update_file(self, data, id, key, new_value):
        try:
            if os.path.exists(self.filename):
                for item in data[self.datakey]:
                    if item['id'] == id: #if the id is the same then can re-state another piece of info
                        item[key] = new_value
                self.create_json_file(data)
        except:
            print("ERROR with updating record.")

    #Used for removing a piece of information such as a polygon
    def remove_record(self, data, id):
        try:
            if os.path.exists(self.filename):
                data[self.datakey] = [item for item in data[self.datakey] if item['id'] != id] #remove the polygon with the same id
                self.create_json_file(data) #write to the json file
        except:
            print("ERROR with removing record.")

#Class for the Database. The program does not create a database. However, I built this as I was researching db structure to gain knowledge. Therefore, it can be easily incorporated.
#Class is fully dynamic to add notes, polygon data etc
#Contains various methods that have not been commented fully within class. These include create table, add record, edit record, delete record. **THIS HAS NOT BEEN RECENTLY TESTED**
class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    def create_table(self, table_name, columns):
        conn = sqlite3.connect(self.db_name) #will create the db
        c = conn.cursor() #create the cursor

        query = """CREATE TABLE """ + table_name + """ ("""
        for column in columns:
            query += column['col_name'] + " " + column['col_type'] + ","
        query = query[:-1]
        query += """)"""
        c.execute(query)
        conn.commit() #commit changes
        conn.close() #close the connection to db

    def add_record(self, table_name, values, columns):
        if len(values) == len(columns):
            try:
                conn = sqlite3.connect(self.db_name) #will create the db
                c = conn.cursor() #create the cursor

                query = "INSERT INTO " + table_name + " ("

                for column in columns:
                    query += column['col_name'] + ", "
                query = query[:-2] + ")"
                query += " VALUES ("

                for value in values:
                    query += value + ", "
                query = query[:-2] + ")"
                print(query)
                c.execute(query)

                conn.commit() #commit changes
                conn.close() #close the connection to db

            except Exception as e:
                print(e)
        else:
            print("ERROR: Incorrect Number of Values Provided")

    def edit_record(self, table_name, values_to_be_updated, oid):
        if len(values) != len(columns):
            try:
                conn = sqlite3.connect(self.db_name) #will create the db
                c = conn.cursor() #create the cursor

                query = "UPDATE " + table_name + " SET "

                for new_val in values_to_be_updated:
                    query += new_val['column_name'] + " = " + new_val['new_val'] + ", "
                query = query[:-2] + "WHERE oid = " + oid

                c.execute(query)
                conn.commit() #commit changes
                conn.close() #close the connection to db

            except Exception as e:
                print(e)
        else:
            print("ERROR: Incorrect Number of Values Provided")

    def delete_record(self, table_name, oid):
        #delete record from the db using oid (presented on screen)
        try:
            conn = sqlite3.connect(self.db_name) #will create the db
            c = conn.cursor() #create the cursor
            query = "DELETE FROM " + table_name + " WHERE oid = " + oid
            c.execute(query)
            conn.commit() #commit changes
            conn.close() #close the connection to db
        except Exception as e:
            print(e)

    def delete_table(self, table_name):
        #delete table from the db
        try:
            conn = sqlite3.connect(self.db_name) #will create the db
            c = conn.cursor() #create the cursor
            query = "DROP TABLE " + table_name
            c.execute(query)
            conn.commit() #commit changes
            conn.close() #close the connection to db
        except Exception as e:
            print(e)

    def show_records(self, table_name):
        conn = sqlite3.connect(self.db_name) #will create the db
        c = conn.cursor() #create the cursor
        c.execute("SELECT *, oid FROM {}".format(table_name)) #oid is the primary key
        records = c.fetchall() #gets all the records

        conn.commit() #commit changes
        conn.close() #close the connection to db
        return records
