# login.py
import customtkinter
import pyodbc
from app import show_app_window


def login_correct(login_window, user_id):
    login_window.destroy()
    show_app_window(user_id)


def login(login_window, conn, login, password):
    try:
        # Add code to check login credentials and get user ID from the database
        user_id = check_login_credentials(conn, login, password)
        if user_id is not None:
            login_correct(login_window, user_id)
        else:
            # Show a warning or handle incorrect login
            pass
    except Exception as ex:
        print(f"An exception of type {type(ex).__name__} occurred: {ex}")
    else:
        print("No exception occurred.")


def check_login_credentials(conn, login, password):
    cursor = conn.cursor()
    cursor.execute("SELECT UserID FROM LoginTab WHERE UserLogin = ? AND UserPassword = ?", (login, password))
    row = cursor.fetchone()
    return row[0] if row else None


def show_login_window(conn):
    login_window = customtkinter.CTk()
    login_window.geometry("450x260")
    login_window.title("Task Manager")

    # Disable resizing of the window
    login_window.resizable(width=False, height=False)

    frame = customtkinter.CTkFrame(master=login_window)
    frame.pack(pady=20,
               padx=60,
               fill="both",
               expand=True
               )

    label = customtkinter.CTkLabel(master=frame,
                                   text="Login",
                                   font=("Roboto", 24)
                                   )
    label.pack(pady=12,
               padx=10
               )

    entry_name = customtkinter.CTkEntry(master=frame,
                                        placeholder_text="Username",
                                        border_width=2,
                                        border_color="#ffc857"
                                        )
    entry_name.pack(pady=12,
                    padx=10
                    )

    entry_password = customtkinter.CTkEntry(master=frame,
                                            placeholder_text="Password",
                                            show="*",
                                            border_width=2,
                                            border_color="#ffc857"
                                            )
    entry_password.pack(pady=12,
                        padx=10
                        )

    login_button = customtkinter.CTkButton(master=frame,
                                           text="login",
                                           command=lambda: login(login_window,
                                                                 conn,
                                                                 entry_name.get(),
                                                                 entry_password.get()
                                                                 ),
                                           width=60,
                                           border_width=2,
                                           border_color="#ffc857",
                                           fg_color="#1a1a1a",
                                           hover_color="#6e542f",
                                           text_color="#ffc857"
                                           )
    login_button.pack(pady=12,
                      padx=10
                      )

    login_window.mainloop()
