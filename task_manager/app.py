import customtkinter
from PIL import Image, ImageTk


def logout(app_window):
    app_window.destroy()
    from login import show_login_window
    show_login_window()


def show_app_window():
    app_window = customtkinter.CTk()
    app_window.geometry("800x600")
    app_window.title("App Window")
    app_window.resizable(height=False, width=False)

    # create a frame for app window
    app_frame = customtkinter.CTkFrame(master=app_window)
    app_frame.pack(pady=20, padx=30, fill="both", expand=True)

    # left side of the app (10% of total width)
    app_left_frame = customtkinter.CTkFrame(master=app_frame)
    app_left_frame.pack(side="left", fill="both", expand=False, padx=(0, 10))

    # icon
    app_home_icon = customtkinter.CTkFrame(master=app_left_frame,
                                           border_width=2, border_color="#ffc857")
    app_home_icon.pack(pady=(10, 5), padx=10)

    # icon image + add images
    image_path1 = 'img/home1.png'   # unused homepage
    image_path2 = 'img/home2.png'   # unused homepage
    image_path3 = 'img/logout.png'
    image = Image.open(image_path3)

    # resize the images
    new_size = (40, 40)
    resized_image = image.resize(new_size)
    icon_image = ImageTk.PhotoImage(resized_image)
    icon_label = customtkinter.CTkLabel(master=app_home_icon, image=icon_image, text="", bg_color="#6e542f")
    icon_label.image = icon_image
    icon_label.pack(pady=(10, 5), padx=50)

    # button
    logout_button = customtkinter.CTkButton(
        master=app_home_icon, text="logout", command=lambda: logout(app_window),
        width=60, border_width=2, border_color="#ffc857",
        fg_color="#1a1a1a", hover_color="#6e542f", text_color="#ffc857"
    )
    logout_button.pack(pady=(5, 10), padx=10)

    # sidebar
    app_sidebar = customtkinter.CTkFrame(master=app_left_frame,
                                         border_width=2, border_color="#ffc857")
    app_sidebar.pack(pady=(5, 10), padx=10, fill="both", expand=True)

    # right side of the app
    app_right_frame = customtkinter.CTkFrame(master=app_frame,
                                             border_width=2, border_color="#ffc857")
    app_right_frame.pack(side="right", fill="both", expand=True)

    app_window.mainloop()
