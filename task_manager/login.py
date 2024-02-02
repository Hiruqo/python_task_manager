import customtkinter


def login_correct(login_window):
    login_window.destroy()
    from app import show_app_window
    show_app_window()


def login(login_window):
    try:
        login_correct(login_window)
    except Exception as ex:
        print(f"An exception of type {type(ex).__name__} occurred: {ex}")
    else:
        print("No exception occurred.")


def show_login_window():
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
                                           command=lambda: login(login_window),
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
