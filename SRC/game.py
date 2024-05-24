import sys
import hangman_functions as fn
from turtle import Screen, Turtle
import turtle as t
t.hideturtle()

def main():
    while True:
        j=1
        name, game_word,word_letters,dashes,correct_letters, wrong_letters,marker,PEN,category=fn.game()        #to start game again
        t.setup(1100,1000,startx=300,starty=0)      #to adjust screen size
        t.bgpic("5.png")
        scr=Screen()
        mark=Turtle()
        mark.hideturtle()
        mark.penup()
        while True:
            marker.goto(120,-50)
            mark.goto(120,-150)
            mark.pencolor("White")
            fn.display_hangman(len(wrong_letters),name,category)            #draws hangman according to penalties (the set of wrong letters)
            marker.clear()
            marker.write('  '.join(dashes),move=False,font=('Arial',14,'bold'))
            if j==1:
                if len(wrong_letters)!=0:
                    mark.goto(120,-150)
                    mark.pencolor("red")
                    mark.write("Wrong letters are:  ",move=True,font=('Arial',13,'bold'))
                    mark.write(', '.join(wrong_letters),move=False,font=('Arial',13,'bold'))
                else:
                    mark.goto(120,-150)
                    mark.write("No wrong letters yet.",move=False,font=('Arial',13,'bold'))
                j=2
            letter = fn.enter_letter()
            letter = fn.check_letter(letter,category,wrong_letters,correct_letters,name,dashes,game_word)
            mark.clear()
            dashes,win=fn.dashes_display(dashes,letter,game_word)
            marker.clear()
            marker.write('  '.join(dashes),move=False,font=('Arial',14,'bold'))
            
            if win :
                correct_letters.add(letter)
            else:
                wrong_letters.add(letter)
                
            if len(wrong_letters)!=0:
                mark.goto(120,-150)
                mark.pencolor("red")
                mark.write("Wrong letters are:  ",move=True,font=('Arial',13,'bold'))
                mark.write(', '.join(wrong_letters),move=False,font=('Arial',13,'bold'))
            else:
                mark.goto(120,-150)
                mark.write("No wrong letters yet.",move=False,font=('Arial',13,'bold'))
                
            if fn.check_win(correct_letters,word_letters): # checks if user won
                t.clear()
                mark.clear()
                marker.clear()
                fn.dialog("Winner!! ","happy",game_word)
                returned=fn.again() # asks if he wants to play again, if yes returns to game() in line 11 ,  if not closes game
                if returned==False:
                    t.bye()
                    sys.exit()
                else:
                    t.clear()
                    break
                
            elif len(wrong_letters)>=PEN: #checks if user lost, if set of wrong letters are more than the max penalty then the user lost game.
                fn.display_hangman(6,name,category)
                t.clear()
                mark.clear()
                marker.clear()
                fn.dialog("You lost ","sad",game_word)
                returned=fn.again() # asks if he wants to play again, if yes returns to game() in line 11 ,  if not closes game
                if returned==False:
                    t.bye()
                    sys.exit()
                else:
                    t.clear()
                    break

main()
