import mysql.connector
from mysql.connector import (connection)
from mysql.connector import errorcode


class CrudOperation:
    """In this class we are going to connect with DB for doing CRUD Operation"""
    def __init__(self, database_name):
        """This is constructor of CrudOperation"""
        self.database_name = database_name
        self.connection = None
        try:
            self.connection = mysql.connector.connect(user="root", password="12345", host="127.0.0.1", port=3306,
                                                      database=self.database_name)
            # connection = connection.MySQLConnection(user="Dhoni", password="dhoni07", host="127.0.0.1", port=3306,
            # database="python")
            print("connection Established")
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Error occurred in your username and password")
            elif e.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database Doesn't Exist")
            else:
                print(e)

    def create_table(self):
        """This function is used to create a table in mysql Database"""
        try:
            while True:
                table_name = input("please enter the Table Name")
                display_query = "show tables"
                self.cursor.execute(display_query)
                tables = self.cursor.fetchall()
                for i in tables:
                    str_i = ''.join(i)
                    print(str_i)
                    if str_i == table_name:
                        print("Sorry Table already present in the Database")
                        choice = input("Do you want to create table with new name? press Y/N")
                        break
                    else:
                        continue
                else:
                    no_of_columns = int(input("please enter no of columns you want to create in table"))
                    create_query = f"create table {table_name}("
                    for i in range(no_of_columns):
                        add = input(f"please enter the details of record {i+1}:\nplease Enter column name and its constraints by leaving space inbetween")
                        create_query = create_query+add+','
                    new_create_query = create_query[0:-1]
                    query = new_create_query+')'
                    print(query)
                    self.cursor.execute(query)
                    print("Table created")
                    column_lst = self.desc_table(table_name)
                    print(column_lst)
                    choice = " "
                if choice.upper() == 'Y':
                    continue
                elif choice.upper() == 'N':
                    print("Table creation terminated by user")
                    break
                else:
                    break
            # create_query = f"""create table if not exists {table_name}(id integer not null unique,first_name varchar(20) not null,last_name varchar(20))"""
            # self.cursor.execute(create_query)
            # print("Query Executed successfully")
        except Exception as e:
            print(e)

    def insert_data(self, table_name):
        """This function is used to  insert data into particular table"""
        try:
            column_lst = self.desc_table(table_name)
            print(column_lst)
            self.printall_data(table_name)
            length_column = len(column_lst)
            query = f"insert into {table_name} values(%s)"
            new_query = query % (",".join("%s" for i in range(length_column)))
            print(new_query)
            lst_tuples = []
            tup = ()
            for i in range(length_column):
                value_i = input("Enter the value for {} column".format(column_lst[i]))
                tup = tup + (value_i,)
            lst_tuples.append(tup)

            self.cursor.executemany(new_query, lst_tuples)
            # id = int(input("Please Enter the student id"))
            # first_name = input("Please Enter the first_name of student")
            # last_name = input("Please Enter the last_name of student")
            # insert_query = f"""insert into {table_name}(id,first_name,last_name)values(%s,%s,%s)"""
            # values_query = (id, first_name, last_name)
            # self.cursor.execute(insert_query, values_query)
            print("Data inserted")
            self.printall_data(table_name)
        except Exception as e:
            print(e)

    def printall_data(self, table_name):
        """This function is used print all data from the specific table"""
        try:
            query = f"""select * from {table_name}"""
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            for x in data:
                print(x)
        except Exception as e:
            print(e)

    def delete_data(self, table_name):
        """This function is  used to delete the record from particular table"""
        try:
            column_lst = self.desc_table(table_name)
            print("Before Delete")
            print(column_lst)
            self.printall_data(table_name)
            value_id = int(input("please enter the id to  delete the record"))
            delete_query = f"""Delete from {table_name} where {column_lst[0]}=%s"""
            value_query = [value_id]
            self.cursor.execute(delete_query, value_query)
            print("Data Deleted\nAfter Delete")
            self.printall_data(table_name)
        except Exception as e:
            print(e)

    def update_data(self, table_name):
        """This function is used to  update the record in particular table"""
        try:
            column_lst = self.desc_table(table_name)
            print("Before update")
            print(column_lst)
            self.printall_data(table_name)
            column_name = input("Please enter the column name to modify the value")
            if column_name == column_lst[0]:
                print("sorry you cannot change primary column value")
            else:
                value = input(f"please enter the value for the column {column_name}")
                id = input("please enter the id ")
                update_query = f"""update {table_name} set {column_name} = %s where {column_lst[0]}=%s"""
                query_value = (value, id)
                self.cursor.execute(update_query, query_value)
                print("Data updated\nAfter Update")
                self.printall_data(table_name)

        except Exception as e:
            print(e)

    def desc_table(self, table_name):
        """This function is used to provide the description about the table"""
        try:
            lst = []
            query = f"desc {table_name}"
            self.cursor.execute(query)
            table_structure = self.cursor.fetchall()
            for struc in table_structure:
                lst.append(struc[0])
            return lst
        except Exception as e:
            print("Exception occurred {}".format(e))

    def commit_close(self):
        """In this function we are closing the connection and committing it"""
        if self.connection is not None:
            print("closing connection")
            self.connection.commit()
            self.connection.close()


def main():
    """This main method is used to ask user which operation would you like perform on which database and table"""
    try:
        dbname = input("PLEASE ENTER THE DATABASE NAME")
        cd = CrudOperation(dbname)
        if cd.connection is not None:
            while True:
                choice = int(input("PLEASE CHOOSE THE OPERATION WOULD YOU LIKE TO PERFORM"
                               "\nPRESS 1.CREATE TABLE\nPRESS 2.INSERT DATA\nPRESS 3.UPDATE DATA\nPRESS 4.DELETE DATA\n"))
                if choice == 1:
                    print("creating table")
                    cd.create_table()

                elif choice == 2:
                    table_name = input("Please Enter the Table name")
                    print("inserting data")
                    cd.insert_data(table_name)

                elif choice == 3:
                    table_name = input("Please Enter the Table name")
                    print("updating data")
                    cd.update_data(table_name)

                elif choice == 4:
                    table_name = input("Please Enter the Table name")
                    print("Deleting Data")
                    cd.delete_data(table_name)

                else:
                    print("Invalid Data, Please Try Again..!!")

                criteria = input("Do you like to continue If yes Then press Y If not then Press N (Y/N)?")
                if criteria.upper() == 'Y':
                    continue
                elif criteria.upper() == 'N':
                    break
                else:
                    print("Invalid Answer So Program Terminated")
                    break

    except Exception as e:
        print(e)

    finally:
        cd.commit_close()


if __name__ == "__main__":
    main()
