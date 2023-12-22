from flask import Blueprint, render_template, request, redirect, url_for, flash
import re
import pandas as pd
import pyttsx3
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier, _tree
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
import csv
import warnings
from .models import History
from . import db
import pyttsx3
import speech_recognition as sr
import os
import pyaudio
# from sqlalchemy.ext.declarative import declarative_base

upgrade = Blueprint('upgrade', __name__)
# Model = declarative_base()

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)
        print("Unable to Recognize your voice.")
        return "None"

    return query

# global sentence
warnings.filterwarnings("ignore", category=DeprecationWarning)
training = pd.read_csv('C:\\Users\MSI\Desktop\\bot chat\website\Data\Training.csv')
testing = pd.read_csv('C:\\Users\MSI\Desktop\\bot chat\website\Data\Testing.csv')
cols = training.columns
cols = cols[:-1]
x = training[cols]
y = training['prognosis']
y1 = y


reduced_data = training.groupby(training['prognosis']).max()

# mapping strings to numbers
le = preprocessing.LabelEncoder()
le.fit(y)
y = le.transform(y)


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
testx = testing[cols]
testy = testing['prognosis']
testy = le.transform(testy)


clf1 = DecisionTreeClassifier()
clf = clf1.fit(x_train, y_train)
# print(clf.score(x_train,y_train))
# print ("cross result========")
scores = cross_val_score(clf, x_test, y_test, cv=3)
# print (scores)
print(scores.mean())


model = SVC()
model.fit(x_train, y_train)
print("for svm: ")
print(model.score(x_test, y_test))

importances = clf.feature_importances_
indices = np.argsort(importances)[::-1]
features = cols


def readn(nstr):
    engine = pyttsx3.init()
    engine.setProperty('voice', "english+f5")
    engine.setProperty('rate', 130)
    engine.say(nstr)
    engine.runAndWait()
    engine.stop()


severityDictionary = dict()
description_list = dict()
precautionDictionary = dict()

symptoms_dict = {}

for index, symptom in enumerate(x):
       symptoms_dict[symptom] = index


def calc_condition():
    global num_days
    sum = 0
    exp, days = symptoms_exp, num_days
    for item in exp:
         sum = sum+severityDictionary[item]
    if(sum*days)/(len(exp)+1) > 13:
        return "You should take the consultation from doctor. "
    else:
        return "It might not be that bad but you should take precautions."


def getDescription():
    global description_list
    with open('C:\\Users\MSI\Desktop\\bot chat\website\MasterData\symptom_Description.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # line_count = 0
        for row in csv_reader:
            _description = {row[0]: row[1]}
            description_list.update(_description)


def getSeverityDict():
    global severityDictionary
    with open('C:\\Users\MSI\Desktop\\bot chat\website\MasterData\Symptom_severity.csv') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        # line_count = 0
        try:
            for row in csv_reader:
                _diction = {row[0]: int(row[1])}
                severityDictionary.update(_diction)
        except:
            pass


def getprecautionDict():
    global precautionDictionary
    with open('C:\\Users\MSI\Desktop\\bot chat\website\MasterData\symptom_precaution.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # line_count = 0
        for row in csv_reader:
            _prec = {row[0]: [row[1], row[2], row[3], row[4]]}
            precautionDictionary.update(_prec)


def getInfo():
    # print("-----------------------------------HealthCare ChatBot-----------------------------------")
    sentence: list = ["Your Name?"]
    print(sentence)
    # print("\nYour Name? \t\t\t\t", end="->")
    return sentence
    # name=input("")
    # print("Hello, ",name)

def check_pattern(dis_list, inp):
    # pred_list = []
    inp = inp.replace(' ', '_')
    patt = f"{inp}"
    regexp = re.compile(patt)
    pred_list = [item for item in dis_list if regexp.search(item)]
    if len(pred_list) > 0:
        return 1, pred_list
    else:
        return 0, []


def sec_predict(symptom_exp):
    df = pd.read_csv('C:\\Users\MSI\Desktop\\bot chat\website\Data\Training.csv')
    X = df.iloc[:, :-1]
    y = df['prognosis']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=20)
    rf_clf = DecisionTreeClassifier()
    rf_clf.fit(X_train, y_train)

    symptoms_dict = {symptom: index for index, symptom in enumerate(X)}
    input_vector = np.zeros(len(symptoms_dict))
    for item in symptom_exp:
      input_vector[symptoms_dict[item]] = 1
    return rf_clf.predict([input_vector])


def print_disease(node):
    node = node[0]
    val = node.nonzero()
    disease = le.inverse_transform(val[0])
    return list(map(lambda x: x.strip(), list(disease)))


# def extra(syms):
#     global sentence
#     sentence = syms
#     return sentence



def recurse(node, depth):
    global present_disease, symptoms_exp, length_symptoms_exp
    symptoms_present = []
    indent = "  " * depth
    print("Done")
    if tree_.feature[node] != _tree.TREE_UNDEFINED:
        # print("if")
        statement: str = "if"
        namee = feature_name[node]
        threshold = tree_.threshold[node]

        if namee == disease_input:
            val = 1
        else:
            val = 0
        if val <= threshold:
            recurse(tree_.children_left[node], depth + 1)
        else:
            symptoms_present.append(name)
            recurse(tree_.children_right[node], depth + 1)
    else:
        # print("else")
        # statement: str = "else"
        present_disease = print_disease(tree_.value[node])
        # print( "You may have " +  present_disease )
        red_cols = reduced_data.columns
        symptoms_given = red_cols[reduced_data.loc[present_disease].values[0].nonzero()]
        print("symptoms_given: ", type(symptoms_given))
        print(symptoms_given)
        # dis_list=list(symptoms_present)
        # if len(dis_list)!=0:
        #     print("symptoms present  " + str(list(symptoms_present)))
        # print("symptoms given "  +  str(list(symptoms_given)) )
        # print("Are you experiencing any ")
        l: int = 0
        symptoms_eg = "Are you experiencing any "
        # print("Ok")
        # print(list(symptoms_given))
        # list_sym_given = list(symptoms_given)
        for syms in list(symptoms_given):
            # inp=""

            # if l == 0:
            # print("if")
            symptoms_egg = symptoms_eg + "\n" + syms + "? : "
            # list_sym_given += [syms]
            symptoms_exp += [symptoms_egg]
            print("symptoms_eg: ", symptoms_egg)
            print("symptoms_exp 1: ", symptoms_exp)
            length_symptoms_exp = len(symptoms_exp)
            # print("if: ", symptoms_exp)
            # l += 1
#             else:
#                 print("else")
#                 symptoms_exp += [syms + "? : "]
# #                 print("else: ", symptoms_exp)
            # print(syms, "? : ", end='')
            # extra(syms)
    # print("statement: ", statement)
    # print("symptoms_exp: ", symptoms_exp)
    # if statement == "else":
    #     print(symptoms_exp)
    print("symptoms_exp 2: ", symptoms_exp)
    return symptoms_exp
        #     while True:
        #         # inp = input("")
        #         if inp == "yes" or inp == "no":
        #             break
        #         else:
        #             print("provide proper answers i.e. (yes/no) : ", end="")
        #     if inp == "yes":
        #         symptoms_exp.append(syms)
        # second_prediction = sec_predict(symptoms_exp)
        # print(second_prediction)
        # calc_condition(symptoms_exp, num_days)
        # if present_disease[0] == second_prediction[0]:
        #     print("You may have ", present_disease[0])
        #     print(description_list[present_disease[0]])
        #     # readn(f"You may have {present_disease[0]}")
        #     # readn(f"{description_list[present_disease[0]]}")
        # else:
        #     print("You may have ", present_disease[0], "or ", second_prediction[0])
        #     print(description_list[present_disease[0]])
        #     print(description_list[second_prediction[0]])
        #
        # # print(description_list[present_disease[0]])
        # precution_list = precautionDictionary[present_disease[0]]
        # print("Take following measures : ")
        # for i, j in enumerate(precution_list):
        #     print(i+1, ")", j)



def que_tree_to_code_4():
    global sentence
    sent = calc_condition()
    if present_disease[0] == second_prediction[0]:
        sent += "\nYou may have " + present_disease[0] + "\n" + description_list[present_disease[0]]
        # print("You may have ", present_disease[0])
        # print(description_list[present_disease[0]])
        # readn(f"You may have {present_disease[0]}")
        # readn(f"{description_list[present_disease[0]]}")
    else:
        sent = "You may have " + present_disease[0] + "or " + second_prediction[0] + "\n" + description_list[present_disease[0]] + "\n" + description_list[second_prediction[0]]
        # print("You may have ", present_disease[0], "or ", second_prediction[0])
        # print(description_list[present_disease[0]])
        # print(description_list[second_prediction[0]])
    precution_list = precautionDictionary[present_disease[0]]
    sent += "\nTake following measures : "
    # print("Take following measures : ")
    for i, j in enumerate(precution_list):
        sent += "\n" + str(int(i) + 1) + ")" + j
        # print(i + 1, ")", j)
    sentence = [sent]
    return sentence


def que_tree_to_code_3():
    global sentence, num
    # if t == 0:
    print("num: ", num)
    # if "Okay. From how many days ? : " not in sentence[0]:
    #     if num == 0:
    #         sent = sentence[0] + "\nOkay. From how many days ? : "
    #     else:
    #         sent = "Okay. From how many days ? : "
    #     sentence = [sent]
    #     return sentence
    # t += 1
    sentence = ["Okay. From how many days ? : "]
    return sentence


def que_tree_to_code_2():
    global sentence, cnf_dis, num
    # nonlocal num
    # print(conf)
    # print(cnf_dis)
    if conf == 1:
        sent = ""
        # print(num)
        for num, it in enumerate(cnf_dis):
            sent += "\n" + str(num) + ")" + it
            # print(sent)
            # print(num)
            # print(num, ")", it)
        print("num:", num)
        if num != 0:
            sent += "\n" + f"Select the one you meant (0 - {num}):  "
            # print(f"Select the one you meant (0 - {num}):  ", end="")
            # conf_inp = int(input(""))
            sentence = [sent]
            # print(sentence)
            return sentence
        else:
            global t, count
            process2()
            # t = 0
            count += 1
            senti = que_tree_to_code_3()
            sent += "\n" + senti[0]

        # disease_input = cnf_dis[conf_inp]
        # break
        # print("Did you mean: ",cnf_dis,"?(yes/no) :",end="")
        # conf_inp = input("")
        # if(conf_inp=="yes"):
        #     break
    else:
        sent = "Error Occured!"
        # print("Enter valid symptom.")
    sentence = [sent]
    return sentence


def que_tree_to_code_1():
    global sentence, name
    if name:
        sentence = [f"Hello, {name}! Enter the symptom you are experiencing"]
    else:
        sentence = ["Enter the symptom you are experiencing"]
    return sentence


def process2(conf_inp=0):
    global disease_input
    disease_input = cnf_dis[conf_inp]
    # print(disease_input)
    # sentence = ""


def process1(disease_in):
    global feature_name, conf, cnf_dis, tree_
    # print("Done")
    tree = clf
    feature_names = cols
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    # print(feature_name)
    chk_dis = ",".join(feature_names).split(",")

    conf, cnf_dis = check_pattern(chk_dis, disease_in.lower())
    # que_tree_to_code_2(conf, cnf_dis)




# def tree_to_code1(tree, feature_names):
#     tree_ = tree.tree_
#     feature_name = [
#         feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
#         for i in tree_.feature
#     ]
#
#     chk_dis = ",".join(feature_names).split(",")
#     symptoms_present = []
#
#     while True:
#         sentence = "Enter the symptom you are experiencing"
#         return sentence
#         # print("\nEnter the symptom you are experiencing  \t\t", end="->")
#         # disease_input = input("")
#         conf, cnf_dis = check_pattern(chk_dis, disease_input.lower())
#         # global disease_input
#         if conf == 1:
#             print("searches related to input: ")
#             for num, it in enumerate(cnf_dis):
#                 print(num, ")", it)
#             if num != 0:
#                 print(f"Select the one you meant (0 - {num}):  ", end="")
#                 conf_inp = int(input(""))
#             else:
#                 conf_inp = 0
#
#             disease_input = cnf_dis[conf_inp]
#             break
#             # print("Did you mean: ",cnf_dis,"?(yes/no) :",end="")
#             # conf_inp = input("")
#             # if(conf_inp=="yes"):
#             #     break
#         else:
#             print("Enter valid symptom.")
#     while True:
#         try:
#             num_days = int(input("Okay. From how many days ? : "))
#             break
#         except:
#             print("Enter valid input.")
#
#     def recurse(node, depth):
#         indent = "  " * depth
#         if tree_.feature[node] != _tree.TREE_UNDEFINED:
#             name = feature_name[node]
#             threshold = tree_.threshold[node]
#
#             if name == disease_input:
#                 val = 1
#             else:
#                 val = 0
#             if val <= threshold:
#                 recurse(tree_.children_left[node], depth + 1)
#             else:
#                 symptoms_present.append(name)
#                 recurse(tree_.children_right[node], depth + 1)
#         else:
#             present_disease = print_disease(tree_.value[node])
#             # print( "You may have " +  present_disease )
#             red_cols = reduced_data.columns
#             symptoms_given = red_cols[reduced_data.loc[present_disease].values[0].nonzero()]
#             # dis_list=list(symptoms_present)
#             # if len(dis_list)!=0:
#             #     print("symptoms present  " + str(list(symptoms_present)))
#             # print("symptoms given "  +  str(list(symptoms_given)) )
#             print("Are you experiencing any ")
#             symptoms_exp=[]
#             for syms in list(symptoms_given):
#                 # inp=""
#                 print(syms, "? : ", end='')
#                 while True:
#                     inp = input("")
#                     if inp == "yes" or inp == "no":
#                         break
#                     else:
#                         print("provide proper answers i.e. (yes/no) : ", end="")
#                 if inp == "yes":
#                     symptoms_exp.append(syms)
#             second_prediction = sec_predict(symptoms_exp)
#             # print(second_prediction)
#             calc_condition(symptoms_exp, num_days)
#             if present_disease[0] == second_prediction[0]:
#                 print("You may have ", present_disease[0])
#                 print(description_list[present_disease[0]])
#                 # readn(f"You may have {present_disease[0]}")
#                 # readn(f"{description_list[present_disease[0]]}")
#             else:
#                 print("You may have ", present_disease[0], "or ", second_prediction[0])
#                 print(description_list[present_disease[0]])
#                 print(description_list[second_prediction[0]])
#
#             # print(description_list[present_disease[0]])
#             precution_list = precautionDictionary[present_disease[0]]
#             print("Take following measures : ")
#             for i, j in enumerate(precution_list):
#                 print(i+1, ")", j)
#             # confidence_level = (1.0*len(symptoms_present))/len(symptoms_given)
#             # print("confidence level is " + str(confidence_level))
#     recurse(0, 1)


count: int = 0
# t: int = 0
num: int = 0
num_days: int = 0
conf: int = 0
disease_input: str = ""
user_message: str = ""
user_message2: str = ""
name: str = ""
# dictionary: dict = {}
yes_no: dict = {}
sentence: list = []
var: str = ""
cnf_dis: list = []
symptoms_exp: list = []
length_symptoms_exp: int = 0
symptom_exp: list = []
sent: list = []
feature_name: list = []
# list_sym_given: list = []
getSeverityDict()
getDescription()
getprecautionDict()
sentence: list = getInfo()
# tree_to_code(clf, cols)


# @upgrade.route('/')
@upgrade.route('home2')
def home2():
    # if request.method == 'POST':
    #     user_message = request.form.get('user')
    #     print(user_message)
    #     hist = History(bot=sentence, user=user_message)
    #     db.session.add(hist)
    #     db.session.commit()
    #     print(hist)
    #     return "<h1>Done</h1>"
    global count, sentence, sent, symptom_exp, second_prediction, yes_no, var
    # print("count 1: ", count)
    var = "start"
    if count == 1:
        # if user_message == "":
        #
        sentence = que_tree_to_code_1()
        var = "mid"
    elif count == 2:
        sentence = que_tree_to_code_2()
        var = "mid"
        # sentence = tree_to_code(clf, cols)
    elif count == 3:
        sentence = que_tree_to_code_3()
        var = "mid"
    elif count == 4:
        print("sentence before: ", sentence)
        sent = recurse(0, 1)
        sentence = [sent[0]]
        var = "mid"
        # sent.remove(sent[0])
        print("sentence after: ", sentence)

    elif count > 4:
        print("count 1: ", count)
        if sent != []:
            print("DOne Ha AHSA")
            sentence = [sent[0]]
            var = "mid"
            print(sentence)
            # sent.remove(sent[0])

    # elif count > 10:
        else:
            for i in yes_no:
                sym: str = i[26:len(i)-4]
                symptom_exp.append(sym)
                print("Updated symptom_exp: ", symptom_exp)
            print("Result :", symptom_exp)
            second_prediction = sec_predict(symptom_exp)
            sentence = que_tree_to_code_4()
            var = "last"
    else:
        pass
    # count += 1
    # if len(sentence) == 1:
    #     dictionary[0] = sentence
    # else:
    #     sent_count: int = 0
    #     sent_length = len(sentence)
    #     l_list = [i for i in range(sent_length)]
    #     for se in sentence:
    #         for n in l_list:
    #             dictionary[n] = se
    #             l_list.remove(n)
    #             break
    items = History.query.all()
    print("items: ", type(items))
    print("hist: ", items)
    if items:
        if len(items) > 10:
            rev = [items[i] for i in range(-10, 0, 1)]
        else:
            rev = [items[i] for i in range(-(len(items)), 0, 1)]
    else:
        rev = []
    print("reverse: ", rev)
    # speak(sentence[0])
    return render_template("upgrade.html", sentence=sentence, items=rev, var=var)


@upgrade.route('chat2', methods=['POST', 'GET'])
def chat2():
    global name, sentence, count, num, yes_no, num_days, symptom_exp, disease_input, var, sent, user_message
    if request.method == 'POST':
        user_message = request.form.get('user')
        count += 1
        # print(user_message)
        hist = History(bot=sentence[0], user=user_message)
        db.session.add(hist)
        db.session.commit()
        # print(hist)
        print(hist.user, hist.bot, hist.id)
        # print("count 2: ", count)
        print("length_symptoms_exp: ", length_symptoms_exp)
        print("int(4) + int(length_symptoms_exp): ", int(4) + int(length_symptoms_exp))
        # if (user_message.isalnum() == True) or (user_message.isdigit() == True) or (user_message.isalpha() == True):
        if all(ch.isspace() or ch.isalnum() for ch in user_message) == True:
            if count == 1:
                if all(ch.isalpha() or ch.isspace() for ch in user_message) == True:
                    name = user_message
                else:
                    count -= 1
                    flash("Enter alphabet characters only!", category="error")
            elif count == 2:
                if all(ch.isalpha() or ch.isspace() for ch in user_message) == True:
                    process1(user_message)
                    if conf != 1:
                        count -= 1
                        flash("Enter a valid symptom!", category="error")
                else:
                    count -= 1
                    flash("Use alphabets only!", category="error")
            elif count == 3:
                if num != 0:
                    print("user message: ", user_message)
                    print("type: ", type(user_message))
                    try:
                        if type(int(user_message)) == int and int(user_message) <= num and int(user_message) >= 0:
                            process2(conf_inp=int(user_message))
                        else:
                            count -= 1
                            flash(f"Please use numbers only from 0 to {num}", category="error")
                    except:
                        count -= 1
                        flash(f"Enter only numbers(0 to {num})!", category="error")
                # else:
                #     count += 1
            elif count == 4:
                try:
                    if type(int(user_message) == int) and int(user_message) >= 0:
                        num_days = int(user_message)
                    else:
                        count -= 1
                        flash("Number of days should not be in negative values!", category="error")
                except:
                    count -= 1
                    flash("Please give the input in numbers only(0-9)", category="error")

            elif count > 4 and count <= (int(4) + int(length_symptoms_exp)):
                if user_message.lower() == "yes" or user_message.lower() == "no":
                    print("count 2: ", count)
                    print("user_message: ", user_message)
                    if user_message.lower() == "yes":
                        yes_no[sentence[0]] = "yes"
                        sent.remove(sent[0])
                        print("sentence[0]: ", sentence[0])
                        print("yes_no[sentence[0]]", yes_no[sentence[0]])
                    else:
                        sent.remove(sent[0])
                else:
                    count -= 1
                    flash("Please, type only (yes/no) about experiencing...")
            elif count == (int(5) + int(length_symptoms_exp)):
                fin_val = user_message.lower()
                if fin_val == "yes":
                    print("yes vela seiyuthu....")
                    count = 1
                    num = num_days = 0
                    disease_input = var = ""
                    # dictionary: dict = {}
                    yes_no = {}
                    sentence = symptom_exp = sent = []
                    flash("Ok! Check for an another symptom...", category="success")
                    # return redirect(url_for("upgrade.home"))
                elif fin_val == "no":
                    print("poda dei...")
                    num = num_days = count = 0
                    disease_input = var = ""
                    # dictionary: dict = {}
                    yes_no = {}
                    sentence = symptom_exp = sent = []
                    sentence = getInfo()
                    flash("Take care! Get well soon...", category="success")
                    # return redirect(url_for("upgrade.home"))
                else:
                    count -= 1
                    flash("Enter a valid response - 'yes/no'", category="error")
                    # return redirect(url_for("upgrade.home"))
        else:
            count -= 1
            flash("Don\'t use any special characters!", category="error")
                # pass
            # li: list = [i for i in yes_no if yes_no[i] == "yes"]
            # for i in yes_no:
            #     if yes_no[i] == "yes":
            # if dictionary[i] == sentence[0]:
            #     sym: str = dictionary[i][25:]
            # else:
            #     sym: str = dictionary[i]
            # symptoms_exp.append(sym)
            # second_prediction = sec_predict(symptoms_exp)
        return redirect(url_for('upgrade.home'))


@upgrade.route('new_chat2')
def new_chat2():
    global num, num_days, count, disease_input, yes_no, sent, sentence, symptom_exp
    num = num_days = count = 0
    disease_input = var = ""
    # dictionary: dict = {}
    yes_no = {}
    sentence = symptom_exp = sent = []
    sentence = getInfo()
    flash("New chat started!", category="success")
    return redirect(url_for("upgrade.home"))


@upgrade.route('clear2')
def clear2():
    global num, num_days, count, disease_input, yes_no, sent, sentence, symptom_exp
    if History:
        num = num_days = count = 0
        disease_input = var = ""
        # dictionary: dict = {}
        yes_no = {}
        sentence = symptom_exp = sent = []
        sentence = getInfo()
        msg = History.query.all()
        for i in msg:
            db.session.delete(i)
        # db.session.query(Model).delete
        db.session.commit()
        flash("All conversations deleted successfully!", category="success")
    else:
        flash("There is no conversation to delete!", category="error")
    return redirect(url_for("upgrade.home"))


# @upgrade.route('upgrade')
# def upgrade():
#     return render_template("")
