from tkinter import *
from tkinter import messagebox
import mysql.connector
import hashlib
import random

mydb = mysql.connector.connect(host="localhost", user="sqluser", password="password", database="srs_data")
mycursor = mydb.cursor(buffered=True)

#check sql data type length and that all exceptions are handled accordingly when signig up or smth/creating stuff
window = Tk()
window.title("Spaced Repetition Flashcard Software")
window['bg']="#e6e7f0"
window.resizable(False, False)

class Flashcard:
    def __init__(self, id, question, answer, priority):
        self.id = id
        self.question = question
        self.answer = answer
        self.priority = priority

class PeerFlashcard(Flashcard):
    def __init__(self, id, question, answer, priority, input):
        super().__init__(id, question, answer, priority)
        self.input = input

class CircularPriorityQueue:
    def __init__(self, size):
        self.front = -1
        self.rear = -1
        self.maxsize = size
        self.queue = [None] * self.maxsize

    def isEmpty(self):
        return self.front == -1 and self.rear == -1
    
    def isFull(self):
        return (self.rear + 1) % self.maxsize == self.front
    
    def enQueue(self, flashcard):
        if flashcard.priority == -1: #to allow unused cards to be placed randomly in queue
            flashcard.priority = float(random.randint(0, 10)) #float data type to identify new flashcards so they can be prioritised according to their "new" status
            priority = flashcard.priority
        else:
            priority = flashcard.priority
        if self.isFull():
            return None
        elif self.isEmpty():
            self.front = 0
            self.rear = 0
            self.queue[self.rear] = flashcard
        else:
            position = self.front
            while position != self.rear and self.queue[position].priority >= priority: #checking all cards from front until finding one with lower priority
                position = (position + 1) % self.maxsize

            if position == self.rear: #works if self.rear == 0
                if self.queue[position].priority >= priority: #if priorities are equal, the new flashcard will be placed behind
                    self.rear = (self.rear + 1) % self.maxsize
                    self.queue[self.rear] = flashcard
                elif self.queue[position].priority < priority: #shuffle self.rear along 1
                    item = self.queue[position]
                    self.rear = (self.rear + 1) % self.maxsize
                    self.queue[self.rear] = item
                    self.queue[position] = flashcard
            else: #shuffle all flashcards after target position along 1
                card_position = self.rear
                while card_position != (position - 1) % self.maxsize:
                    item = self.queue[card_position]
                    new_card_position = (card_position + 1) % self.maxsize
                    self.queue[new_card_position] = item
                    card_position = (card_position - 1) % self.maxsize
                self.rear = (self.rear + 1) % self.maxsize
                self.queue[position] = flashcard

    def deQueue(self):
        if self.isEmpty():
            return None
        else:
            item = self.queue[self.front]
            if self.front == self.rear:
                self.front = -1
                self.rear = -1
            else:
                self.front = (self.front + 1) % self.maxsize
            return item
        
    def getQueue(self):
        return list((flashcard.id, flashcard.priority) for flashcard in self.queue if flashcard is not None)
    
class Stack:
    def __init__(self, size):
        self.top = -1
        self.maxsize = size
        self.stack = [None] * self.maxsize

    def isEmpty(self):
        return self.top == -1
    
    def isFull(self):
        return self.top + 1 == self.maxsize
    
    def push(self, flashcard):
        if self.isFull():
            return None
        else:
            self.top += 1
            self.stack[self.top] = flashcard

    def pop(self):
        if self.isEmpty():
            return None
        else:
            flashcard = self.stack[self.top]
            self.top -= 1
            return flashcard
        
    def getStack(self):
        return list((flashcard.id, flashcard.question, flashcard.input) for flashcard in self.stack if flashcard is not None)

fill_widget = {
    "fill": BOTH,
    "expand": True
}

stretch_widget = {
    "side": TOP,
    "fill": X
}

footer_widget = {
    "side": BOTTOM,
    "fill": X
}

vertical_scrollbar = {
    "side": RIGHT,
    "fill": Y
}

login_label = {
    "bg": "#e6e7f0",
    "font": ("Helvetica", 12)
}

header_label = {
    "bg": "#d7d8e0",
    "font": ("Helvetica", 9)
}

option_label = {
    "bg": "#d7d8e0",
    "font": ("Helvetica", 11)
}

notification_label = {
    "bg": "#e6e7f0",
    "font": ("Helvetica", 9)
}

supertitle_label = {
    "bg": "#e6e7f0",
    "font": ("Helvetica", 12, "bold")
}

title_label = {
    "bg": "#e6e7f0",
    "font": ("Helvetica", 14)
}

top_button = {
    "bg": "#bfc0c7",
    "font": ("Helvetica", 9)
}

select_list = {
    "relief": FLAT,
    "selectmode": SINGLE,
    "selectbackground": "#bfc0c7"
}

button_on = {
    "bg": "#ffffff",
    "relief": SUNKEN
}

button_off = {
    "bg": "#d7d8e0",
    "relief": RAISED
}

button2_off = {
    "bg": "#bfc0c7",
    "relief": RAISED
}

class page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()
        
class loginPage(page):
    def __init__(self, *args, **kwargs):
        page.__init__(self, *args, **kwargs)

        self.login_page = Frame(self, bg="#e6e7f0")

        self.front_title = Label(self.login_page, bg="#d7d8e0", font=("Helvetica", 15, "bold"), text="Spaced Repetition Flashcard Software")
        self.front_title.pack()

        self.username_label = Label(self.login_page, **login_label, text="Username")
        self.username_label.pack()
        self.username_entry = Entry(self.login_page)
        self.username_entry.pack()

        self.password_label = Label(self.login_page, **login_label, text="Password")
        self.password_label.pack()
        self.password_entry = Entry(self.login_page, show="*")
        self.password_entry.pack()

        self.login_button = Button(
            self.login_page,
            text="Log in", 
            font=("Helvetica", 9),
            command=self.login
            )
        self.login_button.pack()
        self.to_signup_button = Button(
            self.login_page, 
            text="Sign up", 
            font=("Helvetica", 9),
            command=self.show_signupPage
            )
        self.to_signup_button.pack()

        self.login_page.pack(**fill_widget)

    def login(self):
        global username_login
        username_login = self.username_entry.get()
        password_login = self.password_entry.get()
        hashed_login = self.hashing_login(password_login)

        mycursor.execute("SELECT * FROM user_account WHERE username = %s AND password = %s", (username_login, hashed_login))
        if mycursor.fetchone():
            app.showButtons()
            page1.show_dashboard() #use username coz its the only column that requires to be unique across all records
        else:
            messagebox.showerror("Invalid Login", "Username or password is incorrect.")

    def hashing_login(self, password_login):
        return (hashlib.sha256(password_login.encode("utf-8"))).hexdigest()
    
    def show_signupPage(self):
        page00.show()

class signupPage(page):
    def __init__(self, *args, **kwargs):
        page.__init__(self, *args, **kwargs)

        self.signup_page = Frame(self, bg="#e6e7f0")

        self.new_firstname_label = Label(self.signup_page, **login_label, text="First name")
        self.new_firstname_label.pack()
        self.new_firstname_entry = Entry(self.signup_page)
        self.new_firstname_entry.pack()

        self.new_lastname_label = Label(self.signup_page, **login_label, text="Last name")
        self.new_lastname_label.pack()
        self.new_lastname_entry = Entry(self.signup_page)
        self.new_lastname_entry.pack()

        self.new_username_label = Label(self.signup_page, **login_label, text="Username")
        self.new_username_label.pack()
        self.new_username_entry = Entry(self.signup_page)
        self.new_username_entry.pack()

        self.new_password_label = Label(self.signup_page, **login_label, text="Password")
        self.new_password_label.pack()
        self.new_password_entry = Entry(self.signup_page, show="*")
        self.new_password_entry.pack()

        self.confirm_password_label = Label(self.signup_page, **login_label, text="Confirm password")
        self.confirm_password_label.pack()
        self.confirm_password_entry = Entry(self.signup_page, show="*")
        self.confirm_password_entry.pack()

        self.signup_button = Button(
            self.signup_page, 
            text="Sign up", 
            font=("Helvetica", 9),
            command=self.signup
            )
        self.signup_button.pack()
        self.to_login_button = Button(
            self.signup_page, 
            text="Back", 
            font=("Helvetica", 9),
            command=self.show_loginPage
            )
        self.to_login_button.pack()

        self.signup_page.pack(**fill_widget)

    def signup(self):
        new_firstname = self.new_firstname_entry.get()
        if self.validate_name(new_firstname):
            messagebox.showerror("Invalid First Name", "First name must be between 1 and 30 characters in length.")
        else:

            new_lastname = self.new_lastname_entry.get()
            if self.validate_name(new_lastname):
                messagebox.showerror("Invalid Last Name", "Last name must be between 1 and 30 characters in length.")
            else:

                new_username = self.new_username_entry.get()
                if self.validate_username(new_username) == 1:
                    messagebox.showerror("Invalid Username", "Username can only contain letters, numbers and _ or - symbols.")
                elif self.validate_username(new_username) == 2:
                    messagebox.showerror("Invalid Username", "Username must be between 1 and 20 characters in length.")
                elif self.validate_username(new_username) == 3:
                    messagebox.showerror("Invalid Username", "Username already registered.")
                else:

                    new_password = self.new_password_entry.get()
                    if self.validate_password(new_password) == 1:
                        messagebox.showerror("Invalid Password", "Password must contain both letters and numbers.")
                    elif self.validate_password(new_password) == 2:
                        messagebox.showerror("Invalid Password", "Password must be between 8 and 100 characters in length.")
                    else:

                        confirm_password = self.confirm_password_entry.get()
                        if new_password != confirm_password:
                            messagebox.showerror("Invalid Password", "Passwords do not match.")
                        else:
                            hashed_password = self.hash_password(new_password)
                            mycursor.execute("INSERT INTO user_account (username, firstName, lastName, password) VALUES (%s, %s, %s, %s)", (new_username, new_firstname, new_lastname, hashed_password))
                            mydb.commit()
                            self.show_confirmation(new_username)

    def validate_name(self, new_name):
        if len(new_name) > 30 or len(new_name) < 1:
            return True
        
    def validate_username(self, new_username):
        if not all(char.isalnum() or char in ["_", "-"] for char in new_username):
            return 1
        elif len(new_username) > 20 or len(new_username) < 1:
            return 2
        else:
            mycursor.execute("SELECT * FROM user_account WHERE username = %s", (new_username,)) #case sensitive
            if mycursor.fetchone():
                return 3
            
    def validate_password(self, new_password):
        if not (any(char.isalpha() for char in new_password) and any(char.isdigit() for char in new_password)):
            return 1
        elif len(new_password) > 100 or len(new_password) < 8:
            return 2
        
    def hash_password(self, new_password):
        return (hashlib.sha256(new_password.encode("utf-8"))).hexdigest()
    
    def show_confirmation(self, new_username):
        self.show_loginPage()
        messagebox.showinfo("Account Creation", f"Welcome {new_username}!\nPlease log in with your new account.")

    def show_loginPage(self):
        page0.show()
        
class collectionPage(page):
    def __init__(self, *args, **kwargs):
        page.__init__(self, *args, **kwargs)

        self.fullname = StringVar()
        self.friendsnumber = StringVar()

        self.collection_page = Frame(self, bg="#e6e7f0")

        self.header_buttons = Frame(self.collection_page, bg="#d7d8e0")
        self.fullname_label = Label(self.header_buttons, **header_label, textvariable=self.fullname)
        self.fullname_label.pack(side=LEFT)
        
        self.settings_button = Button(self.header_buttons, **top_button, text="Settings", command=self.settings_window)
        self.settings_button.pack(side=RIGHT)
        self.friends_button = Button(self.header_buttons, **top_button, textvariable=self.friendsnumber, command=self.friends_window)
        self.friends_button.pack(side=RIGHT)
        self.newdeck_button = Button(self.header_buttons, **top_button, text="New Deck", command=self.newdeck_window)
        self.newdeck_button.pack(side=RIGHT)
        self.header_buttons.pack(**stretch_widget)

        self.collection_page.pack(**fill_widget)

    def settings_window(self):
        def friends_on():
            if self.friends_on_button.cget("bg") == "#d7d8e0":
                self.friends_on_button.config(**button_on)
                self.friends_off_button.config(**button_off)
                mycursor.execute("UPDATE user_account SET friendRequest = 'on' WHERE username = %s", (username_login,))
                mydb.commit()

        def friends_off():
            if self.friends_off_button.cget("bg") == "#d7d8e0":
                self.friends_on_button.config(**button_off)
                self.friends_off_button.config(**button_on)
                mycursor.execute("UPDATE user_account SET friendRequest = 'off' WHERE username = %s", (username_login,))
                mydb.commit()

        def marking_on():
            if self.marking_on_button.cget("bg") == "#d7d8e0":
                self.marking_on_button.config(**button_on)
                self.marking_off_button.config(**button_off)
                mycursor.execute("UPDATE user_account SET markingRequest = 'on' WHERE username = %s", (username_login,))
                mydb.commit()

        def marking_off():
            if self.marking_off_button.cget("bg") == "#d7d8e0":
                self.marking_on_button.config(**button_off)
                self.marking_off_button.config(**button_on)
                mycursor.execute("UPDATE user_account SET markingRequest = 'off' WHERE username = %s", (username_login,))
                mydb.commit()

        self.settingsPage = Toplevel()
        self.settingsPage.title("Settings")
        self.settingsPage.resizable(False, False)

        self.settings_page = Frame(self.settingsPage, bg="#e6e7f0")

        self.friends_section = Frame(self.settings_page, bg="#d7d8e0")
        self.friends_label = Label(self.friends_section, **option_label, text="Friend requests")
        self.friends_label.pack(side=LEFT)
        self.friends_section.pack(**stretch_widget)

        self.friends_buttons = Frame(self.settings_page, bg="#e6e7f0", pady=6)
        self.friends_on_button = Button(self.friends_buttons, **header_label, text="On", command=friends_on)
        self.friends_on_button.pack(side=LEFT)
        self.friends_off_button = Button(self.friends_buttons, **header_label, text="Off", command=friends_off)
        self.friends_off_button.pack(side=LEFT)
        self.friends_buttons.pack(**stretch_widget)

        mycursor.execute("SELECT friendRequest FROM user_account WHERE username = %s", (username_login,))
        friend_result = mycursor.fetchone()
        if friend_result[0] == "on":
            self.friends_on_button.config(**button_on)
        elif friend_result[0] == "off":
            self.friends_off_button.config(**button_on)

        self.marking_section = Frame(self.settings_page, bg="#d7d8e0")
        self.marking_label = Label(self.marking_section, **option_label, text="Marking requests")
        self.marking_label.pack(side=LEFT)
        self.marking_section.pack(**stretch_widget)
        
        self.marking_buttons = Frame(self.settings_page, bg="#e6e7f0", pady=6)
        self.marking_on_button = Button(self.marking_buttons, **header_label, text="On", command=marking_on)
        self.marking_on_button.pack(side=LEFT)
        self.marking_off_button = Button(self.marking_buttons, **header_label, text="Off", command=marking_off)
        self.marking_off_button.pack(side=LEFT)
        self.marking_buttons.pack(**stretch_widget)

        mycursor.execute("SELECT markingRequest FROM user_account WHERE username = %s", (username_login,))
        marking_result = mycursor.fetchone()
        if marking_result[0] == "on":
            self.marking_on_button.config(**button_on)
        elif marking_result[0] == "off":
            self.marking_off_button.config(**button_on)

        self.settings_page.pack(**fill_widget)
        
    def friends_window(self):
        def check_friend():
            friend_username = self.friend_input.get()
            if not friend_username:
                messagebox.showerror("Invalid Username", "Username is empty.")
            else:
                if friend_username == username_login:
                    messagebox.showerror("Invalid Username", "You cannot send a friend request to yourself.")
                else:
                    mycursor.execute("SELECT * FROM user_account WHERE username = %s", (friend_username,))
                    if mycursor.fetchone():
                        mycursor.execute("SELECT * FROM user_friend INNER JOIN user_account ua1 ON ua1.accountID = user_friend.accountID INNER JOIN user_account ua2 ON ua2.accountID = user_friend.accountID2 WHERE ua1.username = %s AND ua2.username = %s", (username_login, friend_username))
                        if mycursor.fetchone(): #also for if you have already sent friend request, or the user has already sent friend request to you
                            messagebox.showerror("Invalid Username", "You are already friends with this user.")
                        else:
                            mycursor.execute("SELECT * FROM user_friendrequest INNER JOIN user_account ua1 ON ua1.accountID = user_friendrequest.accountID INNER JOIN user_account ua2 ON ua2.accountID = user_friendrequest.accountID2 WHERE ua1.username = %s AND ua2.username = %s", (username_login, friend_username))
                            if mycursor.fetchone():
                                messagebox.showerror("Invalid Username", "You have already sent a friend request to this user.")
                            else:
                                mycursor.execute("SELECT * FROM user_friendrequest INNER JOIN user_account ua1 ON ua1.accountID = user_friendrequest.accountID INNER JOIN user_account ua2 ON ua2.accountID = user_friendrequest.accountID2 WHERE ua1.username = %s AND ua2.username = %s", (friend_username, username_login))
                                if mycursor.fetchone():
                                    messagebox.showerror("Invalid Username", "This user has already sent you a friend request.")
                                else:
                                    mycursor.execute("SELECT * FROM user_account WHERE username = %s AND friendRequest = 'off'", (friend_username,))
                                    if mycursor.fetchone():
                                        messagebox.showerror("Invalid Username", "This user has friend requests turned off.")
                                    else:
                                        mycursor.execute("INSERT INTO user_friendrequest (accountID, accountID2) VALUES ((SELECT user_account.accountID FROM user_account WHERE user_account.username = %s), (SELECT user_account.accountID FROM user_account WHERE user_account.username = %s))", (username_login, friend_username))
                                        mydb.commit()
                                        messagebox.showinfo("Friend Request Sent", f"Your friend request to {friend_username} has been sent and is now pending.")
                    else:
                        messagebox.showerror("Invalid Username", "This user does not exist.")

        def forget_request(request_username, inner_frame, requesting_user, accept_button, deny_button):
            inner_frame.pack_forget()
            requesting_user.pack_forget()
            accept_button.pack_forget()
            deny_button.pack_forget()
            mycursor.execute("DELETE user_friendrequest FROM user_friendrequest INNER JOIN user_account ua1 ON ua1.accountID = user_friendrequest.accountID WHERE ua1.username = %s AND user_friendrequest.accountID2 = (SELECT ua2.accountID FROM user_account AS ua2 WHERE ua2.username=%s)", (request_username, username_login))
            mydb.commit()

        def accept_request(request_username, inner_frame, requesting_user, accept_button, deny_button):
            self.friends_list.insert(END, request_username)
            mycursor.execute("INSERT INTO user_friend (accountID, accountID2) VALUES ((SELECT user_account.accountID FROM user_account WHERE user_account.username = %s), (SELECT user_account.accountID FROM user_account WHERE user_account.username = %s))", (username_login, request_username))
            mydb.commit()
            mycursor.execute("INSERT INTO user_friend (accountID, accountID2) VALUES ((SELECT user_account.accountID FROM user_account WHERE user_account.username = %s), (SELECT user_account.accountID FROM user_account WHERE user_account.username = %s))", (request_username, username_login))
            mydb.commit()
            forget_request(request_username, inner_frame, requesting_user, accept_button, deny_button)

        self.friendsPage = Toplevel()
        self.friendsPage.title("Friends")
        self.friendsPage.resizable(False, False)
        
        self.friend_info = self.fetch_friendinfo()
        self.friendrequest_info = self.fetch_friendrequestinfo()

        self.friends_page = Frame(self.friendsPage, bg="#e6e7f0")

        self.friendslist_header = Frame(self.friends_page, bg="#d7d8e0")
        self.friendslist_label = Label(self.friendslist_header, **option_label, text="Friends list")
        self.friendslist_label.pack(side=LEFT)
        self.friendslist_header.pack(**stretch_widget)

        self.friendslist_frame = Frame(self.friends_page, bg="#e6e7f0")
        self.friendslist_scrollbar = Scrollbar(self.friendslist_frame)
        self.friendslist_scrollbar.pack(**vertical_scrollbar)
        self.friends_list = Listbox(self.friendslist_frame, **notification_label, yscrollcommand=self.friendslist_scrollbar.set, relief=FLAT, selectmode=SINGLE, selectbackground="#e6e7f0", selectforeground="#000000", activestyle="none")
        self.friends_list.pack(**fill_widget)
        self.friendslist_frame.pack(**fill_widget)
        self.friendslist_scrollbar.config(command = self.friends_list.yview)

        self.friendrequests_header = Frame(self.friends_page, bg="#d7d8e0")
        self.friendrequests_label = Label(self.friendrequests_header, **option_label, text="Friend requests")
        self.friendrequests_label.pack(side=LEFT)
        self.friendrequests_header.pack(**stretch_widget)

        self.friendrequests_frame = Frame(self.friends_page, bg="#e6e7f0")
        self.friendrequests_frame.pack()

        self.addfriend_header = Frame(self.friends_page, bg="#d7d8e0")
        self.addfriend_label = Label(self.addfriend_header, **header_label, text="Enter username:")
        self.addfriend_label.pack(side=LEFT)
        self.friend_input = Entry(self.addfriend_header)
        self.friend_input.pack(side=LEFT, fill=X)
        self.add_button = Button(self.addfriend_header, **top_button, text="Add friend", command=check_friend)
        self.add_button.pack(side=RIGHT)
        self.addfriend_header.pack(**footer_widget)

        self.friends_page.pack(**fill_widget)

        if not self.friend_info:
            pass
        else:
            for friend in self.friend_info:
                self.friends_list.insert(END, friend[0])

        if not self.friendrequest_info:
            pass
        else:
            for request in self.friendrequest_info:
                inner_frame = Frame(self.friendrequests_frame, bg="#e6e7f0")
                requesting_user = Label(inner_frame, **notification_label, text=f"{request[1]} {request[2]} ({request[0]}) has sent you a friend request.")
                requesting_user.pack(side=LEFT)
                accept_button = Button(inner_frame, font=("Helvetica", 9), text="Accept")
                accept_button.pack(side=LEFT)
                deny_button = Button(inner_frame, font=("Helvetica", 9), text="Deny")
                deny_button.pack(side=LEFT)
                inner_frame.pack(**fill_widget)

                accept_button.config(command=lambda request=request, inner_frame=inner_frame, requesting_user=requesting_user, accept_button=accept_button, deny_button=deny_button: accept_request(request[0], inner_frame, requesting_user, accept_button, deny_button))
                deny_button.config(command=lambda request=request, inner_frame=inner_frame, requesting_user=requesting_user, accept_button=accept_button, deny_button=deny_button: forget_request(request[0], inner_frame, requesting_user, accept_button, deny_button))

    def newdeck_window(self):
        def create_deck():
            deck_name = self.deckname_entry.get() #increase cjaracters in deck name - 50
            mycursor.execute("SELECT * FROM user_deck INNER JOIN user_account ON user_account.accountID = user_deck.accountID WHERE user_deck.deckName = %s AND user_account.username = %s", (deck_name, username_login)) #case sensitive
            if mycursor.fetchone():
                messagebox.showerror("Invalid Deck Name", "You already have a deck with this name.")#add more constraints(length)
            else:
                mycursor.execute("INSERT INTO user_deck (accountID, deckName) VALUES ((SELECT user_account.accountID FROM user_account WHERE user_account.username = %s), %s)", (username_login, deck_name))
                mydb.commit()
                self.newdeckPage.destroy()
                page1.show_dashboard() #refresh

        self.newdeckPage = Toplevel()
        self.newdeckPage.title("Create Deck")
        self.newdeckPage.resizable(False, False)

        self.deck_page = Frame(self.newdeckPage, bg="#e6e7f0")

        self.deckname_header = Frame(self.deck_page, bg="#d7d8e0")
        self.deckname_label = Label(self.deckname_header, **option_label, text="Deck name")
        self.deckname_label.pack(side=LEFT)
        self.deckname_header.pack(**stretch_widget)

        self.decknameentry_frame = Frame(self.deck_page, bg="#e6e7f0")
        self.deckname_entry = Entry(self.decknameentry_frame)
        self.deckname_entry.pack(side=LEFT)
        self.decknameentry_frame.pack(**stretch_widget)

        self.createdeck_button = Button(self.deck_page, **header_label, text="Create", command=create_deck)
        self.createdeck_button.pack(**stretch_widget)

        self.deck_page.pack(**fill_widget)

    def deck_selected(self, event): #event taken as an argument due to bind
        def refresh_flashcards():
            def delete_flashcard(flashcard_list):
                selected_flashcard = "".join(flashcard_list.get(i) for i in flashcard_list.curselection())
                message_answer = messagebox.askokcancel("Delete Flashcard", "Are you sure you want to delete this flashcard?")
                if message_answer:
                    if (flashcard_list.curselection())[0] % 2 == 0:
                        mycursor.execute("DELETE user_peermarked FROM user_peermarked INNER JOIN user_flashcard ON user_flashcard.flashcardID = user_peermarked.flashcardID WHERE user_flashcard.question = %s AND (user_flashcard.deckID = (SELECT user_deck.deckID FROM user_deck WHERE user_deck.deckName = %s AND user_deck.accountID = (SELECT user_account.accountID FROM user_account WHERE user_account.username = %s)))", (selected_flashcard, selected_deck, username_login))
                        mydb.commit()
                        mycursor.execute("DELETE user_peermarking FROM user_peermarking INNER JOIN user_flashcard ON user_flashcard.flashcardID = user_peermarking.flashcardID WHERE user_flashcard.question = %s AND (user_flashcard.deckID = (SELECT user_deck.deckID FROM user_deck WHERE user_deck.deckName = %s AND user_deck.accountID = (SELECT user_account.accountID FROM user_account WHERE user_account.username = %s)))", (selected_flashcard, selected_deck, username_login))
                        mydb.commit()
                        mycursor.execute("DELETE user_flashcard FROM user_flashcard INNER JOIN user_deck ON user_deck.deckID = user_flashcard.deckID WHERE user_flashcard.question = %s AND (user_flashcard.deckID = (SELECT user_deck.deckID FROM user_deck WHERE user_deck.deckName = %s AND user_deck.accountID = (SELECT user_account.accountID FROM user_account WHERE user_account.username = %s)))", (selected_flashcard, selected_deck, username_login))
                        mydb.commit()
                    else:
                        mycursor.execute("DELETE user_peermarked FROM user_peermarked INNER JOIN user_flashcard ON user_flashcard.flashcardID = user_peermarked.flashcardID WHERE user_flashcard.answer = %s AND (user_flashcard.deckID = (SELECT user_deck.deckID FROM user_deck WHERE user_deck.deckName = %s AND user_deck.accountID = (SELECT user_account.accountID FROM user_account WHERE user_account.username = %s)))", (selected_flashcard, selected_deck, username_login))
                        mydb.commit()
                        mycursor.execute("DELETE user_peermarking FROM user_peermarking INNER JOIN user_flashcard ON user_flashcard.flashcardID = user_peermarking.flashcardID WHERE user_flashcard.answer = %s AND (user_flashcard.deckID = (SELECT user_deck.deckID FROM user_deck WHERE user_deck.deckName = %s AND user_deck.accountID = (SELECT user_account.accountID FROM user_account WHERE user_account.username = %s)))", (selected_flashcard, selected_deck, username_login))
                        mydb.commit()
                        mycursor.execute("DELETE user_flashcard FROM user_flashcard INNER JOIN user_deck ON user_deck.deckID = user_flashcard.deckID WHERE user_flashcard.answer = %s AND (user_flashcard.deckID = (SELECT user_deck.deckID FROM user_deck WHERE user_deck.deckName = %s AND user_deck.accountID = (SELECT user_account.accountID FROM user_account WHERE user_account.username = %s)))", (selected_flashcard, selected_deck, username_login))
                        mydb.commit()
                    refresh_flashcards()
                    
            for widget in self.flashcardlist_frame.winfo_children():
                if not isinstance(widget, (Listbox, Scrollbar)):
                    continue
                widget.destroy()
                
            flashcard_yscrollbar = Scrollbar(self.flashcardlist_frame)
            flashcard_yscrollbar.pack(**vertical_scrollbar)
            flashcard_xscrollbar = Scrollbar(self.flashcardlist_frame)
            flashcard_xscrollbar.pack(**footer_widget)
            flashcard_list = Listbox(self.flashcardlist_frame, **notification_label, **select_list, yscrollcommand=flashcard_yscrollbar.set, xscrollcommand=flashcard_xscrollbar.set, width=50)
            flashcards = self.fetch_flashcards()
            for flashcard in flashcards:
                flashcard_list.insert(END, flashcard[1])
                flashcard_list.itemconfig(END, bg="#d7d8e0")
                flashcard_list.insert(END, flashcard[2])
            flashcard_list.pack(**fill_widget)
            flashcard_list.bind("<Double-1>", lambda event:delete_flashcard(flashcard_list))
            flashcard_yscrollbar.config(command=flashcard_list.yview)
            flashcard_xscrollbar.config(command=flashcard_list.xview)

        def add_flashcards():
            def add_flashcard(question_entry, answer_entry):
                question = question_entry.get("1.0", "end-1c") #add constraints eg length of question, answer... (probably increase length coz wtf)
                answer = answer_entry.get("1.0", "end-1c")

                mycursor.execute("SELECT * FROM user_flashcard INNER JOIN user_deck ON user_deck.deckID = user_flashcard.deckID INNER JOIN user_account ON user_account.accountID = user_deck.accountID WHERE user_flashcard.question = %s AND user_deck.deckName = %s AND user_account.username = %s", (question, selected_deck, username_login))
                if mycursor.fetchone():
                    messagebox.showerror("Invalid Flashcard", "You already have a flashcard with this question in this deck.")
                else:
                    mycursor.execute("INSERT INTO user_flashcard (deckID, question, answer) VALUES ((SELECT user_deck.deckID FROM user_deck INNER JOIN user_account ON user_account.accountID = user_deck.accountID WHERE user_deck.deckName = %s AND user_account.username = %s), %s, %s)", (selected_deck, username_login, question, answer))#replace subquery within subquery for INSERT or anything else with inner join
                    mydb.commit()
                    question_entry.delete("1.0", "end")
                    answer_entry.delete("1.0", "end")
                    refresh_flashcards()

            global addflashcardPage
            addflashcardPage = Toplevel()
            addflashcardPage.title(selected_deck)
            addflashcardPage.resizable(False, False)

            addflashcard_page = Frame(addflashcardPage, bg="#e6e7f0")

            flashcardquestion_header = Frame(addflashcard_page, bg="#d7d8e0")
            flashcardquestion_label = Label(flashcardquestion_header, **option_label, text="Question")
            flashcardquestion_label.pack(side=LEFT)
            flashcardquestion_header.pack(**stretch_widget)

            questionentry_frame = Frame(addflashcard_page, bg="#e6e7f0")
            question_entry = Text(questionentry_frame, width=30, height=4)
            question_entry.pack(side=LEFT)
            questionentry_frame.pack(**stretch_widget)

            flashcardanswer_header = Frame(addflashcard_page, bg="#d7d8e0")
            flashcardanswer_label = Label(flashcardanswer_header, **option_label, text="Answer")
            flashcardanswer_label.pack(side=LEFT)
            flashcardanswer_header.pack(**stretch_widget)

            answerentry_frame = Frame(addflashcard_page, bg="#e6e7f0")
            answer_entry = Text(answerentry_frame, width=30, height=7)
            answer_entry.pack(side=LEFT)
            answerentry_frame.pack(**stretch_widget)

            addflashcard_frame = Frame(addflashcard_page, bg="#e6e7f0")
            addflashcard_button = Button(addflashcard_frame, **header_label, text="Add", command=lambda:add_flashcard(question_entry, answer_entry))
            addflashcard_button.pack(**stretch_widget)
            addflashcard_frame.pack(**stretch_widget)

            addflashcard_page.pack(**fill_widget)
        
        def check_review():
            def review_flashcards(): #indirect recursion? base case is when deQueue returns None (i.e. queue is empty) or number > 10
                def queue_flashcards(flashcards, flashcard_queue):
                    for flashcard in flashcards:
                        flashcard = Flashcard(flashcard[0], flashcard[1], flashcard[2], flashcard[3])
                        flashcard_queue.enQueue(flashcard)

                def answer_review(review_flashcards_page, new_flashcard, question_header, input_text, flip_button, flashcard_counter, reviewed_list, peer_review_stack, text_frame, button_frame, flashcard_queue):
                    def update_priority(new_flashcard, new_priority, reviewed_list):
                        new_priority = max(0, min(10, new_priority))
                        mycursor.execute("UPDATE user_flashcard SET priority = %s WHERE flashcardID = %s", (new_priority, new_flashcard.id)) #make sure flashcards with lowest priority arent just left at the back forever - if all cards are the same priority, randomise?
                        mydb.commit()
                        reviewed_list.append([new_flashcard.id, new_flashcard.question, new_flashcard.answer, new_priority]) #no option to edit DURING reviews

                    def flashcard_rating1(new_flashcard, reviewed_list):
                        if isinstance(new_flashcard.priority, float):
                            new_priority = 9
                        else:
                            new_priority = new_flashcard.priority + 2 #low increment coz program assumes that you will do better on next review considering you've just looked at the flashcard.
                        update_priority(new_flashcard, new_priority, reviewed_list)

                    def flashcard_rating2(new_flashcard, reviewed_list):
                        if isinstance(new_flashcard.priority, float):
                            new_priority = 7
                        else:
                            new_priority = new_flashcard.priority + 1 #add or minus 1 means that all possible rating numbers (0-10) will be used
                        update_priority(new_flashcard, new_priority, reviewed_list)

                    def flashcard_rating3(new_flashcard, reviewed_list):
                        if isinstance(new_flashcard.priority, float):
                            new_priority = 5
                        else:
                            new_priority = new_flashcard.priority - 1
                        update_priority(new_flashcard, new_priority, reviewed_list)

                    def flashcard_rating4(new_flashcard, reviewed_list): #so that cards selected as "easy" don't automatically have lowest priority - need more than 1 "easy"
                        if isinstance(new_flashcard.priority, float):
                            new_priority = 3
                        else:
                            new_priority = new_flashcard.priority - 2
                        update_priority(new_flashcard, new_priority, reviewed_list)

                    def check_peermark(review_flashcards_page, new_flashcard, reviewed_list, peer_review_stack, text_frame, button_frame, flashcard_queue):
                        def peer_rating_push(review_flashcards_page, new_flashcard, reviewed_list, peer_review_stack, text_frame, button_frame, flashcard_queue):
                            peer_flashcard = PeerFlashcard(new_flashcard.id, new_flashcard.question, new_flashcard.answer, new_flashcard.priority, user_input)
                            peer_review_stack.push(peer_flashcard)
                            print(peer_review_stack.getStack())
                            reviewed_list.append([new_flashcard.id, new_flashcard.question, new_flashcard.answer, new_flashcard.priority])
                            question_review(review_flashcards_page, flashcard_counter, reviewed_list, peer_review_stack, text_frame, button_frame, flashcard_queue)

                        mycursor.execute("SELECT * FROM user_peermarking INNER JOIN user_account ON user_account.accountID = user_peermarking.accountID WHERE user_peermarking.flashcardID = %s AND user_account.username = %s", (new_flashcard.id, username_login))
                        if mycursor.fetchone():
                            messagebox.showerror("Invalid Flashcard", "This flashcard is already pending a response in a different peer marking submission.")
                        else:
                            mycursor.execute("SELECT ua2.username FROM user_account ua1 INNER JOIN user_friend ON user_friend.accountID = ua1.accountID INNER JOIN user_account ua2 ON ua2.accountID = user_friend.accountID2 WHERE ua1.username = %s", (username_login,))
                            if mycursor.fetchone():
                                mycursor.execute("SELECT ua2.username FROM user_account ua1 INNER JOIN user_friend ON user_friend.accountID = ua1.accountID INNER JOIN user_account ua2 ON ua2.accountID = user_friend.accountID2 WHERE ua1.username = %s AND ua2.markingRequest = 'on'", (username_login,))
                                if mycursor.fetchone():
                                    peer_rating_push(review_flashcards_page, new_flashcard, reviewed_list, peer_review_stack, text_frame, button_frame, flashcard_queue)
                                else:
                                    messagebox.showerror("Unable to Peer Mark", "None of your friends have peer marking turned on.")
                            else:
                                messagebox.showerror("Unable to Peer Mark", "Friends are required for sending peer marking submissions.")
                        
                    user_input = input_text.get("1.0", "end-1c")
                    question_header.pack_forget()
                    flip_button.pack_forget()
                    input_text.pack_forget()

                    answer_header = Label(text_frame, **title_label, text=f"{new_flashcard.answer}", wraplength=500, pady=5)
                    answer_header.pack()
                    output_header = Label(text_frame, **notification_label, text="You wrote:")
                    output_header.pack()
                    output_text = Label(text_frame, font=("Helvetica", 10), bg="#e6e7f0", text=f"{user_input}", wraplength=450)
                    output_text.pack()

                    rating1_button = Button(button_frame, **top_button, text="Fail", command=lambda:[flashcard_rating1(new_flashcard, reviewed_list), question_review(review_flashcards_page, flashcard_counter, reviewed_list, peer_review_stack, text_frame, button_frame, flashcard_queue)]) #in order of function being called
                    rating1_button.pack(side=LEFT)
                    rating2_button = Button(button_frame, **top_button, text="Hard", command=lambda:[flashcard_rating2(new_flashcard, reviewed_list), question_review(review_flashcards_page, flashcard_counter, reviewed_list, peer_review_stack, text_frame, button_frame, flashcard_queue)])
                    rating2_button.pack(side=LEFT)
                    rating3_button = Button(button_frame, **top_button, text="Good", command=lambda:[flashcard_rating3(new_flashcard, reviewed_list), question_review(review_flashcards_page, flashcard_counter, reviewed_list, peer_review_stack, text_frame, button_frame, flashcard_queue)])
                    rating3_button.pack(side=LEFT)
                    rating4_button = Button(button_frame, **top_button, text="Easy", command=lambda:[flashcard_rating4(new_flashcard, reviewed_list), question_review(review_flashcards_page, flashcard_counter, reviewed_list, peer_review_stack, text_frame, button_frame, flashcard_queue)])
                    rating4_button.pack(side=LEFT)

                    peer_button = Button(button_frame, **top_button, text="Peer Mark", command=lambda:[check_peermark(review_flashcards_page, new_flashcard, reviewed_list, peer_review_stack, text_frame, button_frame, flashcard_queue)])
                    peer_button.pack(side=RIGHT)

                def question_review(review_flashcards_page, flashcard_counter, reviewed_list, peer_review_stack, text_frame, button_frame, flashcard_queue):
                    def end_review(review_flashcards_page, peer_review_stack, flashcard_counter, reviewed_list, text_frame, button_frame, flashcard_queue):
                        def review_show(review_flashcards_page, flashcard_counter, reviewed_list, text_frame, button_frame, flashcard_queue):
                            def review_again(review_flashcards_page, flashcard_counter, reviewed_list, text_frame, button_frame, flashcard_queue):
                                peer_review_stack = Stack(deck_size)
                                for i in range(0, len(reviewed_list)): #list used (instead of stack/queue bc...) (this list basically functions as a queue anyway, but the order isn't relevant because it'll be arranged by priority by cpq)
                                    again_flashcard = Flashcard(reviewed_list[i][0], reviewed_list[i][1], reviewed_list[i][2], reviewed_list[i][3])
                                    flashcard_queue.enQueue(again_flashcard) #utilises circular queue's wrapping around properties

                                flashcard_counter = 0
                                reviewed_list = []
                                question_review(review_flashcards_page, flashcard_counter, reviewed_list, peer_review_stack, text_frame, button_frame, flashcard_queue)

                            def finish_review(review_flashcards_page):
                                review_flashcards_page.destroy()
                                self.deck_list.bind("<Double-1>", self.deck_selected)

                            mycursor.execute("SELECT priority FROM user_flashcard INNER JOIN user_deck ON user_deck.deckID = user_flashcard.deckID INNER JOIN user_account ON user_account.accountID = user_deck.accountID WHERE user_deck.deckName = %s AND user_account.username = %s", (selected_deck, username_login))
                            result = mycursor.fetchall()
                            flashcards_number = len(result)
                            flashcards_sum = 0

                            for i in range (0, flashcards_number):
                                if result[i][0] == -1:
                                    flashcards_sum += 7 #weighed(?) priority for non-used cards
                                else:
                                    flashcards_sum += result[i][0]

                            score = round((10 - (flashcards_sum / flashcards_number)) * 10, 1) #make it so a flashcard has to have a certain number of "easy"s to immediately be considered 100%?  or mkae an "ease" value which increases/decreases with each "easy" - max 100 or smth, and then combine this to find a reliable priority in the queue - although above algorith already kinda solves this
                            score = max(0.0, min(100.0, score))
                            mycursor.execute("UPDATE user_deck INNER JOIN user_account ON user_account.accountID = user_deck.accountID SET user_deck.score = %s WHERE user_deck.deckName = %s AND user_account.username = %s", (score, selected_deck, username_login))
                            mydb.commit()
                            
                            grade_title = Label(text_frame, font=("Helvetica", 17), bg="#e6e7f0", text="Deck Score")
                            grade_title.pack()
                            score_title = Label(text_frame, font=("Helvetica", 20, "bold"), bg="#e6e7f0", text=f"{score}%")
                            score_title.pack()
                            again_button = Button(button_frame, **top_button, text="Review Again", command=lambda:review_again(review_flashcards_page, flashcard_counter, reviewed_list, text_frame, button_frame, flashcard_queue))
                            again_button.pack(side=LEFT)
                            finish_button = Button(button_frame, **top_button, text="Finish", command=lambda:finish_review(review_flashcards_page)) #finish button allows all data to be uploaded to mysql database. not really but still
                            finish_button.pack(side=LEFT)

                        def peer_review(review_flashcards_page, peer_counter, number_stacked, peer_review_stack, flashcard_counter, reviewed_list, text_frame, button_frame, flashcard_queue):
                            def check_peer(review_flashcards_page, peer_flashcard, peer_counter, number_stacked, flashcard_counter, reviewed_list, peer_review_stack, text_frame, button_frame, flashcard_queue):
                                selected_peer = "".join(peers_list.get(i) for i in peers_list.curselection())
                                if selected_peer:
                                    mycursor.execute("INSERT INTO user_peermarking (accountID, flashcardID, accountID2, useranswer) VALUES ((SELECT user_account.accountID FROM user_account WHERE user_account.username = %s), %s, (SELECT user_account.accountID FROM user_account WHERE user_account.username = %s), %s)", (username_login, peer_flashcard.id, selected_peer, peer_flashcard.input))
                                    mydb.commit()
                                    messagebox.showinfo("Marking Request Sent", f"Your marking request to {selected_peer} has been sent and is now pending a response.")
                                    peer_counter += 1
                                    peer_review(review_flashcards_page, peer_counter, number_stacked, peer_review_stack, flashcard_counter, reviewed_list, text_frame, button_frame, flashcard_queue)
                                else:
                                    messagebox.showerror("Invalid Friend", "No friend has been selected.")
                                    
                            if peer_counter < number_stacked:
                                for widget in text_frame.winfo_children():
                                    if not isinstance(widget, (Label, Scrollbar, Listbox)): #subroutine this
                                        continue
                                    widget.destroy()
                                for widget in button_frame.winfo_children():
                                    if not isinstance(widget, (Button)):
                                        continue
                                    widget.destroy()

                                peer_flashcard = peer_review_stack.pop()
                                peer_question = Label(text_frame, **supertitle_label, text=f"{peer_flashcard.question}", wraplength=500)
                                peer_question.pack()
                                peer_answer = Label(text_frame, **login_label, text=f"{peer_flashcard.answer}", wraplength=500)
                                peer_answer.pack()
                                peer_header = Label(text_frame, **notification_label, text="You wrote:")
                                peer_header.pack()
                                peer_output = Label(text_frame, **login_label, text=f"{peer_flashcard.input}", wraplength=450)
                                peer_output.pack()
                                peer_subheader = Label(text_frame, **notification_label, text="Select a friend to send your answer to:")
                                peer_subheader.pack()

                                peers = self.fetchmarkingfriend_info()
                                friend_scrollbar = Scrollbar(text_frame)
                                friend_scrollbar.pack(**vertical_scrollbar)
                                peers_list = Listbox(text_frame, **notification_label, **select_list, yscrollcommand=friend_scrollbar.set)
                                for peer in peers:
                                    peers_list.insert(END, peer[0])
                                peers_list.pack(**fill_widget)
                                friend_scrollbar.config(command=peers_list.yview)

                                send_button = Button(button_frame, **top_button, text="Send", command=lambda:check_peer(review_flashcards_page, peer_flashcard, peer_counter, number_stacked, flashcard_counter, reviewed_list, peer_review_stack, text_frame, button_frame, flashcard_queue))
                                send_button.pack(side=LEFT)
                            else:
                                for widget in text_frame.winfo_children():
                                    if not isinstance(widget, (Label, Scrollbar, Listbox)):
                                        continue
                                    widget.destroy()
                                for widget in button_frame.winfo_children():
                                    if not isinstance(widget, (Button)):
                                        continue
                                    widget.destroy()
                                review_show(review_flashcards_page, flashcard_counter, reviewed_list, text_frame, button_frame, flashcard_queue)

                        number_stacked = len(peer_review_stack.getStack())
                        if number_stacked > 0:
                            peer_counter = 0
                            peer_review(review_flashcards_page, peer_counter, number_stacked, peer_review_stack, flashcard_counter, reviewed_list, text_frame, button_frame, flashcard_queue)
                        else:
                            review_show(review_flashcards_page, flashcard_counter, reviewed_list, text_frame, button_frame, flashcard_queue)

                    for widget in text_frame.winfo_children():
                        if not isinstance(widget, (Label)):
                            continue
                        widget.destroy()
                    for widget in button_frame.winfo_children():
                        if not isinstance(widget, (Button)):
                            continue
                        widget.destroy()

                    flashcard_counter += 1
                    if flashcard_counter > 10:
                        end_review(review_flashcards_page, peer_review_stack, flashcard_counter, reviewed_list, text_frame, button_frame, flashcard_queue)
                    else:
                        new_flashcard = flashcard_queue.deQueue()
                        if new_flashcard is None:
                            end_review(review_flashcards_page, peer_review_stack, flashcard_counter, reviewed_list, text_frame, button_frame, flashcard_queue)
                        else:
                            print(flashcard_queue.getQueue())
                            question_header = Label(text_frame, **title_label, text=f"{new_flashcard.question}", wraplength=500)
                            question_header.pack()
                            input_text = Text(text_frame, width=50, height=9) #require input text
                            input_text.pack(fill=X)
                            flip_button = Button(button_frame, **top_button, text="Flip", command=lambda:answer_review(review_flashcards_page, new_flashcard, question_header, input_text, flip_button, flashcard_counter, reviewed_list, peer_review_stack, text_frame, button_frame, flashcard_queue))
                            flip_button.pack(**stretch_widget)
                
                self.deck_list.unbind("<Double-1>") #cannot open window while reviewing in case the user deletes deck -> causes sql error

                review_flashcards_page = Toplevel()
                review_flashcards_page.title(selected_deck)
                review_flashcards_page.resizable(False, False) #all flashcards put into queue, and organised depending on priority thanks to enQueue(). flashcard reviews are 10 at a time, and are dequeued one by one to get the next flashcard
                review_flashcards_page.protocol("WM_DELETE_WINDOW", self.do_pass)

                flashcards = self.fetch_flashcards()
                deck_size = len(flashcards)

                flashcard_queue = CircularPriorityQueue(deck_size)
                queue_flashcards(flashcards, flashcard_queue)
                peer_review_stack = Stack(deck_size)

                review_page = Frame(review_flashcards_page, bg="#e6e7f0")
                text_frame = Frame(review_page, bg="#e6e7f0")
                text_frame.pack(**stretch_widget)
                button_frame = Frame(review_page, bg="#d7d8e0")
                button_frame.pack(**stretch_widget)
                review_page.pack(**fill_widget)

                flashcard_counter = 0
                reviewed_list = []
                question_review(review_flashcards_page, flashcard_counter, reviewed_list, peer_review_stack, text_frame, button_frame, flashcard_queue)
            
            mycursor.execute("SELECT flashcardID FROM user_flashcard INNER JOIN user_deck ON user_deck.deckID = user_flashcard.deckID INNER JOIN user_account ON user_account.accountID = user_deck.accountID WHERE user_deck.deckName = %s AND user_account.username = %s", (selected_deck, username_login))
            if mycursor.fetchone():
                if "addflashcardPage" in globals():
                    addflashcardPage.destroy()
                self.deckPage.destroy()
                review_flashcards()
            else:
                messagebox.showerror("Empty Deck", "There are no flashcards in this deck.")

        def delete_deck():
            message_answer = messagebox.askokcancel("Delete Deck", f"Are you sure you want to delete {selected_deck}? All of the flashcards it contains will also be deleted.")
            if message_answer: #only 1 inner join able to be used in delete query
                mycursor.execute("DELETE user_peermarked FROM user_peermarked INNER JOIN user_flashcard ON user_flashcard.flashcardID = user_peermarked.flashcardID WHERE (user_flashcard.deckID = (SELECT user_deck.deckID FROM user_deck WHERE user_deck.deckName = %s AND user_deck.accountID = (SELECT user_account.accountID FROM user_account WHERE user_account.username = %s)))", (selected_deck, username_login))
                mydb.commit()
                mycursor.execute("DELETE user_peermarking FROM user_peermarking INNER JOIN user_flashcard ON user_flashcard.flashcardID = user_peermarking.flashcardID WHERE (user_flashcard.deckID = (SELECT user_deck.deckID FROM user_deck WHERE user_deck.deckName = %s AND user_deck.accountID = (SELECT user_account.accountID FROM user_account WHERE user_account.username = %s)))", (selected_deck, username_login))
                mydb.commit()
                mycursor.execute("DELETE user_flashcard FROM user_flashcard INNER JOIN user_deck ON user_deck.deckID = user_flashcard.deckID WHERE user_deck.deckName = %s AND user_deck.accountID = (SELECT user_account.accountID FROM user_account WHERE user_account.username = %s)", (selected_deck, username_login))
                mydb.commit()
                mycursor.execute("DELETE user_deck FROM user_deck INNER JOIN user_account ON user_account.accountID = user_deck.accountID WHERE user_deck.deckName = %s AND user_account.username = %s", (selected_deck, username_login))
                mydb.commit()
                self.deckPage.destroy()
                page1.show_dashboard() #refresh
            else:
                pass
            
        global selected_deck
        selected_deck = "".join(self.deck_list.get(i) for i in self.deck_list.curselection())

        self.deckPage = Toplevel()
        self.deckPage.title(selected_deck)
        self.deckPage.resizable(False, False)

        mycursor.execute("SELECT score FROM user_deck INNER JOIN user_account ON user_account.accountID = user_deck.accountID WHERE user_deck.deckName = %s AND user_account.username = %s", (selected_deck, username_login)) #make sure all sql string input are unique, as to not accidentally fetch someone else's deck
        deck_results = mycursor.fetchone()
        
        self.deck_page = Frame(self.deckPage, bg="#e6e7f0")

        self.header_buttons = Frame(self.deck_page, bg="#d7d8e0")
        self.addflashcard_button = Button(self.header_buttons, **top_button, text="Add Flashcard", command=add_flashcards)
        self.addflashcard_button.pack(side=LEFT)
        self.reviewdeck_button = Button(self.header_buttons, **top_button, text="Review", command=check_review)
        self.reviewdeck_button.pack(side=LEFT)
        self.deletedeck_button = Button(self.header_buttons, **top_button, text="Delete", command=delete_deck)
        self.deletedeck_button.pack(side=LEFT)
        self.header_buttons.pack(**stretch_widget)

        self.deck_frame = Frame(self.deck_page, bg="#e6e7f0")
        self.deckname_label = Label(self.deck_frame, **title_label, text=f"{selected_deck}")
        self.deckname_label.pack()
        self.deckscore_label = Label(self.deck_frame, **login_label, text=f"{deck_results[0]}%")
        self.deckscore_label.pack()
        self.deck_frame.pack(**stretch_widget)

        self.flashcardlist_frame = Frame(self.deck_page, bg="#e6e7f0")
        self.flashcardlist_frame.pack(**stretch_widget)
        
        self.deck_page.pack(**fill_widget)

        refresh_flashcards()

    def do_pass(self): #so that listbox is binded when "finish" button is pressed
        pass

    def fetch_account(self):
        mycursor.execute("SELECT username, firstName, lastName, friendRequest, markingRequest FROM user_account WHERE username=%s", (username_login,))
        return mycursor.fetchone()
    
    def fetch_decks(self):
        mycursor.execute("SELECT deckName FROM user_deck INNER JOIN user_account ON user_account.accountID = user_deck.accountID WHERE user_account.username = %s ORDER BY deckName ASC", (username_login,))
        return mycursor.fetchall()
    
    def fetch_flashcards(self):
        mycursor.execute("SELECT flashcardID, question, answer, priority FROM user_flashcard INNER JOIN user_deck ON user_deck.deckID = user_flashcard.deckID INNER JOIN user_account ON user_account.accountID = user_deck.accountID WHERE user_deck.deckName = %s AND user_account.username = %s", (selected_deck, username_login))
        return mycursor.fetchall()
    
    def fetch_friendinfo(self):
        mycursor.execute("SELECT ua2.username FROM user_account ua1 INNER JOIN user_friend ON user_friend.accountID = ua1.accountID INNER JOIN user_account ua2 ON ua2.accountID = user_friend.accountID2 WHERE ua1.username = %s", (username_login,))
        return mycursor.fetchall()
    
    def fetchmarkingfriend_info(self):
        mycursor.execute("SELECT ua2.username FROM user_account ua1 INNER JOIN user_friend ON user_friend.accountID = ua1.accountID INNER JOIN user_account ua2 ON ua2.accountID = user_friend.accountID2 WHERE ua1.username = %s AND ua2.markingRequest = 'on'", (username_login,))
        return mycursor.fetchall()
    
    def fetch_friendrequestinfo(self):
        mycursor.execute("SELECT ua1.username, ua1.firstName, ua1.lastName FROM user_account ua1 INNER JOIN user_friendrequest ON user_friendrequest.accountID = ua1.accountID INNER JOIN user_account ua2 ON ua2.accountID = user_friendrequest.accountID2 WHERE ua2.username = %s", (username_login,))
        return mycursor.fetchall()
    
    def show_dashboard(self): #show method used on each page to refresh info? update sql queries if doesn't work
        user_info = self.fetch_account()
        self.fullname.set(f"{user_info[1]} {user_info[2]} ({user_info[0]})")
        friendsnumber = len(self.fetch_friendrequestinfo())

        if friendsnumber == 0:
            self.friendsnumber.set("Friends")
        else:
            self.friendsnumber.set(f"Friends ({friendsnumber})")

        for widget in self.collection_page.winfo_children(): #cant use pack_forget coz used befor its declared iguess??#destroy destroys all DESCENDENT WIDGETS - simplify
            if not isinstance(widget, (Listbox, Scrollbar)):
                continue
            widget.destroy()

        decks = self.fetch_decks()
        self.scrollbar = Scrollbar(self.collection_page)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.deck_list = Listbox(self.collection_page, yscrollcommand=self.scrollbar.set, bg="#e6e7f0", font=("Helvetica", 12), relief=FLAT, selectmode=SINGLE, selectbackground="#bfc0c7")
        for deck in decks:
            self.deck_list.insert(END, deck[0])
        self.deck_list.pack(**fill_widget)
        self.deck_list.bind("<Double-1>", self.deck_selected)
        self.scrollbar.config(command=self.deck_list.yview)

        app.set_inboxnumber()
        page1.show()

class inboxPage(page):
    def __init__(self, *args, **kwargs):
        page.__init__(self, *args, **kwargs)

        self.inbox_page = Frame(self, bg="#e6e7f0")

        self.submissions_header = Frame(self.inbox_page, bg="#d7d8e0")
        self.submissions_label = Label(self.submissions_header, **header_label, text="Peer Marking Submissions")
        self.submissions_label.pack(side=LEFT)
        self.submissions_header.pack(**stretch_widget)

        self.peermarking_frame = Frame(self.inbox_page, bg="#e6e7f0")
        self.peermarking_frame.pack(**fill_widget)

        self.feedback_header = Frame(self.inbox_page, bg="#d7d8e0")
        self.feedback_label = Label(self.feedback_header, **header_label, text="Peer Marking Feedback")
        self.feedback_label.pack()
        self.feedback_header.pack(**stretch_widget)

        self.peermarked_frame = Frame(self.inbox_page, bg="#e6e7f0")
        self.peermarked_frame.pack(**fill_widget)

        self.inbox_page.pack(**fill_widget)

    def mark_flashcard(self, marking_flashcard, marking_username, marking_firstname, marking_question, inner_frame, marking_user, mark_button):
        def rating1_pressed():
            if self.rating1_button.cget("bg") == "#bfc0c7":
                self.rating1_button.config(**button_on)
                self.rating2_button.config(**button2_off)
                self.rating3_button.config(**button2_off)
                self.rating4_button.config(**button2_off)
            
        def rating2_pressed():
            if self.rating2_button.cget("bg") == "#bfc0c7":
                self.rating1_button.config(**button2_off)
                self.rating2_button.config(**button_on)
                self.rating3_button.config(**button2_off)
                self.rating4_button.config(**button2_off)

        def rating3_pressed():
            if self.rating3_button.cget("bg") == "#bfc0c7":
                self.rating1_button.config(**button2_off)
                self.rating2_button.config(**button2_off)
                self.rating3_button.config(**button_on)
                self.rating4_button.config(**button2_off)

        def rating4_pressed():
            if self.rating4_button.cget("bg") == "#bfc0c7":
                self.rating1_button.config(**button2_off)
                self.rating2_button.config(**button2_off)
                self.rating3_button.config(**button2_off)
                self.rating4_button.config(**button_on)

        def check_marking(flashcard_priority, marking_username, marking_flashcard, flashcard_useranswer, inner_frame, marking_user, mark_button):
            if self.rating1_button.cget("bg") == "#ffffff":
                peer_rating = "fail"
                if flashcard_priority == -1:
                    flashcard_newpriority = 9
                else:
                    flashcard_newpriority = flashcard_priority + 2
                update_priority(flashcard_newpriority, marking_flashcard)
                send_feedback(peer_rating, marking_username, marking_flashcard, flashcard_useranswer, inner_frame, marking_user, mark_button)

            elif self.rating2_button.cget("bg") == "#ffffff":
                peer_rating = "hard"
                if flashcard_priority == -1:
                    flashcard_newpriority = 7
                else:
                    flashcard_newpriority = flashcard_priority + 1
                update_priority(flashcard_newpriority, marking_flashcard)
                send_feedback(peer_rating, marking_username, marking_flashcard, flashcard_useranswer, inner_frame, marking_user, mark_button)

            elif self.rating3_button.cget("bg") == "#ffffff":
                peer_rating = "good"
                if flashcard_priority == -1:
                    flashcard_newpriority = 5
                else:
                    flashcard_newpriority = flashcard_priority - 1
                update_priority(flashcard_newpriority, marking_flashcard)
                send_feedback(peer_rating, marking_username, marking_flashcard, flashcard_useranswer, inner_frame, marking_user, mark_button)

            elif self.rating4_button.cget("bg") == "#ffffff":
                peer_rating = "easy"
                if flashcard_priority == -1:
                    flashcard_newpriority = 3
                else:
                    flashcard_newpriority = flashcard_priority - 2
                update_priority(flashcard_newpriority, marking_flashcard)
                send_feedback(peer_rating, marking_username, marking_flashcard, flashcard_useranswer, inner_frame, marking_user, mark_button)

            else:
                messagebox.showerror("Invalid Marking", "A rating has not been selected.")

        def update_priority(flashcard_newpriority, marking_flashcard):
            flashcard_newpriority = max(0, min(10, flashcard_newpriority))
            mycursor.execute("UPDATE user_flashcard SET priority = %s WHERE flashcardID = %s", (flashcard_newpriority, marking_flashcard))
            mydb.commit()

        def send_feedback(peer_rating, marking_username, marking_flashcard, flashcard_useranswer, inner_frame, marking_user, mark_button):
            peer_feedback = self.flashcard_feedback.get("1.0", "end-1c")
            mycursor.execute("INSERT INTO user_peermarked (accountID, flashcardID, accountID2, useranswer, rating, feedback) VALUES ((SELECT user_account.accountID FROM user_account WHERE user_account.username = %s), %s, (SELECT user_account.accountID FROM user_account WHERE user_account.username = %s), %s, %s, %s)", (username_login, marking_flashcard, marking_username, flashcard_useranswer, peer_rating, peer_feedback))
            mydb.commit()
            mycursor.execute("DELETE user_peermarking FROM user_peermarking INNER JOIN user_account ON user_account.accountID = user_peermarking.accountID WHERE user_account.username = %s AND user_peermarking.flashcardID = %s", (marking_username, marking_flashcard))
            mydb.commit()
            inner_frame.pack_forget()
            marking_user.pack_forget()
            mark_button.pack_forget()
            self.marking_page.destroy()

        self.marking_page = Toplevel()
        self.marking_page.title("Peer Marking")
        self.marking_page.resizable(False, False)

        flashcard_answer, flashcard_priority, flashcard_useranswer = self.fetch_peerflashcardinfo(username_login, marking_username, marking_flashcard)

        self.text_frame = Frame(self.marking_page, bg="#e6e7f0")
        self.question_label = Label(self.text_frame, **supertitle_label, text=f"{marking_question}", wraplength=500)
        self.question_label.pack()
        self.answer_label = Label(self.text_frame, **login_label, text=f"{flashcard_answer}", wraplength=500)
        self.answer_label.pack()

        self.label_header = Label(self.text_frame, **notification_label, text=f"{marking_firstname} wrote:")
        self.label_header.pack()
        self.useranswer_label = Label(self.text_frame, **login_label, text=f"{flashcard_useranswer}", wraplength=450)
        self.useranswer_label.pack()

        self.label_subheader = Label(self.text_frame, **notification_label, text="Provide optional additional feedback:")
        self.label_subheader.pack()
        self.flashcard_feedback = Text(self.text_frame, width=50, height=5) #add constraints for all
        self.flashcard_feedback.pack(fill=X)

        self.label_subheader2 = Label(self.text_frame, **notification_label, text="Select a rating:")
        self.label_subheader2.pack()
        self.text_frame.pack(**fill_widget)

        self.button_frame = Frame(self.marking_page, bg="#d7d8e0")
        self.rating1_button = Button(self.button_frame, **top_button, text="Fail", command=rating1_pressed)
        self.rating1_button.pack(side=LEFT)
        self.rating2_button = Button(self.button_frame, **top_button, text="Hard", command=rating2_pressed)
        self.rating2_button.pack(side=LEFT)
        self.rating3_button = Button(self.button_frame, **top_button, text="Good", command=rating3_pressed)
        self.rating3_button.pack(side=LEFT)
        self.rating4_button = Button(self.button_frame, **top_button, text="Easy", command=rating4_pressed)
        self.rating4_button.pack(side=LEFT)

        self.send_button = Button(self.button_frame, **top_button, text="Send", command=lambda:check_marking(flashcard_priority, marking_username, marking_flashcard, flashcard_useranswer, inner_frame, marking_user, mark_button))
        self.send_button.pack(side=RIGHT)
        self.button_frame.pack(**stretch_widget)

    def finish_peer(self, marked_flashcard, marked_username, inner_frame2, marked_user, marked_button, inner_frame3, marked_user2, inner_frame4, marked_user3):
        mycursor.execute("DELETE user_peermarked FROM user_peermarked INNER JOIN user_account ON user_account.accountID = user_peermarked.accountID WHERE user_account.username = %s AND user_peermarked.flashcardID = %s", (marked_username, marked_flashcard))
        mydb.commit()
        inner_frame2.pack_forget()
        marked_user.pack_forget()
        marked_button.pack_forget()
        inner_frame3.pack_forget()
        marked_user2.pack_forget()
        
        if inner_frame4:
            inner_frame4.pack_forget()
        else:
            pass

        if marked_user3:
            marked_user3.pack_forget()
        else:
            pass

    def fetch_peermarkinginfo(self):
        mycursor.execute("SELECT user_peermarking.flashcardID, ua2.username, ua2.firstName, ua2.lastName, user_flashcard.question FROM user_peermarking INNER JOIN user_account ua2 ON ua2.accountID = user_peermarking.accountID INNER JOIN user_account ua1 ON ua1.accountID = user_peermarking.accountID2 INNER JOIN user_flashcard ON user_flashcard.flashcardID = user_peermarking.flashcardID WHERE ua1.username = %s ORDER BY user_peermarking.accountID ASC", (username_login,))
        return mycursor.fetchall()
    
    def fetch_peermarkedinfo(self):
        mycursor.execute("SELECT user_peermarked.flashcardID, user_peermarked.useranswer, user_peermarked.rating, user_peermarked.feedback, ua2.username, ua2.firstName, ua2.lastName, user_flashcard.question FROM user_peermarked INNER JOIN user_account ua2 ON ua2.accountID = user_peermarked.accountID INNER JOIN user_account ua1 ON ua1.accountID = user_peermarked.accountID2 INNER JOIN user_flashcard ON user_flashcard.flashcardID = user_peermarked.flashcardID WHERE ua1.username = %s ORDER BY user_peermarked.accountID ASC", (username_login,))
        return mycursor.fetchall()

    def fetch_peerflashcardinfo(self, username_login, marking_username, marking_flashcard):
        mycursor.execute("SELECT user_flashcard.answer, user_flashcard.priority, user_peermarking.useranswer FROM user_peermarking INNER JOIN user_account ua2 ON ua2.accountID = user_peermarking.accountID INNER JOIN user_account ua1 ON ua1.accountID = user_peermarking.accountID2 INNER JOIN user_flashcard ON user_flashcard.flashcardID = user_peermarking.flashcardID WHERE ua1.username = %s AND ua2.username = %s AND user_peermarking.flashcardID = %s", (username_login, marking_username, marking_flashcard))
        return mycursor.fetchone()

    def show_dashboard(self):
        self.peermarking_info = self.fetch_peermarkinginfo()
        self.peermarked_info = self.fetch_peermarkedinfo()

        for widget in self.peermarking_frame.winfo_children():
            if not isinstance(widget, (Frame)):
                continue
            widget.destroy()

        if not self.peermarking_info:
            pass
        else:
            for peermarking in self.peermarking_info:
                marking_flashcard, marking_username, marking_firstname, marking_lastname, marking_question = peermarking

                inner_frame = Frame(self.peermarking_frame, bg="#e6e7f0")
                marking_user = Label(inner_frame, **notification_label, text=f"{marking_firstname} {marking_lastname} ({marking_username}) has sent you a peer marking submission: '{marking_question}'.", wraplength=700)
                marking_user.pack(side=LEFT)
                mark_button = Button(inner_frame, font=("Helvetica", 9), text="Mark")
                mark_button.pack(side=LEFT)
                inner_frame.pack(**fill_widget)

                mark_button.config(command=lambda marking_flashcard=marking_flashcard, marking_username=marking_username, marking_firstname=marking_firstname, marking_question=marking_question, inner_frame=inner_frame, marking_user=marking_user, mark_button=mark_button: self.mark_flashcard(marking_flashcard, marking_username, marking_firstname, marking_question, inner_frame, marking_user, mark_button))

        for widget in self.peermarked_frame.winfo_children():
            if not isinstance(widget, (Frame)):
                continue
            widget.destroy()

        if not self.peermarked_info:
            pass
        else:
            for peermarked in self.peermarked_info:
                marked_flashcard, marked_useranswer, marked_rating, marked_feedback, marked_username, marked_firstname, marked_lastname, marked_question = peermarked

                inner_frame2 = Frame(self.peermarked_frame, bg="#e6e7f0")
                marked_user = Label(inner_frame2, **notification_label, text=f"{marked_firstname} {marked_lastname} ({marked_username}) marked your flashcard '{marked_question}' with a {marked_rating.capitalize()} rating.", wraplength=700)
                marked_user.pack(side=LEFT)
                marked_button = Button(inner_frame2, font=("Helvetica", 9), text="Done")
                marked_button.pack(side=LEFT)
                inner_frame2.pack(**fill_widget)

                inner_frame3 = Frame(self.peermarked_frame, bg="#e6e7f0")
                marked_user2 = Label(inner_frame3, **notification_label, text=f"'{marked_useranswer}'", wraplength=700)
                marked_user2.pack(side=LEFT)
                inner_frame3.pack(**fill_widget)

                inner_frame4 = None
                marked_user3 = None

                if marked_feedback:
                    inner_frame4 = Frame(self.peermarked_frame, bg="#e6e7f0")
                    marked_user3 = Label(inner_frame4, **notification_label, text=f"Feedback: '{marked_feedback}'", wraplength=700)
                    marked_user3.pack(side=LEFT)
                    inner_frame4.pack(**fill_widget)
                else:
                    pass

                marked_button.config(command=lambda marked_flashcard=marked_flashcard, marked_username=marked_username, inner_frame2=inner_frame2, marked_user=marked_user, marked_button=marked_button, inner_frame3=inner_frame3, marked_user2=marked_user2, inner_frame4=inner_frame4, marked_user3 = marked_user3: self.finish_peer(marked_flashcard, marked_username, inner_frame2, marked_user, marked_button, inner_frame3, marked_user2, inner_frame4, marked_user3))

        app.set_inboxnumber()
        page2.show()

class footer(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        global page0
        global page00
        global page1
        global page2
        page0 = loginPage(self)
        page00 = signupPage(self)
        page1 = collectionPage(self)
        page2 = inboxPage(self)

        self.inboxnumber = StringVar()

        page0.grid(row=0, column=0, sticky="nsew")
        page00.grid(row=0, column=0, sticky="nsew")
        page1.grid(row=0, column=0, sticky="nsew")
        page2.grid(row=0, column=0, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        page0.show()

    def fetch_peermarkingnumber(self):
        mycursor.execute("SELECT * FROM user_peermarking INNER JOIN user_account ua2 ON ua2.accountID = user_peermarking.accountID INNER JOIN user_account ua1 ON ua1.accountID = user_peermarking.accountID2 WHERE ua1.username = %s", (username_login,))
        return mycursor.fetchall()
    
    def fetch_peermarkednumber(self):
        mycursor.execute("SELECT * FROM user_peermarked INNER JOIN user_account ua2 ON ua2.accountID = user_peermarked.accountID INNER JOIN user_account ua1 ON ua1.accountID = user_peermarked.accountID2 WHERE ua1.username = %s", (username_login,))
        return mycursor.fetchall()
    
    def set_inboxnumber(self):
        inboxnumber = len(self.fetch_peermarkingnumber()) + len(self.fetch_peermarkednumber())
        if inboxnumber == 0:
            self.inboxnumber.set("Inbox")
        else:
            self.inboxnumber.set(f"Inbox ({inboxnumber})")

    def showButtons(self):
        self.set_inboxnumber()

        self.bottom_buttons = Frame(self, bg="#d7d8e0")
        self.collection_button = Button(self.bottom_buttons, font=("Helvetica", 12), text="Collection", command=lambda:page1.show_dashboard())
        self.collection_button.pack(side=LEFT)
        self.search_button = Button(self.bottom_buttons, font=("Helvetica", 12), textvariable=self.inboxnumber, command=lambda:page2.show_dashboard())
        self.search_button.pack(side=LEFT)
        self.bottom_buttons.grid(row=1, column=0, sticky="nsew")

app = footer(window)
app.pack(**footer_widget)
window.mainloop()#GET RID OF ALL NESTED FUNCTIONS and add .self to everything #add more aggregate sql functions and order by#add parent=self for messagebox