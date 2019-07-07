#!/usr/bin/env python3

from cacher import Cacher
from database import DBConnect

class ContactBook(object):

    def __init__(self, db):
        self.db = db
        self.contacts = self.db.list_contacts()

    def add_contact(self, contact):
        """
        Add new contact to the database
        :param contact: <dict> A new contact
        """
        self.db.insert_contact(contact)
        return self.update_contacts()

    def list_contacts(self):
        """
        Print contacts without contacting to database
        """
        return self.contacts

    @Cacher(cache_dir='./data/')
    def update_contacts(self):
        """
        Update contacts after change
        """
        self.contacts = self.db.list_contacts()
        return self.list_contacts()

    def delete_contact(self, index):
        self.db.delete_contact(index)
        return self.update_contacts()

    def delete_contacts(self):
        """
        Delete all contact from database
        """
        self.db.delete_all_contacts()
        return self.update_contacts()

    def edit_contact(self, key, value, index):
        """
        Edit existing contact
        :param key: <str> Key from database - name, surname, phone, email
        :param value: <str> New value for a given key
        :param index: <int> Index of a contact to be edited
        """
        self.db.edit_contact(
            key,
            value,
            index
        )
        return self.update_contacts()

    def list_contact(self, key, value):
        """
        List contact by searching for a given value
        :param key: <str> Key from database - name, surname, phone, email
        :param value: <str> A value to be searched for
        """
        self.db.list_contact(
            key,
            value,
        )

    def sort_list(self, key_):
        """
        Sort list by a given key
        :param key_: <str> Key used to sert the list
        """
        options = {
            'index': 0,
            'name' : 1,
            'surname': 2,
            'email': 3,
            'phone': 4,
        }
        if key_ in options.keys():
            key_ = options.get(key_)

        return(sorted(self.contacts, key = lambda x: x[key_]))

    def present_data(self, data=None):
        """
        Method to present data in a pretty way
        :param data: <list> Optional list of contacts
        """
        print('--------------------------------------------------------------------------')
        print('{:<10}{:<10}{:<15}{:<17}{:<17}'.
              format(
                  'index',
                  'name',
                  'surname',
                  'email',
                  'phone'
              )
             )
        print('--------------------------------------------------------------------------')

        data = data if data else self.contacts
        for contact in data:
            print('{:<10}{:<10}{:<15}{:<17}{:<17}'.
                  format(
                      contact[0],
                      contact[1],
                      contact[2],
                      contact[3],
                      contact[4]
                  )
                 )


if __name__ == "__main__":
    with DBConnect() as db:
        contacts = ContactBook(db)
        contact = {
            'name': 'Anne-Mary',
            'surname': 'Pitt',
            'email': 'ann-mary234@email.com',
            'phone': '+49883495333'
        }
        # contacts.add_contact(contact)
        # print(contacts.delete_contacts())
        # updated = contacts.edit_contact('surname','Doe', 10)
        # for contact in updated:
        #    print(contact)
        # print(contacts.list_contact('name', 'Caroline'))
        # contacts.update_contacts()
        contacts.delete_contact(37)
        sorted_ = contacts.sort_list('name')
        contacts.present_data(sorted_)
        contacts.update_contacts()
