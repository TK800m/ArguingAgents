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
    similar = []
    saveCloseComm = []

    for i in range(len(easyComm)):
        test = abs(easyOP - easyComm[i])
        if test <10:
            similar =np.append(similar,easyComm[i])
            saveCloseComm = np.append(saveCloseComm,i)
           
    return (similar, saveCloseComm)
