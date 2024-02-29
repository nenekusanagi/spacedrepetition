from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import hashlib #create hashing algorithm myself??
import random
#rename variables + make code more concise/less repeats + less globals (by passing local variables into other subroutines) #(remove passing variables into subroutines if not necessary)
mydb = mysql.connector.connect(host="localhost", user="sqluser", password="password", database="srs_data")
mycursor = mydb.cursor(buffered=True)
#offline ver can be made by try'ing sql connection and then alerting user that they are offline,
#have to choose to download dekcs (even if self made)
#make gui look neater, less empty spaces (side=TOP, fill=X)
#use sql order by if necessary + regular refreshes of pages
#make windows same size esp in flashcard reviewing ,,,,,,,maybe?
#style sheets for tkinter in repeating code for widgets?
#check sql data type length and that all exceptions are handled accordingly when signig up or smth/creating stuff
window = Tk()
window.title("Spaced Repetition Flashcard Software")
#window.iconbitmap("librarypc.ico")
window['bg']="#e6e7f0"
window.resizable(False, False)

class Flashcard:
    def __init__(self, id, question, answer, format, priority):
        self.id = id
        self.question = question
        self.answer = answer
        self.format = format
        self.priority = priority

class PeerFlashcard(Flashcard):
    def __init__(self, id, question, answer, format, priority, input):
        super().__init__(id, question, answer, format, priority)
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
            while position != self.rear and self.queue[position].priority >= priority: #also deal with when card doesnt have priority lol (if priority == 0?) #checking all cards from front until finding one with lower priority
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
            else: #shuffle all flashcards after target position along 1 #simplify all this?
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
    def getFront(self):
        return self.front
    def getRear(self):
        return self.rear
    
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
    def peek(self):#do i even need this lol
        if self.isEmpty():
            return None
        else:
            return self.stack[self.top]
    def getStack(self):
        return list((flashcard.id, flashcard.question, flashcard.input) for flashcard in self.stack if flashcard is not None)

class page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

user1 = StringVar(window,"user_friend") #replace and get rid of
user2 = StringVar(window,"user_friend_2") #replace
user3 = StringVar(window,"user_friend_3") #replace

def settingsWindow():
    global settingsButtonon1
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
        settingsButtonoff1.config(bg="#d7d8e0", relief=RAISED)
        mycursor.execute("UPDATE user_account SET friendRequest = 'on' WHERE username = %s", (usernameLogin,))
        mydb.commit()

def friendOffPressed():
    if settingsButtonoff1.cget("bg") == "#d7d8e0":
        settingsButtonon1.config(bg="#d7d8e0", relief=RAISED)
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
    mycursor.execute("SELECT * FROM user_deck INNER JOIN user_account ON user_account.accountID = user_deck.accountID WHERE user_deck.deckName = %s AND user_account.username = %s", (deckName, usernameLogin)) #case sensitive
    if mycursor.fetchone():
        messagebox.showerror("Invalid Deck Name", "You already have a deck with this name.")#add more constraints?
    else:
        mycursor.execute("INSERT INTO user_deck (accountID, deckName) VALUES ((SELECT user_account.accountID FROM user_account WHERE user_account.username = %s), %s)", (usernameLogin, deckName))
        mydb.commit()
        page1.showDashboard(usernameLogin) #refresh
        deckTab.destroy()

def deckSelected(event): #event taken as an argument due to bind
    global refresh_flashcards
    def fetch_flashcards():
        mycursor.execute("SELECT question, answer FROM user_flashcard INNER JOIN user_deck ON user_deck.deckID = user_flashcard.deckID INNER JOIN user_account ON user_account.accountID = user_deck.accountID WHERE user_deck.deckName = %s AND user_account.username = %s ORDER BY flashcardID DESC", (selectedDeck, usernameLogin))
        flashcards = mycursor.fetchall()
        return flashcards
    def refresh_flashcards():
        for widget in list_page.winfo_children():
            if not isinstance(widget, (Listbox, Scrollbar)):
                continue
            widget.destroy()
        yscrollbar = Scrollbar(list_page)
        yscrollbar.pack(side=RIGHT, fill=Y)
        xscrollbar = Scrollbar(list_page)
        xscrollbar.pack(side=BOTTOM, fill=X)
        flashcard_list = Listbox(list_page, yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set, bg="#e6e7f0", font=("Helvetica", 9), relief=FLAT, selectmode=SINGLE, selectbackground="#e6e7f0", selectforeground="#000000", activestyle="none", width=50)
        flashcards = fetch_flashcards()
        for flashcard in flashcards:
            flashcard_list.insert(END, flashcard[0])
            flashcard_list.itemconfig(END, bg="#d7d8e0")
            flashcard_list.insert(END, flashcard[1])
        flashcard_list.pack(fill=BOTH, expand=True)
        yscrollbar.config(command=flashcard_list.yview)
        xscrollbar.config(command=flashcard_list.xview)
    global selectedDeck
    selectedDeck = "".join(deckList.get(i) for i in deckList.curselection())
    mycursor.execute("SELECT score FROM user_deck INNER JOIN user_account ON user_account.accountID = user_deck.accountID WHERE user_deck.deckName=%s AND user_account.username=%s", (selectedDeck, usernameLogin)) #make sure all sql string input are unique, as to not accidentally fetch someone else's deck
    deck_results = mycursor.fetchone()
    deck_score = deck_results[0]
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
        command=lambda:reviewFlashcards(deckPage, deckList)
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
    deck_score_label = Label(
        mainPage,
        text=f"{deck_score}%",
        font=("Helvetica", 12, "bold"),
        bg="#e6e7f0"
        )
    deck_score_label.pack()
    mainPage.pack(side=TOP, fill=X)
    list_page = Frame(deckFrame, bg="#e6e7f0")
    list_page.pack(side=TOP, fill=X)
    deckFrame.pack(fill=BOTH, expand=True)
    refresh_flashcards()

def addFlashcards():
    def checkFormat():
        def add_flashcard():
            if flashcard_format == "text": #add constraints eg length of question, answer... (probably increase length coz wtf)
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
                    refresh_flashcards()
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
    global add_flashcard_page
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

def reviewFlashcards(deckPage, deckList):
    def do_pass(): #so that listbox is binded when "finish" button is pressed
        pass
    def fetch_flashcards():
        mycursor.execute("SELECT flashcardID, question, answer, cardFormat, priority FROM user_flashcard INNER JOIN user_deck ON user_deck.deckID = user_flashcard.deckID INNER JOIN user_account ON user_account.accountID = user_deck.accountID WHERE user_deck.deckName = %s AND user_account.username = %s", (selectedDeck, usernameLogin))
        flashcards = mycursor.fetchall()
        return flashcards
    def queue_flashcards(flashcards, flashcard_queue):
        for flashcard in flashcards:
            flashcard = Flashcard(flashcard[0], flashcard[1], flashcard[2], flashcard[3], flashcard[4])#simpler way to do this using list comprehension?
            flashcard_queue.enQueue(flashcard)
    def review_flashcards(): #indirect recursion? base case is when deQueue returns None (i.e. queue is empty) or number > 10 #review card based on card format
        def answer_review(new_flashcard, question_header, input_text, flip_button, flashcards_reviewed, reviewed_list):
            def update_priority(new_flashcard, new_priority, reviewed_list):
                new_priority = max(0, min(10, new_priority))
                mycursor.execute("UPDATE user_flashcard SET priority = %s WHERE flashcardID = %s", (new_priority, new_flashcard.id)) #make sure flashcards with lowest priority arent just left at the back forever - if all cards are the same priority, randomise?#also document all this
                mydb.commit()
                reviewed_list.append([new_flashcard.id, new_flashcard.question, new_flashcard.answer, new_flashcard.format, new_priority]) #no option to edit DURING reviews
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
            def peer_rating_push(new_flashcard, reviewed_list):
                peer_flashcard = PeerFlashcard(new_flashcard.id, new_flashcard.question, new_flashcard.answer, new_flashcard.format, new_flashcard.priority, user_input)
                peer_review_stack.push(peer_flashcard)
                print(peer_review_stack.getStack())
                reviewed_list.append([new_flashcard.id, new_flashcard.question, new_flashcard.answer, new_flashcard.format, new_flashcard.priority])
            user_input = input_text.get("1.0", "end-1c")
            question_header.pack_forget()
            flip_button.pack_forget()
            input_text.pack_forget()
            answer_header = Label(
                text_frame,
                text=f"{new_flashcard.answer}",
                font=("Helvetica", 14),
                bg="#e6e7f0",
                wraplength=500,
                pady=5
                )
            answer_header.pack()
            output_header = Label(
                text_frame,
                text="You wrote:",
                font=("Helvetica", 10),
                bg="#e6e7f0"
                )
            output_header.pack()
            output_text = Label(
                text_frame,
                text=f"{user_input}",
                font=("Helvetica", 9),
                bg="#e6e7f0",
                wraplength=450
                )
            output_text.pack()
            rating1_button = Button(
                button_frame,
                text="Fail",
                font=("Helvetica", 9),
                bg="#bfc0c7",
                command=lambda:[flashcard_rating1(new_flashcard, reviewed_list), question_review(flashcards_reviewed, reviewed_list)] #in order of function being called
                )
            rating1_button.pack(side=LEFT)
            rating2_button = Button(
                button_frame,
                text="Hard",
                font=("Helvetica", 9),
                bg="#bfc0c7",
                command=lambda:[flashcard_rating2(new_flashcard, reviewed_list), question_review(flashcards_reviewed, reviewed_list)]
                )
            rating2_button.pack(side=LEFT)
            rating3_button = Button(
                button_frame,
                text="Good",
                font=("Helvetica", 9),
                bg="#bfc0c7",
                command=lambda:[flashcard_rating3(new_flashcard, reviewed_list), question_review(flashcards_reviewed, reviewed_list)]
                )
            rating3_button.pack(side=LEFT)
            rating4_button = Button(
                button_frame,
                text="Easy",
                font=("Helvetica", 9),
                bg="#bfc0c7",
                command=lambda:[flashcard_rating4(new_flashcard, reviewed_list), question_review(flashcards_reviewed, reviewed_list)]
                )
            rating4_button.pack(side=LEFT)
            peer_button = Button(
                button_frame,
                text="Peer Mark",
                font=("Helvetica", 9),
                bg="#bfc0c7",
                command=lambda:[peer_rating_push(new_flashcard, reviewed_list), question_review(flashcards_reviewed, reviewed_list)]
            )
            peer_button.pack(side=RIGHT)
        def question_review(flashcards_reviewed, reviewed_list):
            def end_review():
                def peer_review():
                    def fetchfriend_info():
                        mycursor.execute("SELECT ua2.username FROM user_account ua1 INNER JOIN user_friend ON user_friend.accountID = ua1.accountID INNER JOIN user_account ua2 ON ua2.accountID = user_friend.accountID2 WHERE ua1.username = %s", (usernameLogin,))
                        return mycursor.fetchall()
                    def check_peer(peer_flashcard):
                        selected_indices = peers_list.curselection()
                        if selected_indices:
                            selected_peer = "".join(peers_list.get(i) for i in selected_indices)
                            mycursor.execute("SELECT * FROM user_peermarking INNER JOIN user_account ON user_account.accountID = user_peermarking.accountID WHERE user_peermarking.flashcardID = %s AND user.account_username = %s"), (peer_flashcard.id, usernameLogin)
                            if mycursor.fetchone():
                                messagebox.showerror("Invalid Flashcard", "This flashcard is already pending a response in a different peer marking submission.")
                            else:
                                mycursor.execute("SELECT * FROM user_account WHERE username = %s AND markingRequest = 'off'", (selected_peer,))
                                if mycursor.fetchone():
                                    messagebox.showerror("Invalid Friend", "This user has peer marking turned off.")
                                else:
                                    mycursor.execute("INSERT INTO user_peermarking (accountID, flashcardID, accountID2, useranswer) VALUES ((SELECT user_account.accountID FROM user_account WHERE user_account.username = %s), %s, (SELECT user_account.accountID FROM user_account WHERE user_account.username = %s), %s)", (usernameLogin, peer_flashcard.id, selected_peer, peer_flashcard.input))
                                    messagebox.showinfo("Marking Request Sent", f"Your marking request to {selected_peer} has been sent and is now pending a response.")
                        else:
                            messagebox.showerror("Invalid Friend", "No friend has been selected.")
                    for widget in text_frame.winfo_children():
                        if not isinstance(widget, (Label)):
                            continue
                        widget.destroy()
                    for widget in button_frame.winfo_children():
                        if not isinstance(widget, (Button)):
                            continue
                        widget.destroy()
                    for widget in button_frame.winfo_children():
                        if not isinstance(widget, (Scrollbar)):
                            continue
                        widget.destroy()
                    for widget in button_frame.winfo_children():
                        if not isinstance(widget, (Listbox)):
                            continue
                        widget.destroy()
                    peer_flashcard = peer_review_stack.pop()
                    peer_question = Label(
                        text_frame,
                        text=f"{peer_flashcard.question}",
                        font=("Helvetica", 12, "bold"),
                        wraplength=500,
                        bg="#e6e7f0"
                        )
                    peer_question.pack()
                    peer_answer = Label(
                        text_frame,
                        text=f"{peer_flashcard.answer}",
                        font=("Helvetica", 12),
                        wraplength=500,
                        bg="#e6e7f0"
                        )
                    peer_answer.pack()
                    peer_header = Label(
                        text_frame,
                        text="You wrote:",
                        font=("Helvetica", 9),
                        bg="#e6e7f0"
                        )
                    peer_header.pack()
                    peer_output = Label(
                        text_frame,
                        text=f"{peer_flashcard.input}",
                        font=("Helvetica", 13),
                        bg="#e6e7f0",
                        wraplength=450
                        )
                    peer_output.pack()
                    peer_subheader = Label(
                        text_frame,
                        text="Select a friend to send your answer to:",
                        font=("Helvetica", 9),
                        bg="#e6e7f0"
                        )
                    peer_subheader.pack()
                    peers = fetchfriend_info()
                    friend_scrollbar = Scrollbar(text_frame)
                    friend_scrollbar.pack(side=RIGHT, fill=Y)
                    peers_list = Listbox(text_frame, yscrollcommand=friend_scrollbar.set, bg="#e6e7f0", font=("Helvetica", 10), relief=FLAT, selectmode=SINGLE, selectbackground="#bfc0c7")
                    for peer in peers:
                        peers_list.insert(END, peer[0])
                    peers_list.pack(fill=BOTH, expand=TRUE)
                    friend_scrollbar.config(command=peers_list.yview)
                    send_button = Button(
                        button_frame,
                        text="Send",
                        font=("Helvetica",9),
                        bg="#bfc0c7",
                        command=lambda:check_peer(peer_flashcard)
                        )
                    send_button.pack(side=LEFT)
                number_stacked = len(peer_review_stack.getStack())
                if number_stacked > 0:
                    peer_review()
                else:
                    mycursor.execute("SELECT priority FROM user_flashcard INNER JOIN user_deck ON user_deck.deckID = user_flashcard.deckID INNER JOIN user_account ON user_account.accountID = user_deck.accountID WHERE user_deck.deckName = %s AND user_account.username = %s", (selectedDeck, usernameLogin))
                    result = mycursor.fetchall()
                    flashcards_number = len(result)
                    flashcards_sum = 0
                    for i in range (0, len(result)):
                        if result[i][0] == -1:
                            flashcards_sum += 7 #weighed(?) priority for non-used cards
                        else:
                            flashcards_sum += result[i][0]
                    score = round((10 - (flashcards_sum / flashcards_number)) * 10, 1) #make it so a flashcard has to have a certain number of "easy"s to immediately be considered 100%?  or mkae an "ease" value which increases/decreases with each "easy" - max 100 or smth, and then combine this to find a reliable priority in the queue - although above algorith already kinda solves this
                    score = max(0.0, min(100.0, score)) #not even necessary i think but idk just in case
                    mycursor.execute("UPDATE user_deck INNER JOIN user_account ON user_account.accountID = user_deck.accountID SET user_deck.score = %s WHERE user_deck.deckName = %s AND user_account.username = %s", (score, selectedDeck, usernameLogin))
                    mydb.commit()
                    grade_title = Label(
                        text_frame,
                        text="Overall Deck Score",
                        font=("Helvetica",17),
                        bg="#e6e7f0"
                        )
                    grade_title.pack()
                    score_title = Label(
                        text_frame,
                        text=f"{score}%",
                        font=("Helvetica",20,"bold"),
                        bg="#e6e7f0"
                        )
                    score_title.pack()
                    again_button = Button(
                        button_frame,
                        text="Review Again",
                        font=("Helvetica",9),
                        bg="#bfc0c7",
                        command=lambda:review_again(flashcards_reviewed, reviewed_list)
                        )
                    again_button.pack(side=LEFT)
                    finish_button = Button( #finish button allows all data to be uploaded to mysql database
                        button_frame,
                        text="Finish",
                        font=("Helvetica",9),
                        bg="#bfc0c7",
                        command=finish_review
                        )
                    finish_button.pack(side=LEFT)
            def finish_review():
                review_flashcards_page.destroy()
                deckList.bind("<Double-1>", deckSelected)
            def review_again(flashcards_reviewed, reviewed_list):
                for i in range(0, len(reviewed_list)): #list used (instead of stack/queue bc...) (this list basically functions as a queue anyway, but the order isn't relevant because it'll be arranged by priority by cpq)
                    again_flashcard = Flashcard(reviewed_list[i][0], reviewed_list[i][1], reviewed_list[i][2], reviewed_list[i][3], reviewed_list[i][4])
                    flashcard_queue.enQueue(again_flashcard) #utilises circular queue's wrapping around properties
                print(reviewed_list)
                print(len(reviewed_list))
                flashcards_reviewed = 0
                reviewed_list = []
                question_review(flashcards_reviewed, reviewed_list)
            for widget in text_frame.winfo_children():
                if not isinstance(widget, (Label)): #replace with pack_forget()???if possible #change len(mycursor.fetchall()) to count(*)??
                    continue
                widget.destroy()
            for widget in button_frame.winfo_children():
                if not isinstance(widget, (Button)):
                    continue
                widget.destroy()
            print(flashcard_queue.getQueue())
            flashcards_reviewed += 1
            if flashcards_reviewed > 10:
                end_review()
            else:
                new_flashcard = flashcard_queue.deQueue()
                if new_flashcard is None: #pop stacked cards and show one by one and who to send to (if there are any), after: #grade/total score of deck after completed reivew
                    end_review()
                else:
                    question_header = Label(
                        text_frame,
                        text=f"{new_flashcard.question}",
                        font=("Helvetica",14),
                        bg="#e6e7f0",
                        wraplength=500
                        )
                    question_header.pack()
                    input_text = Text(text_frame, width=50, height=9)
                    input_text.pack(fill=X)
                    flip_button = Button(
                        button_frame,
                        text="Flip",
                        font=("Helvetica",9),
                        bg="#bfc0c7",
                        command=lambda:answer_review(new_flashcard, question_header, input_text, flip_button, flashcards_reviewed, reviewed_list)
                        )
                    flip_button.pack(side=TOP, fill=X)
        deckList.unbind("<Double-1>") #cannot open window while reviewing in case the user deletes deck -> causes sql error
        review_flashcards_page = Toplevel()
        review_flashcards_page.title(selectedDeck)
        review_flashcards_page.protocol("WM_DELETE_WINDOW", do_pass)
        review_flashcards_page.resizable(False, False) #all flashcards put into queue, and organised depending on priority thanks to enQueue(). flashcard reviews are 10 at a time, and are dequeued one by one to get the next flashcard
        flashcards = fetch_flashcards()
        deck_size = len(flashcards)
        flashcard_queue = CircularPriorityQueue(deck_size)
        queue_flashcards(flashcards, flashcard_queue)
        peer_review_stack = Stack(deck_size)#if user has no friends, tjhen cant add to peer mark stacj
        review_page = Frame(review_flashcards_page, bg="#e6e7f0")
        text_frame = Frame(review_page, bg="#e6e7f0")
        text_frame.pack(side=TOP, fill=X)
        button_frame = Frame(review_page, bg="#d7d8e0")
        button_frame.pack(side=TOP, fill=X)
        review_page.pack(fill=BOTH, expand=TRUE)
        flashcards_reviewed = 0
        reviewed_list = []
        question_review(flashcards_reviewed, reviewed_list)
    mycursor.execute("SELECT flashcardID FROM user_flashcard INNER JOIN user_deck ON user_deck.deckID = user_flashcard.deckID INNER JOIN user_account ON user_account.accountID = user_deck.accountID WHERE user_deck.deckName = %s AND user_account.username = %s", (selectedDeck, usernameLogin))
    if mycursor.fetchone():
        if "add_flashcard_page" in globals():#check again
            add_flashcard_page.destroy()
        deckPage.destroy()
        review_flashcards()
    else:
        messagebox.showerror("Empty Deck", "There are no flashcards in this deck.")

def delete_deck(deckPage):
    message_answer = messagebox.askokcancel("Delete Deck", f"Are you sure you want to delete {selectedDeck}? All of the flashcards it contains will also be deleted.")
    if message_answer: #only 1 inner join able to be used in delete query
        mycursor.execute("DELETE user_flashcard FROM user_flashcard INNER JOIN user_deck ON user_deck.deckID = user_flashcard.deckID WHERE user_deck.deckName = %s AND user_deck.accountID IN (SELECT user_account.accountID FROM user_account WHERE user_account.username=%s)", (selectedDeck, usernameLogin))
        mydb.commit()
        mycursor.execute("DELETE user_deck FROM user_deck INNER JOIN user_account ON user_account.accountID = user_deck.accountID WHERE user_deck.deckName = %s AND user_account.username = %s", (selectedDeck, usernameLogin))
        mydb.commit()
        deckPage.destroy()
        page1.showDashboard(usernameLogin) #refresh
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
                            mycursor.execute("INSERT INTO user_account (username, firstName, lastName, password) VALUES (%s, %s, %s, %s)", (newUsername, newFirstname, newLastname, hashPassword))
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
    def showDetails(self):
        self.showLoginPage()
        messagebox.showinfo("Account Creation", f"Welcome {newUsername}!\nPlease log in with your new account.")
    def showLoginPage(self):
        page0.show()
        
class collectionPage(page):
    def __init__(self, *args, **kwargs):
        page.__init__(self, *args, **kwargs)
        self.fullname = StringVar()
        self.friendsnumber = StringVar()

        self.collection=Frame(self, bg="#e6e7f0")

        self.top_buttons = Frame(self.collection, bg="#d7d8e0") #top buttons
        self.usernameLabel = Label(
            self.top_buttons,
            textvariable=self.fullname,
            bg="#d7d8e0", 
            font=("Helvetica", 9)
            )
        self.usernameLabel.pack(side=LEFT)
        self.settingsButton = Button(
            self.top_buttons,
            text="Settings",
            bg="#bfc0c7",
            font=("Helvetica", 9),
            command=settingsWindow
            )
        self.settingsButton.pack(side=RIGHT)
        self.friends_button = Button(
            self.top_buttons,
            textvariable=self.friendsnumber,
            bg="#bfc0c7",
            font=("Helvetica", 9),
            command=self.friendslist_page
            )
        self.friends_button.pack(side=RIGHT)
        self.deck_button = Button(
            self.top_buttons, 
            text="New Deck", 
            bg="#bfc0c7", 
            font=("Helvetica",9),
            command=deckWindow
            )
        self.deck_button.pack(side=RIGHT)
        self.top_buttons.pack(side=TOP, fill=X)

        self.collection.pack(fill=BOTH, expand=True)
    def friendslist_page(self):
        def fetch_friendinfo():
            mycursor.execute("SELECT ua2.username FROM user_account ua1 INNER JOIN user_friend ON user_friend.accountID = ua1.accountID INNER JOIN user_account ua2 ON ua2.accountID = user_friend.accountID2 WHERE ua1.username = %s", (usernameLogin,))
            return mycursor.fetchall()
        def check_friend():
            friend_username = self.friend_input.get()
            if not friend_username:
                messagebox.showerror("Invalid Username", "Username is empty.")
            else:
                if friend_username == usernameLogin:
                    messagebox.showerror("Invalid Username", "You cannot send a friend request to yourself.")
                else:
                    mycursor.execute("SELECT * FROM user_account WHERE username = %s", (friend_username,))
                    if mycursor.fetchone():
                        mycursor.execute("SELECT * FROM user_friend INNER JOIN user_account ua1 ON ua1.accountID = user_friend.accountID INNER JOIN user_account ua2 ON ua2.accountID = user_friend.accountID2 WHERE ua1.username = %s AND ua2.username = %s", (usernameLogin, friend_username))
                        if mycursor.fetchone(): #also for if you have already sent friend request, or the user has already sent friend request to you
                            messagebox.showerror("Invalid Username", "You are already friends with this user.")
                        else:
                            mycursor.execute("SELECT * FROM user_friendrequest INNER JOIN user_account ua1 ON ua1.accountID = user_friendrequest.accountID INNER JOIN user_account ua2 ON ua2.accountID = user_friendrequest.accountID2 WHERE ua1.username = %s AND ua2.username = %s", (usernameLogin, friend_username))
                            if mycursor.fetchone():
                                messagebox.showerror("Invalid Username", "You have already sent a friend request to this user.")
                            else:
                                mycursor.execute("SELECT * FROM user_friendrequest INNER JOIN user_account ua1 ON ua1.accountID = user_friendrequest.accountID INNER JOIN user_account ua2 ON ua2.accountID = user_friendrequest.accountID2 WHERE ua1.username = %s AND ua2.username = %s", (friend_username, usernameLogin))
                                if mycursor.fetchone():
                                    messagebox.showerror("Invalid Username", "This user has already sent you a friend request.")
                                else:
                                    mycursor.execute("SELECT * FROM user_account WHERE username = %s AND friendRequest = 'off'", (friend_username,))
                                    if mycursor.fetchone():
                                        messagebox.showerror("Invalid Username", "This user has friend requests turned off.")
                                    else:
                                        mycursor.execute("INSERT INTO user_friendrequest (accountID, accountID2) VALUES ((SELECT user_account.accountID FROM user_account WHERE user_account.username = %s), (SELECT user_account.accountID FROM user_account WHERE user_account.username = %s))", (usernameLogin, friend_username))
                                        mydb.commit()
                                        messagebox.showinfo("Friend Request Sent", f"Your friend request to {friend_username} has been sent and is now pending.")
                    else:
                        messagebox.showerror("Invalid Username", "This user does not exist.")
        def forget_request(request_username, inner_frame, requesting_user, accept_button, deny_button):
            inner_frame.pack_forget()
            requesting_user.pack_forget()
            accept_button.pack_forget()
            deny_button.pack_forget()
            mycursor.execute("DELETE user_friendrequest FROM user_friendrequest INNER JOIN user_account ua1 ON ua1.accountID = user_friendrequest.accountID WHERE ua1.username = %s AND user_friendrequest.accountID2 = (SELECT ua2.accountID FROM user_account AS ua2 WHERE ua2.username=%s)", (request_username, usernameLogin))
            mydb.commit()
        def accept_request(request_username, inner_frame, requesting_user, accept_button, deny_button):
            self.friends_list.insert(END, request_username)
            mycursor.execute("INSERT INTO user_friend (accountID, accountID2) VALUES ((SELECT user_account.accountID FROM user_account WHERE user_account.username = %s), (SELECT user_account.accountID FROM user_account WHERE user_account.username = %s))", (usernameLogin, request_username))
            mydb.commit()
            mycursor.execute("INSERT INTO user_friend (accountID, accountID2) VALUES ((SELECT user_account.accountID FROM user_account WHERE user_account.username = %s), (SELECT user_account.accountID FROM user_account WHERE user_account.username = %s))", (request_username, usernameLogin))
            mydb.commit()
            forget_request(request_username, inner_frame, requesting_user, accept_button, deny_button)
        self.friend_info = fetch_friendinfo()
        self.friendrequest_info = self.fetch_friendrequestinfo()
        self.friendslist = Toplevel()
        self.friendslist.title("Friends")
        self.friendslist.resizable(False, False)
        self.main_list = Frame(self.friendslist, bg="#e6e7f0")
        self.friendslist_header = Frame(self.main_list, bg="#d7d8e0")
        self.friends_header = Label(
            self.friendslist_header,
            text="Friends list",
            bg="#d7d8e0",
            font=("Helvetica", 11)
            )
        self.friends_header.pack()
        self.friendslist_header.pack(side=TOP, fill=X)
        self.friendslist_frame = Frame(self.main_list, bg="#e6e7f0")
        self.scrollbar = Scrollbar(self.friendslist_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.friends_list = Listbox(self.friendslist_frame, yscrollcommand=self.scrollbar.set, bg="#e6e7f0", font=("Helvetica", 9), relief=FLAT, selectmode=SINGLE, selectbackground="#e6e7f0", selectforeground="#000000", activestyle="none")
        self.friends_list.pack(fill=BOTH, expand=TRUE)
        self.scrollbar.config(command = self.friends_list.yview)
        self.friendslist_frame.pack(fill=BOTH, expand=TRUE)
        self.friendrequestslist_header = Frame(self.main_list, bg="#d7d8e0")
        self.friendrequests_header = Label(
            self.friendrequestslist_header,
            text="Friend requests",
            bg="#d7d8e0",
            font=("Helvetica", 11)
            )
        self.friendrequests_header.pack()
        self.friendrequestslist_header.pack(side=TOP, fill=X)
        self.friendrequestslist_frame = Frame(self.main_list, bg="#e6e7f0")
        self.friendrequestslist_frame.pack()
        self.top_header = Frame(self.main_list, bg="#d7d8e0")
        self.add_title = Label(
            self.top_header,
            text="Enter username:",
            bg="#d7d8e0",
            font=("Helvetica", 9)
            )
        self.add_title.pack(side=LEFT)
        self.friend_input = Entry(self.top_header)
        self.friend_input.pack(side=LEFT, fill=X, expand=TRUE)
        self.add_button = Button(
            self.top_header,
            text="Add friend",
            bg="#bfc0c7",
            font=("Helvetica", 9),
            command=check_friend
            )
        self.add_button.pack(side=RIGHT)
        self.top_header.pack(side=BOTTOM, fill=X)
        self.main_list.pack(fill=BOTH, expand=TRUE)
        if not self.friend_info:
            pass
        else:
            for friend in self.friend_info:
                self.friends_list.insert(END, friend[0])
        if not self.friendrequest_info:
            pass
        else:
            for request in self.friendrequest_info:
                inner_frame = Frame(self.friendrequestslist_frame, bg="#e6e7f0")
                requesting_user = Label(
                    inner_frame,
                    text=f"{request[1]} {request[2]} ({request[0]}) has sent you a friend request.",
                    bg="#e6e7f0",
                    font=("Helvetica", 9)
                    )
                requesting_user.pack(side=LEFT)
                accept_button = Button(
                    inner_frame,
                    text="Accept",
                    font=("Helvetica", 9)
                    )
                accept_button.pack(side=LEFT)
                deny_button = Button(
                    inner_frame,
                    text="Deny",
                    font=("Helvetica", 9)
                    )
                deny_button.pack(side=LEFT)
                accept_button.configure(command=lambda request=request, inner_frame=inner_frame, requesting_user=requesting_user, accept_button=accept_button, deny_button=deny_button: accept_request(request[0], inner_frame, requesting_user, accept_button, deny_button))
                deny_button.configure(command=lambda request=request, inner_frame=inner_frame, requesting_user=requesting_user, accept_button=accept_button, deny_button=deny_button: forget_request(request[0], inner_frame, requesting_user, accept_button, deny_button))
                inner_frame.pack(fill=BOTH, expand=TRUE)
    def fetchUserInfo(self, usernameLogin):
        mycursor.execute("SELECT username, firstName, lastName, friendRequest, markingRequest FROM user_account WHERE username=%s", (usernameLogin,))
        return mycursor.fetchone()
    def fetch_friendrequestinfo(self):
        mycursor.execute("SELECT ua1.username, ua1.firstName, ua1.lastName FROM user_account ua1 INNER JOIN user_friendrequest ON user_friendrequest.accountID = ua1.accountID INNER JOIN user_account ua2 ON user_friendrequest.accountID2 = ua2.accountID WHERE ua2.username = %s", (usernameLogin,))
        return mycursor.fetchall()
    def fetchDecks(self):
        mycursor.execute("SELECT deckName FROM user_deck INNER JOIN user_account ON user_account.accountID = user_deck.accountID WHERE user_account.username = %s ORDER BY deckName ASC", (usernameLogin,))
        return mycursor.fetchall()
    def showDashboard(self, usernameLogin): #show method used on each page to refresh info? update sql queries if doesn't work
        global deckList
        user_info = self.fetchUserInfo(usernameLogin)
        friendsnumber = len(self.fetch_friendrequestinfo())
        username = user_info[0]
        firstname = user_info[1]
        lastname = user_info[2]
        self.fullname.set(f"{firstname} {lastname} ({username})")
        if friendsnumber == 0:
            self.friendsnumber.set("Friends")
        else:
            self.friendsnumber.set(f"Friends ({friendsnumber})")
        for widget in self.collection.winfo_children(): #cant use pack_forget coz used befor its declared iguess??
            if not isinstance(widget, (Listbox, Scrollbar)):
                continue
            widget.destroy()
        decks = self.fetchDecks()
        self.scrollbar = Scrollbar(self.collection)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        deckList = Listbox(self.collection, yscrollcommand=self.scrollbar.set, bg="#e6e7f0", font=("Helvetica", 12), relief=FLAT, selectmode=SINGLE, selectbackground="#bfc0c7")
        for deck in decks:
            deckList.insert(END, deck[0])
        deckList.pack(fill=BOTH, expand=True)
        deckList.bind("<Double-1>", deckSelected)
        self.scrollbar.config(command = deckList.yview)
        page1.show()

class inboxPage(page):
    def __init__(self, *args, **kwargs):
        page.__init__(self, *args, **kwargs)
        inboxNotification1 = Frame(self, bg="#d7d8e0")
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
        inboxContent1 = Frame(self, bg="#e6e7f0")
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
        inboxButtons1 = Frame(self, bg="#e6e7f0")
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
            self,
            text=" ",
            font=("Helvetica", 1),
            bg="#aeafb5"
            )
        inboxMidfiller1.pack(side=TOP, fill=X)
        inboxNotification2 = Frame(self, bg="#e6e7f0")
        inboxName2 = Label(
            inboxNotification2,
            text="Marking feedback",
            font=("Helvetica", 9),
            bg="#e6e7f0"
            )
        inboxName2.pack(side=LEFT)
        inboxNotification2.pack(side=TOP, fill=X)
        inboxContent2 = Frame(self)
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
        inboxButtons2 = Frame(self)
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
            self,
            text=" ",
            font=("Helvetica", 1),
            bg="#aeafb5"
            )
        inboxMidfiller2.pack(side=TOP, fill=X)
        inboxNotification3 = Frame(self, bg="#e6e7f0")
        inboxName3 = Label(
            inboxNotification3,
            text="Marking request denied",
            font=("Helvetica", 9),
            bg="#e6e7f0"
            )
        inboxName3.pack(side=LEFT)
        inboxNotification3.pack(side=TOP, fill=X)
        inboxContent3 = Frame(self)
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
        inboxButtons3 = Frame(self)
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
        inboxButtons3.pack(side=TOP, fill=X)
    def showDashboard(self, usernameLogin):
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

        page0.grid(row=0, column=0, sticky="nsew")
        page00.grid(row=0, column=0, sticky="nsew")
        page1.grid(row=0, column=0, sticky="nsew")
        page2.grid(row=0, column=0, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        page0.show()
    def showButtons(self):
        self.bottomButtons = Frame(self, bg="#d7d8e0") #bottom buttons
        self.collectionButton = Button(
            self.bottomButtons,
            text="Collection",
            font=("Helvetica", 12),
            command=lambda:page1.showDashboard(usernameLogin)
            )
        self.collectionButton.pack(side=LEFT)
        self.searchButton = Button(
            self.bottomButtons,
            text="Inbox (1)",
            font=("Helvetica", 12),
            command=lambda:page2.showDashboard(usernameLogin)
            )
        self.searchButton.pack(side=LEFT)
        self.bottomButtons.grid(row=1, column=0, sticky="nsew")

app = footer(window)
app.pack(side=BOTTOM, fill=X)
window.mainloop()