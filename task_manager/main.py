# main.py
import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

if __name__ == "__main__":
    from login import show_login_window
    show_login_window()
