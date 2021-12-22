from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


# Password Generator Project
def generate_password():
    global password_entry
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]

    password_list = password_letters + password_numbers + password_symbols

    random.shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)

    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website_entry_text = website_entry.get()
    email_username_entry_text = email_username_entry.get()
    password_entry_text = password_entry.get()
    new_data = {
        website_entry_text: {
            "email": email_username_entry_text,
            "password": password_entry_text,
        },
    }

    if len(website_entry_text) == 0:
        messagebox.showinfo(title="Oops", message="Don't leave any fields empty.")
    elif len(email_username_entry_text) == 0:
        messagebox.showinfo(title="Oops", message="Don't leave any fields empty.")
    elif len(password_entry_text) == 0:
        messagebox.showinfo(title="Oops", message="Don't leave any fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading the old data.
                data = json.load(data_file)
                # Updating the old data with the new one.
                data.update(new_data)

            with open("data.json", "w") as data_file:
                # Saving the updated data in the file.
                json.dump(data, data_file, indent=4)
        except json.decoder.JSONDecodeError:
            with open("data.json", "w") as data_file:
                data_file.write(json.dumps(new_data, indent=4))
        finally:
            website_entry.delete(0, END)
            email_username_entry.delete(0, END)
            password_entry.delete(0, END)

        website_entry.focus()
        email_username_entry.insert(0, "akileshakileshs1234@gmail.com")


# ---------------------------- Search Password ------------------------------- #
website_name = None
website_password = None


def find_password():
    try:
        global website_name
        global website_password
        website_entry_text = website_entry.get()
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            for thing in data:
                if thing == website_entry_text:
                    website_name = thing
                    website_password = data[thing]["password"]
                    messagebox.showinfo(title=website_name, message=f"Website: {website_name}\n"
                                                                    f"Password: {website_password}")
                    website_entry.delete(0, END)
    except json.decoder.JSONDecodeError:
        messagebox.showinfo(title="Error", message="No details for the website exists.")


# ---------------------------- UI SETUP ------------------------------- #

# Window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Putting image on to the screen with canvas widget.
canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:", font=("Arial", 12, "normal"))
website_label.grid(row=1, column=0)

email_username_label = Label(text="Email/Username:", font=("Arial", 12, "normal"))
email_username_label.grid(row=2, column=0)

password_label = Label(text="Password:", font=("Arial", 12, "normal"))
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=19)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_username_entry = Entry(width=35)
email_username_entry.grid(row=2, column=1, columnspan=2)
# With the below method I am pre inserting the email that I am mostly going to use. This could save me a lot of time.
email_username_entry.insert(0, "akileshakileshs1234@gmail.com")

password_entry = Entry(width=19)
password_entry.grid(row=3, column=1)

# Buttons
generate_password_button = Button(text="Generate Password", width=15, command=generate_password)
generate_password_button.grid(row=3, column=2)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(row=1, column=2)
window.mainloop()
