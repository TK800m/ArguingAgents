from textstat.textstat import textstat
import numpy

def flesch_kincaid_comm(text):
	flesch_kincaid = []
	for i in range(len(text)):
	    flesch_kincaid.append(textstat.flesch_kincaid_grade(text[i]))
	return(flesch_kincaid)

def flesch_ease_comm(text):
	flesch_ease = []
	for i in range(len(text)):
	    flesch_ease.append(textstat.flesch_reading_ease(text[i]))
	return(flesch_ease)

def flesch_kincaid_OP(text):
	flesch_kincaid = textstat.flesch_kincaid_grade(text)
	return(flesch_kincaid)

def flesch_ease_OP(text):
	flesch_ease = textstat.flesch_reading_ease(text)
	return(flesch_ease)

def similarEase(easyOP, easyComm, CommentText, commentName):
    closest = [0,0,0,0,0,0,0,0,0,0]
    saveCloseComm = closest
    closest[0] = abs(easyOP - easyComm[0])

    for i in range(len(easyComm)):
        test = abs(easyOP - easyComm[i])
        for x in range(len(closest)):
            if x+1 < len(closest) and closest[x+1] == 0:
                closest[x+1] = test
                saveCloseComm[x+1]= i
                break
            elif OPname != commentName[i] and closest[x] > test:
                closest[x] = test
                saveCloseComm[x] = i
                break

    for i in range(len(saveCloseComm)):
        print("--------------------------------------------------------------------------------\n")
        print("OP's ease: "+str(easyOP) +" versus comment ease: "+str(easyComm[saveCloseComm[i]]))
        print(CommentText[saveCloseComm[i]])
        print(commentName[saveCloseComm[i]] + "\n")

    return(closest, saveCloseComm)

