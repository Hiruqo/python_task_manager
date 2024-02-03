# app.py
import customtkinter
from tkinter import ttk
from classes import Task
import pyodbc
from PIL import Image, ImageTk
import speech_recognition as sr

tasks = []
app_right_frame = None
conn = None


def initialize_database():
    conn_str = 'DRIVER={SQL Server};SERVER=DESKTOP-HGV327J\\SQLEXPRESS;DATABASE=TaskDB;Trusted_Connection=yes;'
    connection = pyodbc.connect(conn_str)
    return connection


def logout(app_window):
    app_window.destroy()
    from login import show_login_window
    show_login_window()


def show_warning(message):
    war_wind = customtkinter.CTk()
    war_wind.geometry("270x100")
    war_wind.title("Warning")
    war_wind.resizable(height=False, width=False)

    warning_label = customtkinter.CTkLabel(master=war_wind, text=message)
    warning_label.pack(pady=10, padx=10)

    warning_btn = customtkinter.CTkButton(master=war_wind,
                                          text="OK",
                                          command=war_wind.destroy,
                                          width=60,
                                          border_width=2,
                                          border_color="#ffc857",
                                          fg_color="#1a1a1a",
                                          hover_color="#6e542f",
                                          text_color="#ffc857"
                                          )
    warning_btn.pack(pady=(5, 10),
                     padx=10
                     )

    war_wind.mainloop()


def add_task(task_combobox, right_task_name, right_task_description, user_id):
    global tasks, conn  # Ensure that you use the global variables

    task_name = right_task_name.get()
    task_description = right_task_description.get()

    if len(task_name) > 21 and len(task_description) > 250:
        show_warning("The title and description are too long!")
    elif len(task_name) > 21:
        show_warning("The title has to be \nshorter than 21 letters!")
    elif len(task_description) > 250:
        show_warning("The description has to be \nshorter than 250 letters!")
    else:
        if task_name:
            new_task = Task(title=task_name, description=task_description)
            tasks.append(new_task)

            # Insert the new task into the database
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Tasks (UserID, Title, Description) VALUES (?, ?, ?)",
                           (user_id, task_name, task_description))
            conn.commit()

            task_combobox["values"] = tuple(task.title for task in tasks)
            right_task_name.delete(0, "end")  # Clear the entry after adding the task
            right_task_description.delete(0, "end")  # Clear the entry after adding the task


def delete_task(task, task_combobox, app_frame):
    global tasks, app_right_frame  # Ensure that you use the global variables

    # Delete the task from the database
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Tasks WHERE TaskID = ?", (task.task_id,))
    conn.commit()

    tasks.remove(task)
    task_combobox["values"] = tuple(task.title for task in tasks)
    reset_right_frame(task_combobox, app_frame)


def edit_task(task, task_combobox, app_frame, user_id):
    global app_right_frame, conn

    edit_window = customtkinter.CTk()
    edit_window.geometry("450x300")
    edit_window.title("Edit Description")
    edit_window.resizable(height=False, width=False)

    edit_label = customtkinter.CTkLabel(master=edit_window, text="Enter new description", font=("Roboto", 24))
    edit_label.pack(pady=(10, 5), padx=10)

    new_description_entry = customtkinter.CTkEntry(master=edit_window,
                                                    placeholder_text="New description..",
                                                    height=200,
                                                    width=400,
                                                    border_width=2,
                                                    border_color="#ffc875"
                                                    )
    new_description_entry.pack(pady=(5, 5), padx=10)

    def apply_changes():
        new_description = new_description_entry.get()
        if new_description:
            # Update the description in the tasks list
            task.description = new_description

            # Update the description in the database
            cursor = conn.cursor()
            cursor.execute("UPDATE Tasks SET Description = ? WHERE TaskID = ? AND UserID = ?",
                           (new_description, task.task_id, user_id))
            conn.commit()

            # Destroy the current right frame
            app_right_frame.destroy()

            # Rebuild the right frame with the updated description
            reset_right_frame(task_combobox, app_frame)

            edit_window.destroy()

    def cancel_changes():
        edit_window.destroy()

    ok_btn = customtkinter.CTkButton(master=edit_window,
                                     text="OK",
                                     command=apply_changes,
                                     border_width=2,
                                     border_color="#ffc857",
                                     fg_color="#1a1a1a",
                                     hover_color="#6e542f",
                                     text_color="#ffc857"
                                     )
    ok_btn.pack(side="left", pady=(5, 10), padx=(75, 5))

    cancel_btn = customtkinter.CTkButton(master=edit_window,
                                         text="Cancel",
                                         command=cancel_changes,
                                         border_width=2,
                                         border_color="#ffc857",
                                         fg_color="#1a1a1a",
                                         hover_color="#6e542f",
                                         text_color="#ffc857"
                                         )
    cancel_btn.pack(side="left", pady=(5, 10), padx=(5, 10))

    edit_window.mainloop()


def update_description(right_task_description, new_description_entry, voice_window):
    description_text = new_description_entry.get()
    right_task_description.delete(0, "end")
    right_task_description.insert(0, description_text)
    voice_window.destroy()


def voice_recognition(app_frame, task_combobox, right_task_description):
    global app_right_frame  # Ensure that you use the global variable

    voice_window = customtkinter.CTk()
    voice_window.geometry("450x300")
    voice_window.title("Voice Recognition")
    voice_window.resizable(height=False, width=False)

    edit_label = customtkinter.CTkLabel(master=voice_window,
                                        text="Enter voice description",
                                        font=("Roboto", 24)
                                        )
    edit_label.pack(pady=(10, 5),
                    padx=10
                    )

    new_description_entry = customtkinter.CTkEntry(master=voice_window,
                                                   placeholder_text="",
                                                   height=200,
                                                   width=400,
                                                   border_width=2,
                                                   border_color="#ffc875"
                                                   )
    new_description_entry.pack(pady=(5, 5),
                               padx=10
                               )

    def try_to_say():
        smaller_window = customtkinter.CTk()
        smaller_window.geometry("200x100")
        smaller_window.title("Say something..")
        smaller_window.resizable(height=False, width=False)

        def voice_recognize_google():
            recognizer = sr.Recognizer()  # 'recognizer' object start

            with sr.Microphone() as source:  # set microphone peripherial as audio source
                recognizer.adjust_for_ambient_noise(source, duration=1)  # set the environmental (sound) settings
                audio = recognizer.listen(source)  # start listening to user's microphone

            try:
                text = recognizer.recognize_google(audio)  # google cloud tries to detect words
                return text
            except sr.UnknownValueError:  # unknown text
                print("Could not understand audio.")
                return None
            except sr.RequestError as e:  # Error code print
                print(f"Google Speech Recognition request failed: {e}")
                return None

        voice_text = voice_recognize_google()
        if voice_text:
            if "exit" in voice_text.lower():
                smaller_window.destroy()
            else:
                new_description_entry.insert("end", voice_text + " ")

    def cancel_changes():
        voice_window.destroy()

    listen_btn = customtkinter.CTkButton(master=voice_window,
                                         text="Listen",
                                         border_width=2,
                                         border_color="#ffc857",
                                         fg_color="#1a1a1a",
                                         hover_color="#6e542f",
                                         text_color="#ffc857"
                                         )
    listen_btn.pack(side="left",
                    pady=(5, 10),
                    padx=(20, 5)
                    )

    ok_btn = customtkinter.CTkButton(master=voice_window,
                                     text="OK",
                                     command=lambda: update_description(right_task_description,
                                                                        new_description_entry,
                                                                        voice_window
                                                                        ),
                                     border_width=2,
                                     border_color="#ffc857",
                                     fg_color="#1a1a1a",
                                     hover_color="#6e542f",
                                     text_color="#ffc857"
                                     )
    ok_btn.pack(side="left",
                pady=(5, 10),
                padx=(5, 5)
                )

    cancel_btn = customtkinter.CTkButton(master=voice_window,
                                         text="Cancel",
                                         command=cancel_changes,
                                         border_width=2,
                                         border_color="#ffc857",
                                         fg_color="#1a1a1a",
                                         hover_color="#6e542f",
                                         text_color="#ffc857"
                                         )
    cancel_btn.pack(side="left",
                    pady=(5, 10),
                    padx=(5, 10)
                    )

    voice_window.mainloop()


def show_selected_task(event, task_combobox, app_frame):
    global app_right_frame  # Ensure that you use the global variable
    selected_task_name = task_combobox.get()
    for task in tasks:
        if task.title == selected_task_name:
            display_task_details(task, task_combobox, app_frame)
            break


def display_task_details(task, task_combobox, app_frame):
    global app_right_frame  # Ensure that you use the global variable

    if app_right_frame is None:
        return  # Skip further execution if app_right_frame is not assigned

    # Clear the right frame
    for widget in app_right_frame.winfo_children():
        widget.destroy()

    # Display details of the selected task
    title_label = customtkinter.CTkLabel(master=app_right_frame,
                                         text=f"Title: {task.title}",
                                         font=("Roboto", 36)
                                         )
    title_label.pack(pady=(30, 5),
                     padx=10
                     )

    description_label = customtkinter.CTkLabel(master=app_right_frame,
                                               text=task.description,
                                               height=400,
                                               width=500
                                               )
    description_label.pack(pady=5)

    home_btn = customtkinter.CTkButton(master=app_right_frame,
                                       text="Home",
                                       command=lambda: reset_right_frame(task_combobox, app_frame),
                                       width=60,
                                       border_width=2,
                                       border_color="#ffc857",
                                       fg_color="#1a1a1a",
                                       hover_color="#6e542f",
                                       text_color="#ffc857"
                                       )
    home_btn.pack(side="left",
                  pady=(5, 10),
                  padx=(175, 5)
                  )

    edit_btn = customtkinter.CTkButton(master=app_right_frame,
                                       text="Edit",
                                       command=lambda: edit_task(task, task_combobox, app_frame),
                                       width=60,
                                       border_width=2,
                                       border_color="#ffc857",
                                       fg_color="#1a1a1a",
                                       hover_color="#6e542f",
                                       text_color="#ffc857"
                                       )
    edit_btn.pack(side="left",
                  pady=(5, 10),
                  padx=(5, 5)
                  )

    del_btn = customtkinter.CTkButton(master=app_right_frame,
                                      text="Delete",
                                      command=lambda: delete_task(task, task_combobox, app_frame),
                                      width=60,
                                      border_width=2,
                                      border_color="#ffc857",
                                      fg_color="#1a1a1a",
                                      hover_color="#6e542f",
                                      text_color="#ffc857"
                                      )
    del_btn.pack(side="left",
                 pady=(5, 10),
                 padx=(5, 5)
                 )


def reset_right_frame(task_combobox, app_frame):
    global app_right_frame  # Ensure that you use the global variable

    # Create a new right frame
    new_right_frame = customtkinter.CTkFrame(master=app_frame,
                                             border_width=2,
                                             border_color="#ffc857"
                                             )
    new_right_frame.pack(side="right",
                         fill="both",
                         expand=True
                         )

    # add button to add a task to the list
    right_task_name = customtkinter.CTkEntry(master=new_right_frame,
                                             placeholder_text="Task title",
                                             border_width=2,
                                             border_color="#ffc857",
                                             width=200
                                             )
    right_task_name.pack(pady=(20, 5),
                         padx=10
                         )

    right_task_description = customtkinter.CTkEntry(master=new_right_frame,
                                                    placeholder_text="Description..",
                                                    border_width=2,
                                                    border_color="#ffc857",
                                                    height=450,
                                                    width=500
                                                    )
    right_task_description.pack(pady=(5, 5),
                                padx=10
                                )

    right_task_btn = customtkinter.CTkButton(master=new_right_frame,
                                             text="Add Task",
                                             command=lambda: add_task(task_combobox,
                                                                      right_task_name,
                                                                      right_task_description
                                                                      ),
                                             width=100,
                                             border_width=2,
                                             corner_radius=100,
                                             border_color="#ffc857",
                                             fg_color="#1a1a1a",
                                             hover_color="#6e542f",
                                             text_color="#ffc857"
                                             )
    right_task_btn.pack(pady=(5, 0),
                        padx=10
                        )

    # Destroy the old right frame
    if app_right_frame is not None:
        app_right_frame.destroy()

    # Update the reference to the new right frame
    app_right_frame = new_right_frame


def show_app_window(user_id):
    global conn, app_right_frame, tasks  # Ensure that you use the global variable
    conn = initialize_database()
    app_window = customtkinter.CTk()
    app_window.geometry("800x600")
    app_window.title("App Window")
    app_window.resizable(height=False,
                         width=False
                         )

    # create a frame for the app window
    app_frame = customtkinter.CTkFrame(master=app_window)
    app_frame.pack(pady=20,
                   padx=30,
                   fill="both",
                   expand=True
                   )

    # left side of the app (10% of the total width)
    app_left_frame = customtkinter.CTkFrame(master=app_frame)
    app_left_frame.pack(side="left",
                        fill="both",
                        expand=False,
                        padx=(0, 10)
                        )

    # icon
    app_home_icon = customtkinter.CTkFrame(master=app_left_frame,
                                           border_width=2,
                                           border_color="#ffc857"
                                           )
    app_home_icon.pack(pady=(10, 5),
                       padx=10)

    # icon image + add images
    image_path1 = 'img/home1.png'  # unused homepage
    image_path2 = 'img/home2.png'  # unused homepage
    image_path3 = 'img/logout.png'
    image = Image.open(image_path3)

    # resize the images
    new_size = (40, 40)
    resized_image = image.resize(new_size)
    icon_image = ImageTk.PhotoImage(resized_image)
    icon_label = customtkinter.CTkLabel(master=app_home_icon,
                                        image=icon_image,
                                        text="",
                                        bg_color="#6e542f"
                                        )
    icon_label.image = icon_image
    icon_label.pack(pady=(10, 5),
                    padx=50
                    )

    # button
    logout_button = customtkinter.CTkButton(master=app_home_icon,
                                            text="logout",
                                            command=lambda: logout(app_window),
                                            width=60,
                                            border_width=2,
                                            border_color="#ffc857",
                                            fg_color="#1a1a1a",
                                            hover_color="#6e542f",
                                            text_color="#ffc857"
                                            )
    logout_button.pack(pady=(5, 10),
                       padx=10
                       )

    # sidebar
    app_sidebar = customtkinter.CTkFrame(master=app_left_frame,
                                         border_width=2,
                                         border_color="#ffc857"
                                         )
    app_sidebar.pack(pady=(5, 10),
                     padx=10,
                     fill="both",
                     expand=True
                     )

    task_combobox = ttk.Combobox(master=app_sidebar,
                                 width=20
                                 )
    task_combobox.pack(pady=10,
                       padx=10
                       )
    task_combobox.bind("<<ComboboxSelected>>",
                       lambda event: show_selected_task(event,
                                                        task_combobox,
                                                        app_frame
                                                        )
                       )

    # right side of the app
    global app_right_frame  # Ensure that you use the global variable
    app_right_frame = customtkinter.CTkFrame(master=app_frame,
                                             border_width=2, border_color="#ffc857")
    app_right_frame.pack(side="right",
                         fill="both",
                         expand=True
                         )

    # add button to add a task to the list
    right_task_name = customtkinter.CTkEntry(master=app_right_frame,
                                             placeholder_text="Task title",
                                             border_width=2,
                                             border_color="#ffc857",
                                             width=200
                                             )
    right_task_name.pack(pady=(20, 5),
                         padx=10
                         )

    right_task_description = customtkinter.CTkEntry(master=app_right_frame,
                                                    placeholder_text="Description..",
                                                    border_width=2,
                                                    border_color="#ffc857",
                                                    height=450,
                                                    width=500
                                                    )
    right_task_description.pack(pady=(5, 5),
                                padx=10
                                )

    right_task_btn = customtkinter.CTkButton(master=app_right_frame,
                                             text="Add Task",
                                             command=lambda: add_task(task_combobox,
                                                                      right_task_name,
                                                                      right_task_description,
                                                                      user_id
                                                                      ),
                                             width=100,
                                             border_width=2,
                                             corner_radius=100,
                                             border_color="#ffc857",
                                             fg_color="#1a1a1a",
                                             hover_color="#6e542f",
                                             text_color="#ffc857"
                                             )
    right_task_btn.pack(pady=(5, 10),
                        padx=(170, 5),
                        side="left"
                        )

    voice_btn = customtkinter.CTkButton(master=app_right_frame,
                                        text="Voice+",
                                        # command=lambda: voice_recognition(app_frame,
                                        #                                   task_combobox,
                                        #                                   right_task_description
                                        #                                   ),
                                        width=100,
                                        border_width=2,
                                        corner_radius=100,
                                        border_color="#ffc857",
                                        fg_color="#1a1a1a",
                                        hover_color="#6e542f",
                                        text_color="#ffc857"
                                        )
    voice_btn.pack(pady=(5, 10),
                   padx=(5, 5),
                   side="left"
                   )

    # Fetch tasks for the specific user from the database
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Tasks WHERE UserID = ?", (user_id,))
    fetched_tasks = cursor.fetchall()
    
    # Assuming you fetch TaskID along with other columns from the database
    tasks = [Task(task_id=row.TaskID, title=row.Title, description=row.Description) for row in fetched_tasks]

    # Populate task_combobox with task titles
    task_combobox["values"] = tuple(task.title for task in tasks)

    app_window.mainloop()
    