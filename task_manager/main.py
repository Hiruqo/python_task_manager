# main.py
import customtkinter
import pyodbc
from login import show_login_window

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


def initialize_database():
    conn_str = 'DRIVER={SQL Server};SERVER=DESKTOP-HGV327J\\SQLEXPRESS;DATABASE=TaskDB;Trusted_Connection=yes;'
    connection = pyodbc.connect(conn_str)
    cursor = connection.cursor()
    return connection


if __name__ == "__main__":
    conn = initialize_database()
    show_login_window(conn)  # Pass the database connection to the login window
