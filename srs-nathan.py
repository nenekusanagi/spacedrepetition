from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import hashlib
#rename variables + make code more concise/less repeats at the end + less globals
mydb = mysql.connector.connect(host="localhost", user="sqluser", password="password", database="srs_data")
mycursor = mydb.cursor(buffered=True)
#offline ver can be made by try'ing sql connection and then alerting user that they are offline,
#have to choose to download dekcs (even if self made)
#make gui look neater, less empty spaces (fill=X)
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

def inboxWindow():
    inboxTab = Toplevel()
    inboxTab.title("Inbox (1)")
    inboxTab.resizable(False, False)
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
    settingsSection1 = Frame(settingsTab, bg="#d7d8e0")
    settingsHeader1 = Label(
        settingsSection1,
        text="Friend requests",
        font=("Helvetica", 11),
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
        font=("Helvetica", 11),
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
    global deckTab
    global deckEntry1
    global deckEntry2
    deckTab = Toplevel()
    deckTab.title("Create Deck")
    deckTab.resizable(False, False)
    deckSection1 = Frame(deckTab, bg="#d7d8e0")
    deckOption1 = Label(
        deckSection1,
        text="Deck name",
        font=("Helvetica", 11),
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
        font=("Helvetica", 11),
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
        text="Create",
        font=("Helvetica", 9),
        bg="#d7d8e0",
        command=createDeck
        )
    deckCreateButton.pack(side=TOP, fill=X)

def createDeck():
    deckName = deckEntry1.get() #increase cjaracters in deck name
    deckSetting = deckEntry2.get()
    if deckSetting == "Public":
        deckPrivacy = "public"
    elif deckSetting == "Friends only":
        deckPrivacy = "friends"
    elif deckSetting == "Private":
        deckPrivacy = "private"
    mycursor.execute("SELECT * FROM user_deck INNER JOIN user_account ON user_account.accountID = user_deck.accountID WHERE user_deck.deckName = %s AND user_account.username = %s", (deckName, usernameLogin)) #case sensitive
    if mycursor.fetchone():
        messagebox.showerror("Invalid Deck Name", "You already have a deck with this name.")
    else:
        mycursor.execute("INSERT INTO user_deck (accountID, deckName, privacy) VALUES ((SELECT user_account.accountID FROM user_account WHERE user_account.username = %s), %s, %s)", (usernameLogin, deckName, deckPrivacy))
        mydb.commit()
        page2.showDashboard(usernameLogin) #refresh
        deckTab.destroy()

def deckSelected(event): #event taken as an argument due to bind
    global selectedDeck
    selectedDeck = "".join(deckList.get(i) for i in deckList.curselection())
    mycursor.execute("SELECT privacy FROM user_deck INNER JOIN user_account ON user_account.accountID = user_deck.accountID WHERE user_deck.deckName=%s AND user_account.username=%s", (selectedDeck, usernameLogin)) #make sure all sql string input are unique, as to not accidentally fetch someone else's deck
    deckSetting = mycursor.fetchone()
    if deckSetting == ('public',):
        deckPrivacy = "Public"
    elif deckSetting == ('friends',):
        deckPrivacy = "Friends Only"
    elif deckSetting == ('private',):
        deckPrivacy = "Private"
    deckPage = Toplevel()
    deckPage.title(selectedDeck)
    deckPage.resizable(False, False)
    deckFrame=Frame(deckPage, bg="#e6e7f0")
    topButtons = Frame(deckFrame, bg="#d7d8e0")
    addButton = Button(
        topButtons, 
        text="Add Flashcard", 
        bg="#bfc0c7", 
        font=("Helvetica",9),
        command=addFlashcards
        )
    addButton.pack(side=LEFT)
    reviewButton = Button(
        topButtons, 
        text="Review", 
        bg="#bfc0c7", 
        font=("Helvetica",9),
        command=reviewFlashcards
        )
    reviewButton.pack(side=LEFT)
    delete_button = Button(
        topButtons,
        text="Delete",
        bg="#bfc0c7",
        font=("Helvetica",9),
        command=lambda:delete_deck(deckPage)
        )
    delete_button.pack(side=LEFT)
    topButtons.pack(side=TOP, fill=X)
    mainPage = Frame(deckFrame, bg="#e6e7f0")
    deckTitle = Label(
        mainPage,
        text=f"{selectedDeck}",
        font=("Helvetica",14),
        bg="#e6e7f0"
        )
    deckTitle.pack()
    deckPrivate = Label(
        mainPage,
        text=f"Privacy Setting: {deckPrivacy}",
        font=("Helvetica", 12),
        bg="#e6e7f0"
        )
    deckPrivate.pack()
    mainPage.pack(side=TOP, fill=X)
    deckFrame.pack(fill=BOTH, expand=True)

def addFlashcards():
    def checkFormat():
        def add_flashcard():
            if flashcard_format == "text": #add constraints eg length of question, answer...
                question = input_2.get("1.0", "end-1c")
                answer = input_3.get("1.0", "end-1c")
                mycursor.execute("SELECT * FROM user_flashcard INNER JOIN user_deck ON user_deck.deckID = user_flashcard.deckID INNER JOIN user_account ON user_account.accountID = user_deck.accountID WHERE user_flashcard.question = %s AND user_deck.deckName = %s AND user_account.username = %s", (question, selectedDeck, usernameLogin))
                if mycursor.fetchone():
                    messagebox.showerror("Invalid Flashcard", "You already have a flashcard with this question in this deck.")
                else:
                    mycursor.execute("INSERT INTO user_flashcard (deckID, question, answer, cardFormat) VALUES ((SELECT user_deck.deckID FROM user_deck WHERE user_deck.deckName = %s AND (SELECT user_account.accountID FROM user_account WHERE user_account.username = %s)), %s, %s, %s)", (selectedDeck, usernameLogin, question, answer, flashcard_format))
                    mydb.commit()
                    input_2.delete("1.0", "end")
                    input_3.delete("1.0", "end")
        check_card_format = input_1.get()
        title_1.pack_forget()
        input_1.pack_forget()
        button_1.pack_forget()
        header_3.pack_forget()
        if check_card_format == "Basic (Text only)":
            flashcard_format = "text"
            title_2 = Label(
                header_1,
                text="Question",
                font=("Helvetica", 11),
                bg="#d7d8e0"
                )
            title_2.pack(side=LEFT)
            input_2 = Text(header_2, width=30, height=4)
            input_2.pack(side=LEFT)
            header_4 = Frame(window_frame, bg="#d7d8e0")
            title_3 = Label(
                header_4,
                text="Answer",
                font=("Helvetica", 11),
                bg="#d7d8e0"
                )
            title_3.pack(side=LEFT)
            header_4.pack(side=TOP, fill=X)
            header_5 = Frame(window_frame, bg="#e6e7f0")
            input_3 = Text(header_5, width=30, height=7)
            input_3.pack(side=LEFT)
            header_5.pack(side=TOP, fill=X)
            header_6 = Frame(window_frame, bg="#e6e7f0")
            button_2 = Button(
                header_6,
                text="Add",
                font=("Helvetica", 9),
                bg="#d7d8e0",
                command=add_flashcard
                )
            button_2.pack(side=TOP, fill=X)
            header_6.pack(side=TOP, fill=X)
        elif check_card_format == "Media (Audio/images/video)": #dont forget to implement all of these
            flashcard_format = "media"
        elif check_card_format == "Multiple choice":
            flashcard_format = "choice"
        elif check_card_format == "Fill in the gaps":
            flashcard_format = "gaps"
        elif check_card_format == "Image occlusion":
            flashcard_format = "occlusion"
        elif check_card_format == "Mathematics":
            flashcard_format = "maths"
    add_flashcard_page = Toplevel()
    add_flashcard_page.title(selectedDeck)
    add_flashcard_page.resizable(False, False)
    window_frame = Frame(add_flashcard_page, bg="#e6e7f0")
    header_1 = Frame(window_frame, bg="#d7d8e0")
    title_1 = Label(
        header_1,
        text="Format",
        font=("Helvetica", 11),
        bg="#d7d8e0"
        )
    title_1.pack(side=LEFT)
    header_1.pack(side=TOP, fill=X)
    header_2 = Frame(window_frame, bg="#e6e7f0")
    input_1 = ttk.Combobox(
        header_2, 
        state="readonly", 
        values=["Basic (Text only)", "Media (Audio/images/video)", "Multiple choice", "Fill in the gaps", "Image occlusion", "Mathematics"],
        width=25
        )
    input_1.set("Basic (Text only)")
    input_1.pack(side=LEFT)
    header_2.pack(side=TOP, fill=X)
    header_3 = Frame(window_frame, bg="#e6e7f0")
    button_1 = Button(
        header_3,
        text="Add",
        font=("Helvetica", 9),
        bg="#d7d8e0",
        command=checkFormat
        )
    button_1.pack(side=TOP, fill=X)
    header_3.pack(side=TOP, fill=X)
    window_frame.pack(fill=BOTH, expand=True)

def reviewFlashcards():
    mycursor.execute("SELECT flashcardID FROM user_flashcard INNER JOIN user_deck ON user_deck.deckID = user_flashcard.deckID INNER JOIN user_account ON user_account.accountID = user_deck.accountID WHERE user_deck.deckName = %s AND user_account.username = %s", (selectedDeck, usernameLogin))
    if mycursor.fetchone():
        pass #review here
    else:
        messagebox.showerror("Empty Deck", "There are no flashcards in this deck.")

def delete_deck(deckPage):
    answer = messagebox.askokcancel("Delete Deck", f"Are you sure you want to delete {selectedDeck}? All of the flashcards it contains will also be deleted.")
    if answer: #only 1 inner join query able to be used in delete (mysql) + check later for flashcard removal
        mycursor.execute("DELETE user_flashcard FROM user_flashcard INNER JOIN user_deck ON user_deck.deckID = user_flashcard.deckID WHERE user_deck.deckName = %s AND user_deck.accountID IN (SELECT user_account.accountID FROM user_account WHERE user_account.username=%s)", (selectedDeck, usernameLogin))
        mydb.commit()
        mycursor.execute("DELETE user_deck FROM user_deck INNER JOIN user_account ON user_account.accountID = user_deck.accountID WHERE user_deck.deckName = %s AND user_account.username = %s", (selectedDeck, usernameLogin))
        mydb.commit()
        deckPage.destroy()
        page2.showDashboard(usernameLogin) #refresh
    else:
        pass
        
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
            page1.showDashboard(usernameLogin) #use username coz its the only column that requires to be unique across all records
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
        global newFirstname
        global newLastname
        global hashPassword
        newFirstname = newFirstnameEntry.get()
        if self.validateName(newFirstname):
            messagebox.showerror("Invalid First Name", "First name must be between 1 and 30 characters in length.")
        else:
            newLastname = newLastnameEntry.get()
            if self.validateName(newLastname):
                messagebox.showerror("Invalid Last Name", "Last name must be between 1 and 30 characters in length.")
            else:
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
                            if newRank == "I'm a student" or newRank == "I'm a teacher":
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
                                mycursor.execute("INSERT INTO user_account (username, firstName, lastName, password, userRank) VALUES (%s, %s, %s, %s, %s)", (newUsername, newFirstname, newLastname, hashPassword, userNewRank))
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
            mycursor.execute("INSERT INTO user_account (username, firstName, lastName, password, userRank, centre) VALUES (%s, %s, %s, %s, %s, %s)", (newUsername, newFirstname, newLastname, hashPassword, userNewRank, newCentre))
            mydb.commit()
            self.showDetails()
    def validateName(self, newName):
        if len(newName) > 30 or len(newName) < 1:
            return True
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
        self.feed = Frame(self, bg="#e6e7f0")
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

        self.feedUsername1 = Frame(self.feed, bg="#e6e7f0") #1st update
        self.feedName1 = Button(
            self.feedUsername1,
            textvariable=user1,
            font=("Helvetica",10)
            )
        self.feedName1.pack(side=LEFT)
        self.feedUsername1.pack(side=TOP, fill=X)

        self.feedContent1 = Frame(self.feed, bg="#d7d8e0")
        self.feedTime1 = Label(
            self.feedContent1,
            text="2 minutes ago",
            font=("Helvetica", 10),
            bg="#d7d8e0"
            )
        self.feedTime1.pack(side=LEFT)
        self.feedContent1.pack(side=TOP, fill=X)

        self.feedDeck1 = Frame(self.feed, bg="#d7d8e0")
        self.feedDeckname1 = Label(
            self.feedDeck1,
            text="Computer Science Databases",
            font=("Helvetica", 15),
            bg="#d7d8e0"
            )
        self.feedDeckname1.pack(side=LEFT)
        self.feedViewbutton1 = Button(
            self.feedDeck1,
            text="View deck",
            font=("Helvetica", 8),
            )
        self.feedViewbutton1.pack(side=LEFT)
        self.feedDeck1.pack(side=TOP, fill=X)

        self.feed.pack(fill=BOTH, expand=True)
    def fetchUserInfo(self, usernameLogin):
        mycursor.execute("SELECT username, firstName, lastName, userRank, friendRequest, markingRequest, centre FROM user_account WHERE username=%s", (usernameLogin,))
        userInfo = mycursor.fetchone()
        return userInfo
    def showDashboard(self, usernameLogin): #show method used on each page to refresh info? update sql queries if doesn't work
        username1, firstName1, lastName1, userRank1, friendRequest1, markingRequest1, centre1 = self.fetchUserInfo(usernameLogin) #dont need to fetch all the data from the query??use [0] for only username perhaps?or when absolutely necessary
        self.profileUsername.set(username1)
        page1.show()
        
class collectionPage(page):
    def __init__(self, *args, **kwargs):
        page.__init__(self, *args, **kwargs)
        self.collection=Frame(self, bg="#e6e7f0")

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

        self.collection.pack(fill=BOTH, expand=True)
    def fetchUserInfo(self, usernameLogin):
        mycursor.execute("SELECT username, firstName, lastName, userRank, friendRequest, markingRequest, centre FROM user_account WHERE username=%s", (usernameLogin,))
        userInfo = mycursor.fetchone()
        return userInfo
    def fetchDecks(self, usernameLogin):
        mycursor.execute("SELECT deckName, privacy FROM user_deck INNER JOIN user_account ON user_account.accountID = user_deck.accountID WHERE user_account.username = %s", (usernameLogin,))
        userDecks = mycursor.fetchall()
        return userDecks
    def showDashboard(self, usernameLogin):
        username1, firstName1, lastName1, userRank1, friendRequest1, markingRequest1, centre1 = self.fetchUserInfo(usernameLogin) #allowing users to edit decks/flashcards after creation may be a bit long, maybe something to improve in evaluation
        global deckList
        decks = self.fetchDecks(usernameLogin)
        for widget in self.collection.winfo_children():
            if not isinstance(widget, (Listbox, Scrollbar)):
                continue
            widget.destroy()
        scrollbar = Scrollbar(self.collection)
        scrollbar.pack(side = RIGHT, fill=Y)
        deckList = Listbox(self.collection, yscrollcommand=scrollbar.set, bg="#e6e7f0", font=("Helvetica", 12), relief=FLAT, selectmode=SINGLE, selectbackground="#bfc0c7")
        for deck in decks:
            deckList.insert(END, str(deck[0]))
        deckList.pack(fill=BOTH, expand=True)
        deckList.bind("<Double-1>", deckSelected)
        scrollbar.config(command = deckList.yview)
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
        mycursor.execute("SELECT username, firstName, lastName, userRank, friendRequest, markingRequest, centre FROM user_account WHERE username=%s", (usernameLogin,))
        userInfo = mycursor.fetchone()
        return userInfo
    def showDashboard(self, usernameLogin):
        username1, firstName1, lastName1, userRank1, friendRequest1, markingRequest1, centre1 = self.fetchUserInfo(usernameLogin)
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
        self.bottomButtons = Frame(self, bg="#d7d8e0") #bottom buttons
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