import sqlite3

CREATE_CONTACT_BOOK = """
    CREATE TABLE contactbook (
        id INTEGER PRIMARY KEY,
        name TEXT,
        surname TEXT,
        phone TEXT,
        email TEXT
    )
    """

INSERT_CONTACT = """
    INSERT INTO contactbook (
        name,
        surname,
        phone,
        email
    ) values (?, ?, ?, ?)
    """

LIST_CONTACTS = """SELECT * FROM contactbook ORDER BY id"""
LIST_CONTACT_BY_VALUE = """SELECT * FROM contactbook WHERE ? = ?"""
DELETE_CONTACT = """DELETE FROM contactbook WHERE id = ?"""
DELETE_ALL_CONTACTS = """DELETE FROM contactbook"""
DROP_TABLE = """DROP TABLE IF EXISTS contactbook"""

# SET new_value and provide ID of record
EDIT_CONTACT_NAME = """UPDATE contactbook SET NAME = ? WHERE id = ?"""
EDIT_CONTACT_SURNAME = """UPDATE contactbook SET SURNAME = ? where id = ?"""
EDIT_CONTACT_EMAIL = """UPDATE contactbook SET EMAIL = ? where id = ?"""
EDIT_CONTACT_PHONE = """UPDATE contactbook SET PHONE = ? where id = ?"""

EDIT_COMMANDS = [
    EDIT_CONTACT_NAME,
    EDIT_CONTACT_EMAIL,
    EDIT_CONTACT_PHONE,
    EDIT_CONTACT_SURNAME
]


class DBConnect(object):
    """
    Works as context manager
    """

    def __init__(self, create_tables=False):
        self.db = None
        self.create_tables = create_tables
        self.connect()

    def __enter__(self):
        """
        Enter context manager results in creating DB connection
        """
        # Create table only at the very beginning
        if self.create_tables:
            self.create_table()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit context manager to ensure closing connection
        """
        self.db.close()

    def create_table(self):
        self.db.execute(CREATE_CONTACT_BOOK)
        self.commit()

    def connect(self):
        self.db = sqlite3.connect('contacts.db')
        return self.db

    def commit(self):
        self.db.commit()

    def insert_contact(self, contact):
        self.db.execute(
            INSERT_CONTACT,
            (
                contact['name'],
                contact['surname'],
                contact['phone'],
                contact['email']
            )
        )
        self.commit()

    def list_contacts(self):
        cursor = self.db.execute(LIST_CONTACTS)
        return cursor.fetchall()

    def list_contact(self, key, value):
        cursor = self.db.execute(
            LIST_CONTACT_BY_VALUE,
            (
                key,
                value,
            )
        )
        return cursor.fetchall()

    def edit_contact(self, key, new_value, index):
        for command in EDIT_COMMANDS:
            if key.upper() in command:
                sql_command = command
                break

        self.db.execute(
            sql_command,
            (
                new_value,
                str(index)
            )
        )
        self.db.commit()

    def delete_contact(self, index):
        self.db.execute(
            DELETE_CONTACT,
            (
                str(index),
            )
        )
        self.commit()

    def delete_all_contacts(self):
        self.db.execute(DELETE_ALL_CONTACTS)
        self.commit()

    def drop_table(self):
        self.db.execute(DROP_TABLE)
        self.commit()
