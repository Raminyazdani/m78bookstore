import datetime
import re
from os import name as os_name, system as terminal


def clear():
    terminal('cls' if os_name.lower() == 'nt' else 'clear')


class ValidationError(Exception):
    # base exception for validation errors
    def __init__(self, message, value=None):
        self.message = message
        self.value = value

    def __str__(self):
        print("ValidationError: %s %s" % (self.message, self.value))
        return f"{self.value} ERROR:-> {self.message}"


class NameValidationError(ValidationError):
    def __init__(self, name, message):
        self.name = name
        self.message = message
        super(NameValidationError, self).__init__(message, name)


class PhoneValidationError(ValidationError):
    def __init__(self, phone, message):
        self.phone = phone
        self.message = message
        super(PhoneValidationError, self).__init__(message, phone)


class EmailValidationError(ValidationError):
    def __init__(self, email, message):
        self.email = email
        self.message = message
        super(EmailValidationError, self).__init__(message, email)


class NationalIdValidationError(ValidationError):
    def __init__(self, email, message):
        self.email = email
        self.message = message
        super(NationalIdValidationError, self).__init__(message, email)


class AgeValidationError(ValidationError):
    def __init__(self, email, message):
        self.email = email
        self.message = message
        super(AgeValidationError, self).__init__(message, email)


class PasswordValidationError(ValidationError):
    def __init__(self, email, message):
        self.email = email
        self.message = message
        super(PasswordValidationError, self).__init__(message, email)


class FileNameValidationError(ValidationError):
    def __init__(self, email, message):
        self.email = email
        self.message = message
        super(FileNameValidationError, self).__init__(message, email)


# for name ,firstname and surname ,username
def name_validator(name):
    pattern = r"^[a-zA-Z]{1}.*$"
    compiler = re.compile(pattern)
    if compiler.match(name):
        return True
    else:
        return False


def email_validator(email):
    pattern = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    compiler = re.compile(pattern)
    if compiler.match(email):
        return True
    else:
        return False


def national_id_validator(national_id):
    pattern = r"^\d{10}$"
    compiler = re.compile(pattern)
    if compiler.match(national_id):
        return True
    else:
        return False


def age_validator(age):
    pattern = r"^\d+$"
    compiler = re.compile(pattern)
    if compiler.match(age):
        return True
    else:
        return False


def password_validator(password):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    compiler = re.compile(pattern)
    if compiler.match(password):
        return True
    else:
        return False


def phone_validator(phone):
    pattern = r"(^09\d{9}$)|(^\+989\d{9}$)"
    compiler = re.compile(pattern)
    if compiler.match(phone):
        return True
    else:
        return False


class First_name:
    def __get__(self, obj, obj_type=None):
        return self.value

    def __set__(self, obj, value):
        if name_validator(value):
            self.value = value
        else:
            raise NameValidationError("Invalid first name format", value)


class Last_name:
    def __get__(self, obj, obj_type=None):
        return self.value

    def __set__(self, obj, value):
        if name_validator(value):
            self.value = value
        else:
            raise NameValidationError("Invalid Last name format", value)


class Phone:
    def __get__(self, obj, obj_type=None):
        return self.value

    def __set__(self, obj, value):
        if phone_validator(value):
            self.value = value
        else:
            raise PhoneValidationError("Invalid Phone format", value)


class National_id:
    def __get__(self, obj, obj_type=None):
        return self.value

    def __set__(self, obj, value):
        if national_id_validator(value):
            self.value = value
        else:
            raise NationalIdValidationError("Invalid national id format", value)


class Age:
    def __get__(self, obj, obj_type=None):
        return self.value

    def __set__(self, obj, value):
        if age_validator(value):
            self.value = value
        else:
            raise AgeValidationError("Invalid age format", value)


class Password:
    def __get__(self, obj, obj_type=None):
        return self.value

    def __set__(self, obj, value):
        if password_validator(value):
            self.value = value
        else:
            raise PasswordValidationError("Invalid password format", value)


class User_name:
    def __get__(self, obj, obj_type=None):
        return self.value

    def __set__(self, obj, value):
        if name_validator(value):
            self.value = value
        else:
            raise NameValidationError("Invalid Username format", value)


class Email:
    def __get__(self, obj, obj_type=None):
        return self.value

    def __set__(self, obj, value):
        if email_validator(value):
            self.value = value
        else:
            raise EmailValidationError("Invalid Email format", value)


class FileName:
    def __get__(self, obj, obj_type=None):
        return self.value

    def __set__(self, obj, value):
        if name_validator(value):
            self.value = value
        else:
            raise FileNameValidationError("Invalid File Name format", value)


class FilePath:
    def __get__(self, obj, obj_type=None):
        return self.value

    def __set__(self, obj, value):
        if name_validator(value):
            self.value = value
        else:
            raise FileNameValidationError("Invalid File Name format", value)


class Info:
    def __get__(self, obj, obj_type=None):
        return self.value

    def __set__(self, obj, value):
        if name_validator(value):
            self.value = value
        else:
            raise FileNameValidationError("Invalid File Name format", value)


def create_time():
    return str(datetime.datetime.now().timestamp())


table_column_types = {'first_name': "varchar(50)",
                      "last_name": "varchar(50)",
                      "username": "varchar(50)",
                      "email": "varchar(50)",
                      "phone": "varchar(50)",
                      "national_id": "varchar(50)",
                      "age": "varchar(50)",
                      "password": "varchar(50)",
                      "time_created": "varchar(50)",
                      "time_modified": "varchar(50)",
                      "name": "varchar(50)",
                      "owner": "varchar(50)",
                      "path": "varchar(50)",
                      "time_added": "varchar(50)",
                      "info": "varchar(50)"}


unique_table_column_types = ["email", "username"]
