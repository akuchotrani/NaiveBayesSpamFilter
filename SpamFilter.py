# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 08:58:43 2018

@author: Aakash
"""
################################################################################

Dictionary_Email_Labels = {}
Dictionary_Email_Features = {}

Dictionary_Email_Predict = {}

Total_Emails = 0
Train_Probability_Spam = 0
Train_Probability_Ham = 0


################################################################################
def Read_Data(training_features_path, training_labels_path):

    global Total_Emails
    #Creating dictionary of message id and their labels from file.
    message_id = 1
    with open(training_labels_path) as File_Training_Labels:
        for line in File_Training_Labels:
            Dictionary_Email_Labels[message_id] = int(line)
            message_id = message_id + 1
            Total_Emails = Total_Emails + 1
    File_Training_Labels.close()
    
    
    #print(Dictionary_Email_Labels)
    
    with open(training_features_path) as File_Training_Features:
        for line in File_Training_Features:
            each_data_row = line.split(" ")
            
            #if the key already exists check if it belongs to ham or spam and increament the counter 
            if each_data_row[1] in Dictionary_Email_Features.keys():
                if(Dictionary_Email_Labels[int(each_data_row[0])]== 0):
                    Dictionary_Email_Features[each_data_row[1]]['ham'] += int(each_data_row[2])
                else:
                    Dictionary_Email_Features[each_data_row[1]]['spam'] += int(each_data_row[2])
                    
            #if the key is not present insert it into the dictionary        
            else:
                if(Dictionary_Email_Labels[int(each_data_row[0])]== 0):
                    Dictionary_Email_Features[each_data_row[1]] = {'spam':0,'ham':int(each_data_row[2]),'probability_spam':0.0,'probability_ham':0.0}
                else:
                    Dictionary_Email_Features[each_data_row[1]] = {'spam':int(each_data_row[2]),'ham':0,'probability_spam':0.0,'probability_ham':0.0}
                    
    File_Training_Features.close()
    
#    print(Dictionary_Email_Features)
    
    
################################################################################  
    
def Calculate_Spam_Probabilities():
    global Train_Probability_Spam,Train_Probability_Ham
    spam_messages = 0
    spam_messages = sum(Dictionary_Email_Labels.values())
    Train_Probability_Spam = spam_messages/Total_Emails
    Train_Probability_Ham = 1.0 - Train_Probability_Spam
    # print(Train_Probability_Spam)
    # print(Train_Probability_Ham)
    
    #Loop through all the keys in the dictionary and calculate the spam and ham probability
    #store it inside the dictionary itself.
    #(I am saving some space and getting constant access afterwards :) )
    

    for key in Dictionary_Email_Features:
        count_in_spam = 0
        count_in_ham = 0
        spam_probability = 0
        
        count_in_spam = Dictionary_Email_Features[key]['spam']
        count_in_ham = Dictionary_Email_Features[key]['ham']
        spam_probability = count_in_spam/(count_in_spam+count_in_ham)
        
        #similar to laplase smoothing I don't want zeros hence setting 0.01 to probability
        if(spam_probability == 0):
            spam_probability = 0.1
            
        ham_probability = 1.0 - spam_probability
        
        #print("key: ",key," count_spam: ",count_in_spam," count_ham: ",count_in_ham,"spam_probability: ",spam_probability)
        
        #storing the spam and ham probability in the key dictionary itself
        Dictionary_Email_Features[key]['probability_spam'] = spam_probability
        Dictionary_Email_Features[key]['probability_ham'] = ham_probability
    
#    print(Dictionary_Email_Features)
  
################################################################################
def Predict_Spam_Ham(pathToFeatures):
    
    Dictionary_Email_Predict.clear()
    
    
    with open(pathToFeatures) as File_Training_Features:
        for line in File_Training_Features:
            each_data_row = line.split(" ")
            
             #if the key already exists check  
            if int(each_data_row[0]) in Dictionary_Email_Predict.keys():
                Dictionary_Email_Predict[int(each_data_row[0])].append(each_data_row[1])
            else:
                Dictionary_Email_Predict[int(each_data_row[0])] = [each_data_row[1]]
        
    File_Training_Features.close()
#    print(Dictionary_Email_Predict)
    
    Result_Probability_Spam = 1
    Result_Probability_Ham = 1
    
    Result_List = []
    
    for key in Dictionary_Email_Predict:
        wordsList = Dictionary_Email_Predict[key]
        for word in wordsList:
            #check if the word is there. Sometimes in the test set there are words that were not in training data
            if word in Dictionary_Email_Features:
                
                spam_probability = Dictionary_Email_Features[word]['probability_spam']
                ham_probability = Dictionary_Email_Features[word]['probability_ham']
#            print("word: ",word," spam probability: ",spam_probability)
                Result_Probability_Spam = Result_Probability_Spam * spam_probability
                Result_Probability_Ham = Result_Probability_Ham * ham_probability
            else:
                print("word: ",word," not found during training")
            
#          probability(Spam)
#        ------------------------------- = Thus in summary if probability(Spam) > probability(Ham) then it's a spam
#        probability(Spam) + probability(Ham)
        if(Result_Probability_Spam > Result_Probability_Ham):
            print("Message: ",key,": 1"," because probability_spam: ",Result_Probability_Spam," probability_ham: ",Result_Probability_Ham)
#            Resetting the probabilities
            Result_Probability_Spam = 1
            Result_Probability_Ham = 1
            Result_List.append(1)
        else:
            print("Message: ",key,": 0"," because probability_spam: ",Result_Probability_Spam," probability_ham: ",Result_Probability_Ham)
#            Resetting the probabilities
            Result_Probability_Spam = 1
            Result_Probability_Ham = 1
            Result_List.append(0)
            
    print(Result_List)
    return Result_List
            

################################################################################
def Calculate_Accuracy(OriginalFileLabelPath,Result):
    
    correct_predictions = 0.0
    incorrect_predictions = 0.0
    
    ham_correct = 0.0
    ham_incorrect = 0.0
    spam_correct = 0.0
    spam_incorrect = 0.0

    iter_counter = 0
    with open(OriginalFileLabelPath) as File_Labels:
        for line in File_Labels:
            if(int(line) == 0 and int(Result[iter_counter]) == 0):
                ham_correct += 1.0
                correct_predictions += 1.0
            elif(int(line) == 0 and int(Result[iter_counter]) == 1):
                incorrect_predictions += 1.0
                ham_incorrect += 1.0
            
            if(int(line) == 1 and int(Result[iter_counter]) == 1):
                spam_correct += 1.0
                correct_predictions += 1.0
            elif(int(line) == 1 and int(Result[iter_counter]) == 0):
                incorrect_predictions += 1.0
                spam_incorrect += 1.0
            iter_counter += 1
            
    File_Labels.close()
    accuracy =  correct_predictions/(correct_predictions+incorrect_predictions)
    Display_Confusion_Matrix(ham_correct,ham_incorrect,spam_correct,spam_incorrect)
    return accuracy

################################################################################
    
def Display_Confusion_Matrix(ham_correct,ham_incorrect,spam_correct,spam_incorrect):
    print("----------------")
    print(ham_correct,"  ",ham_incorrect)
    print(spam_incorrect,"  ",spam_correct)
    print("----------------")
    


################################################################################
################################################################################

def main():
    
    training_features_path = 'C:\\Users\\Aakash\\Desktop\\NaiveBayesSpamFilter\\preprocdata\\train-features.txt'
    training_labels_path = 'C:\\Users\\Aakash\\Desktop\\NaiveBayesSpamFilter\\preprocdata\\train-labels.txt'

    test_features_path = 'C:\\Users\\Aakash\\Desktop\\NaiveBayesSpamFilter\\preprocdata\\test-features.txt'
    test_labels_path = 'C:\\Users\\Aakash\\Desktop\\NaiveBayesSpamFilter\\preprocdata\\test-labels.txt'

    Read_Data(training_features_path,training_labels_path)
    Calculate_Spam_Probabilities()
    Result = Predict_Spam_Ham(training_features_path)
    accuracy = Calculate_Accuracy(training_labels_path,Result)
    print("Accuracy: ",accuracy)
    
    Result = Predict_Spam_Ham(test_features_path)
    accuracy = Calculate_Accuracy(test_labels_path,Result)
    print("Accuracy: ",accuracy)

if __name__ == "__main__":
    main()