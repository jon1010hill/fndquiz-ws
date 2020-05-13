import random
import asyncio
import websockets
import os

port = os.environ.get('PORT',8765)
def convertLetterToNumber(letter):
    if(letter == 'a'):
        return 0
    if(letter == 'b'):
        return 1
    if(letter == 'c'):
        return 2

def convertNumberToLetter(number):
    if(number == 0):
        return 'a'
    if(number == 1):
        return 'b'
    if(number == 2):
        return 'c'
    
quizList = []

title = []
choices = []

title.append("What day of the week do the family meet?")
choices.append(['Friday','Wednesday','Sunday'])


title.append("What is their neighbour called?")
choices.append(['Jim','John','Joe'])


title.append("What did Jim name his dog?")
choices.append(['Wilson','Rex','Fluffy'])


title.append("What do the family call Martin's Mum?")
choices.append(['Horrible Grandma','Terrible Grandma','Grumpy Gran'])

title.append("Why does Martin take his shirt off?")
choices.append(['He is boiling','He is itchy','He is hot'])

title.append("What was stuck up the tree?")
choices.append(['Plastic bag','Coat','A Dog'])

title.append("What is it all about?")
choices.append(['Punk Rockers','The Government','Pineapples'])

title.append("How many heart attacks has Mr Morris had?")
choices.append (['3','1','A Million'])

title.append("What does Jim call corn on the cob?")
choices.append(['Crunchy Bananas','Yellow Sausages','Corny Cobs'])

title.append("What is Mike Sullivan's job?")
choices.append(['Town Planner','Locksmith','Builder'])

n = 0
score = 0
i = 0
while n < len(title) :
    
    d = dict()
    d['title'] = title[n]
    d['choices'] = choices[n]
    n += 1
    quizList.append(d)


async def echo(websocket, path):
    entry = ''
    position = 0
    awaitingAnswer = False

    while True:
         
        char = await websocket.recv()
        entry = entry + char
        if(char == "\n" or char == "\r"):
                    
            userInput = entry.lower().strip()
            entry = ''
            if(awaitingAnswer):
                if(userInput != 'a' and userInput != 'b' and userInput != 'c'):
                   await websocket.send('Please answer with A, B , or C, try again')
                   continue
                answer = convertLetterToNumber(userInput)
         
                if(possibleAnswers[answer] == questionDict['choices'][0]):
                   await websocket.send("Correct!\n\r")
                   score += 1       
                else:
                    await websocket.send("Incorrect\n\r")
                awaitingAnswer = False
                position += 1
                if(position > len(quizList) -1):
                    await websocket.send("End of quiz\n\rYou scored " + str(score) + " out of " + str(len(quizList)))
                    continue
                questionDict = quizList[position]
                possibleAnswers = questionDict['choices'].copy()  
                random.shuffle(possibleAnswers)
                await websocket.send(quizList[position]['title'] + "\n\r")
                for index in range(len(possibleAnswers)):
                  await websocket.send('Is it ' + convertNumberToLetter(index).upper() + ': ' + possibleAnswers[index] + "\n\r")
                  awaitingAnswer = True
                continue
                   
            if(userInput == 'start'):
               position = 0
               score = 0
               entry = ''
               questionDict = quizList[position]
               possibleAnswers = questionDict['choices'].copy()
               random.shuffle(possibleAnswers)
               await websocket.send(quizList[position]['title'] + "\n\r")
                        
               for index in range(len(possibleAnswers)):
                 await websocket.send('Is it ' + convertNumberToLetter(index).upper() + ': ' + possibleAnswers[index] + "\n\r")
                 awaitingAnswer = True

            


def producer():
    return 'Hello all, Shalom'

start_server = websockets.serve(echo, "0.0.0.0",port)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

    

    
score = 0
i = 0
while i < len(quizList):
    
    questionDict = quizList[i]
    print(questionDict['title'])
    possibleAnswers = questionDict['choices'].copy()
    random.shuffle(possibleAnswers)
    print("Is it A: " + possibleAnswers[0])
    print("Is it B: " + possibleAnswers[1])
    print("Is it C: " + possibleAnswers[2])
    userInput = input().lower()
    answerAsNumber = convertLetterToNumber(userInput.lower())
    if(userInput != 'a' and userInput != 'b' and userInput != 'c'):
        print('Please answer with A, B , or C, try again')
        continue
    elif(possibleAnswers[answerAsNumber].lower() == questionDict['choices'][0].lower()):
        print('Correct!')
        score = score +1
        
    else: print('Wrong!')
    print("\n")
    i += 1
# print("You scored " + str(score) + " out of " + str(len(quizList)))
    
