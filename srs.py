from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import hashlib

mydb = mysql.connector.connect(host="localhost", user="sqluser", password="password", database="srs_data")
mycursor = mydb.cursor()

window = Tk()
window.title("Spaced Repetition Flashcard Software")
#window.iconbitmap("librarypc.ico")
window['bg']="#e6e7f0"
window.resizable(False, False)

class page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

user1 = StringVar(window,"user_friend") #replace
user2 = StringVar(window,"user_friend_2") #replace
user3 = StringVar(window,"user_friend_3") #replace

feedscrollbar = Scrollbar(window)
feedscrollbar.pack(side=RIGHT, fill=X)

def inboxWindow():
    inboxTab = Toplevel()
    inboxTab.title("Inbox (1)")
    inboxTab.resizable(False, False)
    inboxscrollbar = Scrollbar(inboxTab)
    inboxscrollbar.pack(side=RIGHT, fill=Y)
    inboxTitle = Label(
        inboxTab,
        text="Inbox",
        anchor=CENTER,
        bg="#bfc0c7",
        font=("Helvetica", 10, "bold"),
        relief=RIDGE
        )
    inboxTitle.pack(fill=X)
    inboxTopfiller = Label(
        inboxTab,
        text=" ",
        bg="#aeafb5",
        font=("Helvetica", 1)
        )
    inboxTopfiller.pack(side=TOP, fill=X)
    inboxNotification1 = Frame(inboxTab, bg="#d7d8e0")
    inboxIcon1 = Label(
        inboxNotification1,
        bitmap="warning",
        bg="#d7d8e0"
        )
    inboxIcon1.pack(side=LEFT)
    inboxName1 = Label(
        inboxNotification1,
        text="New marking request",
        font=("Helvetica", 9, "bold"),
        bg="#d7d8e0"
        )
    inboxName1.pack(side=LEFT)
    inboxNotification1.pack(side=TOP, fill=X)
    inboxContent1 = Frame(inboxTab, bg="#e6e7f0")
    inboxContentname1 = Label(
        inboxContent1,
        textvariable=user1,
        font=("Helvetica",8,"bold"),
        bg="#e6e7f0"
        )
    inboxContentname1.pack(side=LEFT)
    inboxContentinfo1 = Label(
        inboxContent1,
        text="sent you 5 marking requests.",
        font=("Helvetica", 8),
        bg="#e6e7f0"
        )
    inboxContentinfo1.pack(side=LEFT)
    inboxContent1.pack(side=TOP, fill=X)
    inboxButtons1 = Frame(inboxTab, bg="#e6e7f0")
    inboxButtonview1 = Button(
        inboxButtons1,
        text="View flashcards",
        font=("Helvetica", 7),
        bg="#d7d8e0"
        )
    inboxButtonview1.pack(side=LEFT)
    inboxButtonaccept1 = Button(
        inboxButtons1,
        text="Accept",
        font=("Helvetica", 7),
        bg="#d7d8e0"
        )
    inboxButtonaccept1.pack(side=LEFT)
    inboxButtondeny1 = Button(
        inboxButtons1,
        text="Deny",
        font=("Helvetica", 7),
        bg="#d7d8e0"
        )
    inboxButtondeny1.pack(side=LEFT)
    inboxDate1 = Label(
        inboxButtons1,
        text="36 minutes ago",
        font=("Helvetica", 7),
        bg="#e6e7f0"
        )
    inboxDate1.pack(side=LEFT)
    inboxButtons1.pack(side=TOP, fill=X)
    inboxMidfiller1 = Label(
        inboxTab,
        text=" ",
        font=("Helvetica", 1),
        bg="#aeafb5"
        )
    inboxMidfiller1.pack(side=TOP, fill=X)
    inboxNotification2 = Frame(inboxTab, bg="#e6e7f0")
    inboxName2 = Label(
        inboxNotification2,
        text="Marking feedback",
        font=("Helvetica", 9),
        bg="#e6e7f0"
        )
    inboxName2.pack(side=LEFT)
    inboxNotification2.pack(side=TOP, fill=X)
    inboxContent2 = Frame(inboxTab)
    inboxContentname2 = Label(
        inboxContent2,
        textvariable=user2,
        font=("Helvetica",8,"bold"),
        )
    inboxContentname2.pack(side=LEFT)
    inboxContentinfo2 = Label(
        inboxContent2,
        text="has reviewed your 5 flashcard answers.",
        font=("Helvetica", 8),
        )
    inboxContentinfo2.pack(side=LEFT)
    inboxContent2.pack(side=TOP, fill=X)
    inboxButtons2 = Frame(inboxTab)
    inboxButtonview2 = Button(
        inboxButtons2,
        text="View feedback",
        font=("Helvetica", 7),
        bg="#e6e7f0"
        )
    inboxButtonview2.pack(side=LEFT)
    inboxDate2 = Label(
        inboxButtons2,
        text="5 days ago",
        font=("Helvetica", 7),
        )
    inboxDate2.pack(side=LEFT)
    inboxButtons2.pack(side=TOP, fill=X)
    inboxMidfiller2 = Label(
        inboxTab,
        text=" ",
        font=("Helvetica", 1),
        bg="#aeafb5"
        )
    inboxMidfiller2.pack(side=TOP, fill=X)
    inboxNotification3 = Frame(inboxTab, bg="#e6e7f0")
    inboxName3 = Label(
        inboxNotification3,
        text="Marking request denied",
        font=("Helvetica", 9),
        bg="#e6e7f0"
        )
    inboxName3.pack(side=LEFT)
    inboxNotification3.pack(side=TOP, fill=X)
    inboxContent3 = Frame(inboxTab)
    inboxContentname3 = Label(
        inboxContent3,
        textvariable=user3,
        font=("Helvetica",8,"bold"),
        )
    inboxContentname3.pack(side=LEFT)
    inboxContentinfo3 = Label(
        inboxContent3,
        text="denied your 3 marking requests.",
        font=("Helvetica", 8),
        )
    inboxContentinfo3.pack(side=LEFT)
    inboxContent3.pack(side=TOP, fill=X)
    inboxButtons3 = Frame(inboxTab)
    inboxButtonview3 = Button(
        inboxButtons3,
        text="Send requests to another user",
        font=("Helvetica", 7),
        bg="#e6e7f0"
        )
    inboxButtonview3.pack(side=LEFT)
    inboxDate3 = Label(
        inboxButtons3,
        text="24/10/23",
        font=("Helvetica", 7),
        )
    inboxDate3.pack(side=LEFT)
    inboxButtons3.pack(side=TOP, fill=X) #inbox window

def settingsWindow():
    global settingsButtonon1
    global settingsButtonmutual1
    global settingsButtonoff1
    global settingsButtonon2
    global settingsButtonoff2
    settingsTab = Toplevel()
    settingsTab.title("Settings")
    settingsTab.resizable(False, False)
    settingsTitle = Label(
        settingsTab,
        text="Settings",
        anchor=CENTER,
        bg="#bfc0c7",
        font=("Helvetica", 10, "bold"),
        relief=RIDGE
        )
    settingsTitle.pack(fill=X)
    settingsTopfiller = Label(
        settingsTab,
        text=" ",
        bg="#aeafb5",
        font=("Helvetica", 1)
        )
    settingsTopfiller.pack(side=TOP, fill=X)
    settingsSection1 = Frame(settingsTab, bg="#d7d8e0")
    settingsHeader1 = Label(
        settingsSection1,
        text="Friend requests",
        font=("Helvetica", 11, "bold"),
        bg="#d7d8e0"
        )
    settingsHeader1.pack(side=LEFT)
    settingsSection1.pack(side=TOP, fill=X)
    settingsButtons1 = Frame(settingsTab, bg="#e6e7f0", pady=6)
    settingsButtonon1 = Button(
        settingsButtons1,
        text="On",
        font=("Helvetica", 9),
        bg="#d7d8e0",
        command=friendOnPressed
        )
    settingsButtonon1.pack(side=LEFT)
    settingsButtonmutual1 = Button(
        settingsButtons1,
        text="Mutual friends only",
        font=("Helvetica", 9),
        bg="#d7d8e0",
        command=friendMutualPressed
        )
    settingsButtonmutual1.pack(side=LEFT)
    settingsButtonoff1 = Button(
        settingsButtons1,
        text="Off",
        font=("Helvetica", 9),
        bg="#d7d8e0",
        command=friendOffPressed
        )
    settingsButtonoff1.pack(side=LEFT)
    settingsButtons1.pack(side=TOP, fill=X)

    mycursor.execute("SELECT friendRequest FROM user_account WHERE username = %s", (usernameLogin,))
    friendResult = mycursor.fetchone()
    if friendResult == ('on',):
        settingsButtonon1.config(bg="#ffffff", relief=SUNKEN)
    elif friendResult == ('mutual',):
        settingsButtonmutual1.config(bg="#ffffff", relief=SUNKEN)
    elif friendResult == ('off',):
        settingsButtonoff1.config(bg="#ffffff", relief=SUNKEN)

    settingsSection2 = Frame(settingsTab, bg="#d7d8e0")
    settingsHeader2 = Label(
        settingsSection2,
        text="Marking requests",
        font=("Helvetica", 11, "bold"),
        bg="#d7d8e0"
        )
    settingsHeader2.pack(side=LEFT)
    settingsSection2.pack(side=TOP, fill=X)
    settingsButtons2 = Frame(settingsTab, bg="#e6e7f0", pady=6)
    settingsButtonon2 = Button(
        settingsButtons2,
        text="On",
        font=("Helvetica", 9),
        bg="#d7d8e0",
        command=markingOnPressed
        )
    settingsButtonon2.pack(side=LEFT)
    settingsButtonoff2 = Button(
        settingsButtons2,
        text="Off",
        font=("Helvetica", 9),
        bg="#d7d8e0",
        command=markingOffPressed
        )
    settingsButtonoff2.pack(side=LEFT)
    settingsButtons2.pack(side=TOP, fill=X)

    mycursor.execute("SELECT markingRequest FROM user_account WHERE username = %s", (usernameLogin,))
    markingResult = mycursor.fetchone()
    if markingResult == ('on',):
        settingsButtonon2.config(bg="#ffffff", relief=SUNKEN)
    elif markingResult == ('off',):
        settingsButtonoff2.config(bg="#ffffff", relief=SUNKEN)

def friendOnPressed():
    if settingsButtonon1.cget("bg") == "#d7d8e0":
        settingsButtonon1.config(bg="#ffffff", relief=SUNKEN)
        settingsButtonmutual1.config(bg="#d7d8e0", relief=RAISED)
        settingsButtonoff1.config(bg="#d7d8e0", relief=RAISED)
        mycursor.execute("UPDATE user_account SET friendRequest = 'on' WHERE username = %s", (usernameLogin,))
        mydb.commit()

def friendMutualPressed():
    if settingsButtonmutual1.cget("bg") == "#d7d8e0":
        settingsButtonon1.config(bg="#d7d8e0", relief=RAISED)
        settingsButtonmutual1.config(bg="#ffffff", relief=SUNKEN)
        settingsButtonoff1.config(bg="#d7d8e0", relief=RAISED)
        mycursor.execute("UPDATE user_account SET friendRequest = 'mutual' WHERE username = %s", (usernameLogin,))
        mydb.commit()

def friendOffPressed():
    if settingsButtonoff1.cget("bg") == "#d7d8e0":
        settingsButtonon1.config(bg="#d7d8e0", relief=RAISED)
        settingsButtonmutual1.config(bg="#d7d8e0", relief=RAISED)
        settingsButtonoff1.config(bg="#ffffff", relief=SUNKEN)
        mycursor.execute("UPDATE user_account SET friendRequest = 'off' WHERE username = %s", (usernameLogin,))
        mydb.commit()

def markingOnPressed():
    if settingsButtonon2.cget("bg") == "#d7d8e0":
        settingsButtonon2.config(bg="#ffffff", relief=SUNKEN)
        settingsButtonoff2.config(bg="#d7d8e0", relief=RAISED)
        mycursor.execute("UPDATE user_account SET markingRequest = 'on' WHERE username = %s", (usernameLogin,))
        mydb.commit()

def markingOffPressed():
    if settingsButtonoff2.cget("bg") == "#d7d8e0":
        settingsButtonon2.config(bg="#d7d8e0", relief=RAISED)
        settingsButtonoff2.config(bg="#ffffff", relief=SUNKEN)
        mycursor.execute("UPDATE user_account SET markingRequest = 'off' WHERE username = %s", (usernameLogin,))
        mydb.commit()

def deckWindow():
    global deckEntry1
    global deckEntry2
    deckTab = Toplevel()
    deckTab.title("Create Deck")
    deckTab.resizable(False, False)
    deckSection1 = Frame(deckTab, bg="#d7d8e0")
    deckOption1 = Label(
        deckSection1,
        text="Deck name",
        font=("Helvetica", 11, "bold"),
        bg="#d7d8e0"
        )
    deckOption1.pack(side=LEFT)
    deckSection1.pack(side=TOP, fill=X)
    deckEnter1 = Frame(deckTab, bg="#e6e7f0")
    deckEntry1 = Entry(deckEnter1)
    deckEntry1.pack(side=LEFT)
    deckEnter1.pack(side=TOP, fill=X)
    deckSection2 = Frame(deckTab, bg="#d7d8e0")
    deckOption2 = Label(
        deckSection2,
        text="Privacy setting",
        font=("Helvetica", 11, "bold"),
        bg="#d7d8e0"
        )
    deckOption2.pack(side=LEFT)
    deckSection2.pack(side=TOP, fill=X)
    deckEnter2 = Frame(deckTab, bg="#e6e7f0")
    deckEntry2 = ttk.Combobox(
        deckEnter2, 
        state="readonly", 
        values=["Public", "Friends only", "Private"]
        )
    deckEntry2.set("Public")
    deckEntry2.pack(side=LEFT)
    deckEnter2.pack(side=TOP, fill=X)
    deckCreateButton = Button(
        deckTab,
        text="Create deck",
        font=("Helvetica", 9),
        bg="#d7d8e0",
        command=createDeck
        )
    deckCreateButton.pack(side=TOP, fill=X)

def createDeck():
    mycursor.execute("SELECT accountID FROM user_account WHERE username = %s", (usernameLogin,))
    accountId = (mycursor.fetchone())[0]
    print(accountId)
    deckName = deckEntry1.get()
    print(deckName)
    deckSetting = deckEntry2.get()
    print(deckSetting)
    if deckSetting == "Public":
        deckPrivacy = "public"
    elif deckSetting == "Friends only":
        deckPrivacy = "friends"
    elif deckSetting == "Private":
        deckPrivacy = "private"
    mycursor.execute("INSERT INTO user_deck (accountID, deckName, privacy) VALUES (%s, %s, %s)", (accountId, deckName, deckPrivacy))
    mydb.commit()
        
class loginPage(page):
    def __init__(self, *args, **kwargs):
        page.__init__(self, *args, **kwargs)
        global usernameEntry
        global passwordEntry
        login = Frame(self)
        frontTitle = Label(
            login, 
            text="Spaced Repetition Software"
            )
        frontTitle.pack()
        usernameLabel = Label(
            login,
            text="Username"
            )
        usernameLabel.pack()
        usernameEntry = Entry(login)
        usernameEntry.pack()
        passwordLabel = Label(
            login,
            text="Password"
            )
        passwordLabel.pack()
        passwordEntry = Entry(login, show="*")
        passwordEntry.pack()
        loginButton = Button(
            login,
            text="Log in", 
            command=self.login
            )
        loginButton.pack()
        signupButton = Button(
            login, 
            text="Sign up", 
            command=self.showSignupPage
            )
        signupButton.pack()
        login.pack(fill=BOTH, expand=True)
    def login(self):
        global usernameLogin
        usernameLogin = usernameEntry.get()
        passwordLogin = passwordEntry.get()
        hashLogin = self.hashingLogin(passwordLogin)
        mycursor.execute("SELECT * FROM user_account WHERE username = %s AND password = %s", (usernameLogin, hashLogin))
        userResult = mycursor.fetchone()
        if userResult:
            app.showButtons()
            page1.showDashboard(usernameLogin)
        else:
            messagebox.showerror("Invalid Login", "Username or password is incorrect.")
    def hashingLogin(self, passwordLogin):
        return (hashlib.sha256(passwordLogin.encode("utf-8"))).hexdigest()
    def showSignupPage(self):
        page00.show()

class signupPage(page):
    def __init__(self, *args, **kwargs):
        page.__init__(self, *args, **kwargs)
        global signup
        global newFirstnameEntry
        global newLastnameEntry
        global newUsernameEntry
        global newPasswordEntry
        global confirmPasswordEntry 
        global newRankDropdown
        global newRankLabel
        global makeAccountButton
        global loginBackButton 
        signup = Frame(self)
        newFirstnameLabel = Label(
            signup, 
            text="First name"
            )
        newFirstnameLabel.pack()
        newFirstnameEntry = Entry(signup)
        newFirstnameEntry.pack()
        newLastnameLabel = Label(
            signup, 
            text="Last name"
            )
        newLastnameLabel.pack()
        newLastnameEntry = Entry(signup)
        newLastnameEntry.pack()
        newUsernameLabel = Label(
            signup, 
            text="Username"
            )
        newUsernameLabel.pack()
        newUsernameEntry = Entry(signup)
        newUsernameEntry.pack()
        newPasswordLabel = Label(
            signup, 
            text="Password"
            )
        newPasswordLabel.pack()
        newPasswordEntry = Entry(signup, show="*")
        newPasswordEntry.pack()
        confirmPasswordLabel = Label(
            signup,
            text="Confirm password"
            )
        confirmPasswordLabel.pack()
        confirmPasswordEntry = Entry(signup, show="*")
        confirmPasswordEntry.pack()
        newRankLabel = Label(
            signup, 
            text="Reason for using this software?"
            )
        newRankLabel.pack()
        newRankDropdown = ttk.Combobox(
            signup, 
            state="readonly", 
            values=["I'm a student", "I'm a teacher", "Other/Casual use"]
            )
        newRankDropdown.set("Other/Casual use")
        newRankDropdown.pack()
        makeAccountButton = Button(
            signup, 
            text="Sign up", 
            command=self.registerUser
            )
        makeAccountButton.pack()
        loginBackButton = Button(
            signup, 
            text="Back", 
            command=self.showLoginPage
            )
        loginBackButton.pack()
        signup.pack(fill=BOTH, expand=True)
    def registerUser(self):
        global newUsername
        global newRank
        global newFirstnameCap
        global newLastnameCap
        global hashPassword
        newFirstname = newFirstnameEntry.get()
        if self.validateName(newFirstname) == 1: #GET RID OF ALL OF THIS
            messagebox.showerror("Invalid First Name", "First name must contain only letters.")
        elif self.validateName(newFirstname) == 2:
            messagebox.showerror("Invalid First Name", "First name must be between 1 and 20 characters in length.")
        else:
            newFirstnameCap = (newFirstname.lower()).capitalize()
            newLastname = newLastnameEntry.get()
            if self.validateName(newLastname) == 1:
                messagebox.showerror("Invalid Last Name", "Last name must contain only letters.")
            elif self.validateName(newLastname) == 2:
                messagebox.showerror("Invalid Last Name", "Last name must be between 1 and 20 characters in length.")
            else:
                newLastnameCap = (newLastname.lower()).capitalize()
                newUsername = newUsernameEntry.get()
                if self.validateUsername(newUsername) == 1:
                    messagebox.showerror("Invalid Username", "Username can only contain letters, numbers and “_” or “-” symbols.")
                elif self.validateUsername(newUsername) == 2:
                    messagebox.showerror("Invalid Username", "Username must be between 1 and 20 characters in length.")
                elif self.validateUsername(newUsername) == 3:
                    messagebox.showerror("Invalid Username", "Username already registered.")
                else:
                    newPassword = newPasswordEntry.get()
                    if self.validatePassword(newPassword) == 1:
                        messagebox.showerror("Invalid Password", "Password must contain both letters and numbers.")
                    elif self.validatePassword(newPassword) == 2:
                        messagebox.showerror("Invalid Password", "Password must be between 8 and 100 characters in length.")
                    else:
                        hashPassword = self.hashingPassword(newPassword)
                        confirmPassword = confirmPasswordEntry.get()
                        if newPassword != confirmPassword:
                            messagebox.showerror("Invalid Password", "Passwords do not match.")
                        else:
                            newRank = newRankDropdown.get()
                            if newRank == "I'm a student" or newRank == "I'm a teacher": #changing to im a student but then changing back to casual after clicking sign up??
                                global newCentreEntry
                                newRankLabel.pack_forget()
                                newRankDropdown.pack_forget()
                                makeAccountButton.pack_forget()
                                loginBackButton.pack_forget()
                                newCentreLabel = Label(signup, text="What is your school/tuition centre?")
                                newCentreLabel.pack()
                                newCentreEntry = Entry(signup)
                                newCentreEntry.pack()
                                makeEduAccountButton = Button(signup, text="Sign up", command=self.registerEduUser)
                                makeEduAccountButton.pack()
                            else: 
                                userNewRank = "regular"
                                mycursor.execute("INSERT INTO user_account (username, firstName, lastName, password, userRank) VALUES (%s, %s, %s, %s, %s)", (newUsername, newFirstnameCap, newLastnameCap, hashPassword, userNewRank))
                                mydb.commit()
                                self.showDetails()
    def registerEduUser(self):
        if newRank == "I'm a student":
            userNewRank = "student"
        elif newRank == "I'm a teacher":
            userNewRank = "teacher"
        newCentre = newCentreEntry.get()
        if self.validateCentre(newCentre):
            messagebox.showerror("Invalid Centre", "Centre must be between 1 and 100 characters in length.")
        else:
            mycursor.execute("INSERT INTO user_account (username, firstName, lastName, password, userRank, centre) VALUES (%s, %s, %s, %s, %s, %s)", (newUsername, newFirstnameCap, newLastnameCap, hashPassword, userNewRank, newCentre))
            mydb.commit()
            self.showDetails()
    def validateName(self, newName):
        if not newName.isalpha():
            return 1
        elif len(newName) > 30 or len(newName) < 1:
            return 2
    def validateUsername(self, newUsername):
        if not all(char.isalnum() or char in ["_", "-"] for char in newUsername):
            return 1
        elif len(newUsername) > 20 or len(newUsername) < 1:
            return 2
        else:
            mycursor.execute("SELECT * FROM user_account WHERE username = %s", (newUsername,)) #case sensitive
            if mycursor.fetchone():
                return 3
    def validatePassword(self, newPassword):
        if not (any(char.isalpha() for char in newPassword) and any(char.isdigit() for char in newPassword)):
            return 1
        elif len(newPassword) > 100 or len(newPassword) < 8:
            return 2
    def hashingPassword(self, newPassword):
        return (hashlib.sha256(newPassword.encode("utf-8"))).hexdigest()
    def validateCentre(self, newCentre):
        if len(newCentre) > 100 or len(newCentre) < 1:
            return True
    def showDetails(self):
        self.showLoginPage()
        messagebox.showinfo("Account Creation", f"Welcome {newUsername}!\nPlease log in with your new account.")
    def showLoginPage(self):
        page0.show()

class feedPage(page):
    def __init__(self, *args, **kwargs):
        page.__init__(self, *args, **kwargs)
        self.feed = Frame(self)
        self.profileUsername = StringVar()
        self.profileUsername.set("placeholder")

        self.topButtons = Frame(self.feed, bg="#d7d8e0") #top buttons
        self.usernameLabel = Label(
            self.topButtons,
            textvariable=self.profileUsername,
            bg="#bfc0c7", 
            font=("Helvetica",9),
            pady=4
            )
        self.usernameLabel.pack(side=LEFT)
        self.inboxButton = Button(
            self.topButtons, 
            text="Inbox (1)", 
            bg="#bfc0c7", 
            font=("Helvetica",9),
            command=inboxWindow
            )
        self.inboxButton.pack(side=LEFT)
        self.settingsButton = Button(
            self.topButtons,
            text="Settings",
            bg="#bfc0c7",
            font=("Helvetica", 9),
            command=settingsWindow
            )
        self.settingsButton.pack(side=LEFT)
        self.topButtons.pack(side=TOP, fill=X)

        self.topFiller = Label(
            self.feed,
            bg="#e6e7f0",
            font=("Helvetica", 8),
            height=1,
            ) #1st filler
        self.topFiller.pack(side=TOP, fill=X)

        self.feedUsername1 = Frame(self.feed, bg="#d7d8e0") #1st update
        self.feedName1 = Button(
            self.feedUsername1,
            textvariable=user1,
            bg="#e6e7f0",
            font=("Helvetica",10)
            )
        self.feedName1.pack(side=LEFT)
        self.feedUsername1.pack(side=TOP, fill=X)

        self.feedContent1 = Frame(self.feed, bg="#e6e7f0")
        self.feedContentname1 = Label(
            self.feedContent1,
            textvariable=user1,
            font=("Helvetica",10,"bold"),
            bg="#e6e7f0"
            )
        self.feedContentname1.pack(side=LEFT)
        self.feedTime1 = Label(
            self.feedContent1,
            text="made a new deck 2 minutes ago.",
            font=("Helvetica", 10),
            bg="#e6e7f0"
            )
        self.feedTime1.pack(side=LEFT)
        self.feedContent1.pack(side=TOP, fill=X)

        self.feedDeck1 = Frame(self.feed, bg="#e6e7f0")
        self.feedDeckname1 = Label(
            self.feedDeck1,
            text="Computer Science Databases",
            font=("Helvetica", 15),
            bg="#e6e7f0"
            )
        self.feedDeckname1.pack(side=LEFT)
        self.feedViewbutton1 = Button(
            self.feedDeck1,
            text="View deck",
            font=("Helvetica", 8),
            )
        self.feedViewbutton1.pack(side=LEFT)
        self.feedDeck1.pack(side=TOP, fill=X)

        self.feedUsername2 = Frame(self.feed, bg="#d7d8e0") #2nd notif
        self.feedName2 = Button(
            self.feedUsername2,
            textvariable=user2,
            bg="#e6e7f0",
            font=("Helvetica",10)
            )
        self.feedName2.pack(side=LEFT)
        self.feedUsername2.pack(side=TOP, fill=X)

        self.feedContent2 = Frame(self.feed, bg="#e6e7f0")
        self.feedContentname2 = Label(
            self.feedContent2,
            textvariable=user2,
            font=("Helvetica",10,"bold"),
            bg="#e6e7f0"
            )
        self.feedContentname2.pack(side=LEFT)
        self.feedTime2 = Label(
            self.feedContent2,
            text="made a new deck 1 hour ago.",
            font=("Helvetica", 10),
            bg="#e6e7f0"
            )
        self.feedTime2.pack(side=LEFT)
        self.feedContent2.pack(side=TOP, fill=X)

        self.feedDeck2 = Frame(self.feed, bg="#e6e7f0")
        self.feedDeckname2 = Label(
            self.feedDeck2,
            text="Biology Skeletal Muscle",
            font=("Helvetica", 15),
            bg="#e6e7f0"
            )
        self.feedDeckname2.pack(side=LEFT)
        self.feedViewbutton2 = Button(
            self.feedDeck2,
            text="View deck",
            font=("Helvetica", 8),
            )
        self.feedViewbutton2.pack(side=LEFT)
        self.feedDeck2.pack(side=TOP, fill=X)

        self.feedUsername3 = Frame(self.feed, bg="#d7d8e0") #3rd notif
        self.feedName3 = Button(
            self.feedUsername3,
            textvariable=user3,
            bg="#e6e7f0",
            font=("Helvetica",10)
            )
        self.feedName3.pack(side=LEFT)
        self.feedUsername3.pack(side=TOP, fill=X)

        self.feedContent3 = Frame(self.feed, bg="#e6e7f0")
        self.feedContentname3 = Label(
            self.feedContent3,
            textvariable=user3,
            font=("Helvetica",10,"bold"),
            bg="#e6e7f0"
            )
        self.feedContentname3.pack(side=LEFT)
        self.feedTime3 = Label(
            self.feedContent3,
            text="made a new deck on 11/10/23.",
            font=("Helvetica", 10),
            bg="#e6e7f0"
            )
        self.feedTime3.pack(side=LEFT)
        self.feedContent3.pack(side=TOP, fill=X)

        self.feedDeck3 = Frame(self.feed, bg="#e6e7f0")
        self.feedDeckname3 = Label(
            self.feedDeck3,
            text="Applied Mathematics Histograms",
            font=("Helvetica", 15),
            bg="#e6e7f0"
            )
        self.feedDeckname3.pack(side=LEFT)
        self.feedViewbutton3 = Button(
            self.feedDeck3,
            text="View deck",
            font=("Helvetica", 8),
            )
        self.feedViewbutton3.pack(side=LEFT)
        self.feedDeck3.pack(side=TOP, fill=X)
        self.feed.pack(fill=BOTH, expand=True)
    def fetchUserInfo(self, usernameLogin):
        mycursor.execute("SELECT username, firstName, lastName, userRank, friendRequest, markingRequest, friendList, centre FROM user_account WHERE username=%s", (usernameLogin,))
        userInfo = mycursor.fetchone()
        return userInfo
    def showDashboard(self, usernameLogin): #show method used on each page to refresh info? update sql queries if doesn't work
        username1, firstName1, lastName1, userRank1, friendRequest1, markingRequest1, friendList1, centre1 = self.fetchUserInfo(usernameLogin)
        self.profileUsername.set(username1)
        page1.show()
        
class collectionPage(page):
    def __init__(self, *args, **kwargs):
        page.__init__(self, *args, **kwargs)
        self.collection=Frame(self)
        self.collectionTitle = Label(
            self.collection,
            text="Deck Collection",
            anchor=CENTER,
            bg="#aeafb5", 
            font=("Helvetica",11,"bold"),
            relief=RIDGE
            )
        self.collectionTitle.pack(side=TOP, fill=X)
        self.collection.pack(fill=BOTH, expand=True)

        self.topButtons = Frame(self.collection, bg="#d7d8e0") #top buttons
        self.deckButton = Button(
            self.topButtons, 
            text="New Deck", 
            bg="#bfc0c7", 
            font=("Helvetica",9),
            command=deckWindow
            )
        self.deckButton.pack(side=LEFT)
        self.topButtons.pack(side=TOP, fill=X)
    def fetchUserInfo(self, usernameLogin):
        mycursor.execute("SELECT username, firstName, lastName, userRank, friendRequest, markingRequest, friendList, centre FROM user_account WHERE username=%s", (usernameLogin,))
        userInfo = mycursor.fetchone()
        return userInfo
    def showDashboard(self, usernameLogin):
        username1, firstName1, lastName1, userRank1, friendRequest1, markingRequest1, friendList1, centre1 = self.fetchUserInfo(usernameLogin)
        #self.profileHeader.set(username1)
        page2.show()

class profilePage(page):
    def __init__(self, *args, **kwargs):
        page.__init__(self, *args, **kwargs)
        self.profile=Frame(self)
        self.profileHeader = StringVar()
        self.profileTitle = Label(
            self.profile,
            textvariable=self.profileHeader,
            anchor=CENTER,
            bg="#aeafb5",
            font=("Helvetica",11,"bold"),
            relief=RIDGE
            )
        self.profileTitle.pack(side=TOP, fill=X)
        self.profile.pack(fill=BOTH, expand=True)
    def fetchUserInfo(self, usernameLogin):
        mycursor.execute("SELECT username, firstName, lastName, userRank, friendRequest, markingRequest, friendList, centre FROM user_account WHERE username=%s", (usernameLogin,))
        userInfo = mycursor.fetchone()
        return userInfo
    def showDashboard(self, usernameLogin):
        username1, firstName1, lastName1, userRank1, friendRequest1, markingRequest1, friendList1, centre1 = self.fetchUserInfo(usernameLogin)
        self.profileHeader.set(username1)
        page3.show()

class footer(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        global page0
        global page00
        global page1
        global page2
        global page3
        page0 = loginPage(self)
        page00 = signupPage(self)
        page1 = feedPage(self)
        page2 = collectionPage(self)
        page3 = profilePage(self)

        page0.grid(row=0, column=0, sticky="nsew")
        page00.grid(row=0, column=0, sticky="nsew")
        page1.grid(row=0, column=0, sticky="nsew")
        page2.grid(row=0, column=0, sticky="nsew")
        page3.grid(row=0, column=0, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        page0.show()
    def showButtons(self):
        self.bottomButtons = Frame(self, bg="#e6e7f0") #bottom buttons
        self.feedButton = Button(
            self.bottomButtons,
            text="Feed",
            font=("Helvetica", 12),
            command=lambda:page1.showDashboard(usernameLogin)
            )
        self.feedButton.pack(side=LEFT)
        self.collectionButton = Button(
            self.bottomButtons,
            text="Collection",
            font=("Helvetica", 12),
            command=lambda:page2.showDashboard(usernameLogin)
            )
        self.collectionButton.pack(side=LEFT)
        self.profileButton = Button(
            self.bottomButtons,
            text="Profile",
            font=("Helvetica", 12),
            command=lambda:page3.showDashboard(usernameLogin)
            )
        self.profileButton.pack(side=LEFT)
        self.bottomButtons.grid(row=1, column=0, sticky="nsew")

app = footer(window)
app.pack(side=BOTTOM, fill=X)
window.mainloop()