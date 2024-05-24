import turtle as t
import sys
def getdata():
    #Opens the hangman words file and reads its content
    file = open('hangman_words.txt' , 'r')
    content =file.read().split('\n')
    #Creates an empty dictionary and list to store the data
    dict_of_words={}
    current_list=[]
    count=0
    #the loop is for to check for every word and puts it in the right category
    for word in content:
        #Checks if the line is empty or not
        if word == '':
            #Store all categories names in a list
            categories = list(dict_of_words.keys())
            try:
                dict_of_words[categories[count]]=current_list
            except:
                continue
           
            count+=1
            current_list=[]
        else:
            #if the word ends with a : it means it's a category name
            if word[-1] == ':' :
                #Adds the category name as a key to the dictionary
                dict_of_words[word[0:-1].lower()]=[]
                continue
            else :
                current_list.append(word)
    return dict_of_words , categories


def check_user(user):
#returns true value if the user will resume his previous game and False if he wont

    try:
        #trying to open the file in read mode if it raise error the it doesn't exist
        user_file=open(user+'.txt','r')
        
        #checking if the file is empty or not 
        not_empty=False
        for i in user_file:
            not_empty=True

        #asking the user if he wants to continue the game if the file is not empty
        if not_empty:
          
            reply=t.textinput('Resume? yes / no',"Do you want to resume?")
            reply=reply.lower()
            
            
            if reply=='yes':
                user_file.close()
                return True
            
            elif reply=='no':
                #deletes the user previous game data
                user_file.close()
                user_file=open(user+'.txt','w')
                user_file.close()
                return False
        else:
            user_file.close()
            return False
    except FileNotFoundError :
        #if the file is not found the program creates an emty file and close it 
        user_file=open(user+'.txt','w')
        user_file.close()
        return False

#GET USER'S DATA
def import_data(user):
    #Opens user's file
    file = open(user+'.txt','r')
    #Read the file's content then splits it to the data needed
    data = file.read().rstrip().split('-')
    word= data[0]
    category=data[1]
    correct=data[2]
    wrong=data[3]
    dashess=data[4]
    
    #Making a sets to store the letters in them
    word_letters=set()
    correct_letters=set()
    wrong_letters= set()
    dashes=[]
    
    #adds letters to their corresponding set/list
    for letter in word:
        word_letters.add(letter)
        word_letters.discard(" ")
        word_letters.discard("-")
    for letter in correct:
        correct_letters.add(letter)
    for letter in wrong:
        wrong_letters.add(letter)
    for letter in dashess:
        dashes.append(letter)
    #deletes the save data from the file and then closes it
    del_file = open(user+'.txt','w')
    del_file.close()
    
    #Returns the needed data to the game
    return word, category, word_letters , correct_letters , wrong_letters, dashes

#SAVE DATA FUNCTION
def save_data(user , word, category, correct, wrong, display):
    #creates empty strings to sote the letters in them
    wrong_letters=''
    correct_letters=''
    ans='' #ans is how the word is displayed
    #Opens file to store the data
    file = open(user+'.txt','w')
    
    #converts all sets/lists to strings
    for letter in wrong:
        wrong_letters+=letter
    for letter in correct:
        correct_letters+=letter
    for letter in display:
        ans+=letter
    
    #Concatanete all strings
    data = word+'-'+category+'-'+correct_letters+'-'+wrong_letters+'-'+ans
    #Writes the data then closes the file
    file.write(data)
    file.close()



def select_category(categories,name):   # Prompts the user to enter desired category, validates the input and makes an exit console if input = "-1" , clears GUI screen after finishing
    import random as r
    t.title("Hangman: " + name)
    x=30
    t.penup()
    t.pencolor("White")
    t.hideturtle()
    t.goto(-190,270)
    t.write("Welcome " + name + "!", font=('Arial',20,'bold','underline'))
    t.goto(-200,200)
    t.write("Select from the categories", font=('Arial',15,'bold','underline'))
    t.goto(-200,170)
    for i in categories:
        t.write(i,move=False,font=('Arial',12,'normal'))
        t.penup()
        t.goto(-200,170-x)
        x+=30
    t.write("* Random",move=False,font=('Arial',11,'normal'))
    while True:
        selected=t.textinput("Enter Category:", "")
        selected=selected.lower()
        if selected in categories:
            break
        elif selected=="random":
            selected=r.choice(categories)
            break
        elif selected=="-1":
            prompt=t.textinput("Exit Or Resume","")
            prompt=prompt.lower()
            if prompt=="resume":
                pass
            elif prompt=="exit":
                t.bye()
                sys.exit()
    t.clearscreen()
    return selected

def filter_word(word):
    #returns true to break from the loop (of choosing random word) if the word meets all the criteria 

    #words from 4-8
    #words that doesn't have a repetitive letter (a letter's count>half len of word)
    #words that doesn't have j q x z y

    if len(word)<=8 and len(word)>=4:
    #1st case (word's length)

        #knowing each letter's count
        l_dict={k:0 for k in word} 
        for key in l_dict.keys():
            i=0
            for l in word:
                if key == l:
                    i+=1
            l_dict[key]=i

        #2nd case(when the word contains a letter with too many occurence)
        for value in l_dict.values(): 
            if value>=(0.5*len(word)):
                return False
        #3rd case (the word contains rare letters)
        for k in l_dict.keys():
            if k == 'z' or k =='y' or k =='q' or k =='x'or k=='j':
                return False 

        return True

    else:
        return False
    
def word(dictionary, category): # returns the word to be used in game after approving selection criteria by filter_word()
    import random as r
    approved=False
    limit=0
    while not(approved):
        word=r.choice(dictionary[category]).lower()
        #selection criteria
        approved=filter_word(word)
        # if it the program didn't choose a word randomly 8 times then the program accept the hard word (to reduce hard words accurence)
        limit+=1
        if limit>7:
            approved=True
    return word

def dashes_forming(wrd):
    # forming list of dashes the same length of the word's characters
    lst_of_dashes=[]
    for l in wrd:
        
        if l == ' ': #creating spaces if it is more than a word
            lst_of_dashes.append(' ')
        elif l == '-': #adding hyphen if the word is compound
            lst_of_dashes.append('-')
        else : 
            lst_of_dashes.append('_')
        

    return lst_of_dashes

def dashes_display(dshs,lttr,wrd):
    #updates the dashes 
    #returns true value if the entered value is in the word and false otherwise
    win=False
    index=0 
    for l in wrd:
        if l == lttr:
        #checks if the given letter is in the word 
            win=True    
            dshs[index]=lttr 
        index+=1

    return dshs,win

def check_win(correct_letters,word_letters):        #checks if the user won by counting if the set() of correct letters has number of values equal to that of set() of word letters
        if len(correct_letters)==len(word_letters):
            return True
        else:
            return False


def check_letter(l,category,wrong_letters,correct_letters,name,dashes,game_word):
    t.hideturtle()
    t.penup()
    import sys
    while True:
        l=l.lower()
        if l.isalpha() and len(l)<=1:
            # check if the entered character is one letter
            if l not in wrong_letters and l not in correct_letters:
                return l
        elif l == '-1':
           exit_console(name,game_word,category,correct_letters,wrong_letters,dashes)
        if l in wrong_letters or l in correct_letters:
            l= t.textinput("Enter another Letter","This was entered before")
        elif l =="-1":
            l= t.textinput("Enter Letter","")
        else:
            l= t.textinput("Invalid Letter","Please enter a valid letter")

def exit_console(name,game_word,category,correct_letters,wrong_letters,dashes):
        t.hideturtle()
        t.penup()
        import sys
        while True:
            reply=t.textinput('Prompt',"Do you want to exit, pause, or resume" )
            reply=reply.lower()
            if reply=='exit':
                # if the user wants to exit the game terminates 
                t.bye()
                sys.exit()
            elif reply=='pause':
                #if the user wants to pause the game saves his data and terminates 
                save_data(name,game_word,category,correct_letters,wrong_letters,dashes)
                t.bye()
                sys.exit()
            elif reply=='resume':
                
                break

def scaf0(name,category):                   #were made because when importing savefiles only the last part was drawn, so a recursive function was made to draw all the previous parts
    t.setup(1100,1000,startx=300,starty=0)
    t.bgpic("5.png")
    t.title("Hangman: "+ name + " - Category: " + category)
    t.width(4)
    t.pencolor("White")
    t.hideturtle()
    t.penup()
    t.goto(-400,380)
    t.write(name + ": "+ category, font=('Arial',18,'bold','underline'))
    t.speed(0)
    t.goto(300,-300)
    t.pendown()
    t.goto(-300,-300)
    t.goto(-300,300)
    t.goto(-250,300)
    t.goto(-300,250)
    t.goto(-300,300)
    t.goto(50,300)
    t.goto(0,300)
    t.goto(0,200)
def scaf1(name,category):
    scaf0(name,category)
    t.setheading(180)
    t.pendown()
    t.circle(30)
    t.penup()
def scaf2(name,category):
    scaf1(name,category)
    t.circle(30,180)
    t.pendown()
    t.right(90)
    t.forward(250)
    t.penup()
def scaf3(name,category):
    scaf2(name,category)
    t.left(45)
    t.pendown()
    t.forward(125)
    t.penup()
    t.backward(125)
def scaf4(name,category):
    scaf3(name,category)
    t.pendown()
    t.right(90)
    t.forward(125)
    t.backward(125)
    t.penup()
def scaf5(name,category):
    scaf4(name,category)
    t.right(135)
    t.forward(150)
    t.right(45)
    t.pendown()
    t.forward(125)
    t.penup()
    t.backward(125)
def display_hangman(chances,name,category): # Draws the parts of the hangman according to the penalties(chances) of the user. and takes name, category to draw them on the top left of the GUI
    t.hideturtle()
    t.right(180)
    t.shape("arrow")
    t.pencolor("black")
    t.title("Hangman")
    if chances==0:
        scaf0(name,category)
    elif chances==1:
        scaf0(name,category)
        t.setheading(180)
        t.speed(6)
        t.pendown()
        t.circle(30)
        t.penup()

    elif chances==2:
        scaf1(name,category)
        t.speed(7)
        t.circle(30,180)
        t.pendown()
        t.right(90)
        t.forward(250)
        t.penup()

        
    elif chances==3:
        scaf2(name,category)
        t.speed(3)
        t.left(45)
        t.pendown()
        t.forward(125)
        t.penup()
        t.backward(125)

    elif chances==4:
        scaf3(name,category)
        t.speed(3)
        t.pendown()
        t.right(90)
        t.forward(125)
        t.backward(125)
        t.penup()

    elif chances==5:
        scaf4(name,category)
        t.speed(3)
        t.right(135)
        t.forward(150)
        t.right(45)
        t.pendown()
        t.forward(125)
        t.penup()
        t.backward(125)
        

    elif chances==6:
        scaf5(name,category)
        t.speed(3)
        t.left(90)
        t.pendown()
        t.forward(125)
        t.penup()
        t.backward(125)

def again():            #prompts the user if he wants to play again after game finishes.
    t.hideturtle()
    t.penup()
    while True:
        x=t.textinput("play again?","Yes / No")
        x=x.lower()
        if x=="yes":
            return True
        elif x=="no" or x=="-1":
            return False

def enter_name():           #textbox in GUI to request name from user, and if input is "-1" exit console appears
    while True:
        name=t.textinput("Enter name","")
        if name=="-1":
            prompt=t.textinput("Exit Or Resume","")
            prompt=prompt.lower()
            if prompt=="resume":
                pass
            elif prompt=="exit":
                t.bye()
                sys.exit()
        else:
            return name

def enter_letter():                 #textbox in GUI to request letter from user
    l=t.textinput("Enter letter","")
    return l

def dialog(string,emoji,word):          #after game finishes it shows in GUI if the user lost, or won. According to the emoji and the string entered in arguments when calling function
    t.goto(-50,120)
    t.write(string,move=True,font=('Arial',20,'bold','underline'))          
    if emoji=="happy":
        t.write(" \U0001f600",move=False,font=('Arial',30,'bold'))
    else:
        t.write(" \U0001F914",move=False,font=('Arial',30,'bold'))
    t.goto(-50,70)
    t.write("The correct word is: " + word,move=True,font=('Arial',18,'bold'))  #word argument is here to write the correct word after game finishes

def game():                                 #game function, it is used to be put in main() to make the game repeat after every play
    dictionary, categories = getdata()
    for i in range(len(categories)):
        categories[i]=categories[i].lower()

    from turtle import Screen, Turtle
    screen=Screen()
    marker=Turtle()     # to make another turtle for GUI. A seperate turtle was made to clear its entries without clearing the whole GUI
    marker.hideturtle()
    t.title("Hangman")
    t.setup(1100,1000,startx=300,starty=0)
    t.bgpic("5.png")
    marker.pencolor("White")
    marker.penup()
    marker.goto(-300,180)
    marker.write("WELCOME TO HANGMAN", move=True,font=("Arial",30,"bold",'underline'))
    marker.forward(5)
    marker.left(90)
    marker.forward(2)
    marker.write(" \U0001f600", font=("Arial",40,"bold"))
    name=enter_name()
    marker.clear()
    check = check_user(name)
    if check:
        game_word ,category, word_letters, correct_letters, wrong_letters, dashes = import_data(name)

        
    else:
        category = select_category(categories,name)
        game_word= word(dictionary, category)
        word_letters=set(list(game_word))
        word_letters.discard(" ")
        word_letters.discard("-")
        dashes=dashes_forming(game_word)
        correct_letters=set()
        wrong_letters=set()
        
    PEN=6 # constant variables states the maximum number of guesses 
    return name,game_word,word_letters,dashes,correct_letters, wrong_letters,marker,PEN,category

