# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 08:58:43 2018

@author: Aakash
"""
################################################################################

Dictionary_Email_Labels = {}
Dictionary_Email_Features = {}

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
                    Dictionary_Email_Features[each_data_row[1]]['spam'] += 1
                else:
                    Dictionary_Email_Features[each_data_row[1]]['ham'] += 1
                    
            #if the key is not present insert it into the dictionary        
            else:
                if(Dictionary_Email_Labels[int(each_data_row[0])]== 0):
                    Dictionary_Email_Features[each_data_row[1]] = {'spam':1,'ham':0,'probability_spam':0.0}
                else:
                    Dictionary_Email_Features[each_data_row[1]] = {'spam':0,'ham':1,'probability_spam':0.0,'probability_ham':0.0}
                    
    File_Training_Features.close()
    
    print(Dictionary_Email_Features)
    
    
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
            spam_probability = 0.01
            
        ham_probability = 1.0 - spam_probability
        
        #print("key: ",key," count_spam: ",count_in_spam," count_ham: ",count_in_ham,"spam_probability: ",spam_probability)
        
        #storing the spam and ham probability in the key dictionary itself
        Dictionary_Email_Features[key]['probability_spam'] = spam_probability
        Dictionary_Email_Features[key]['probability_ham'] = ham_probability
    
    print(Dictionary_Email_Features)
  
################################################################################
def Predict_Spam_Ham():
    return
    





################################################################################
################################################################################

def main():
    
    training_features_path = 'C:\\Users\\Aakash\\Desktop\\NaiveBayesSpamFilter\\preprocdata\\train-features.txt'
    training_labels_path = 'C:\\Users\\Aakash\\Desktop\\NaiveBayesSpamFilter\\preprocdata\\train-labels.txt'

    Read_Data(training_features_path,training_labels_path)
    Calculate_Spam_Probabilities()
#    CreateMatrix()
#    PerformFeatureScaling()
#    Spit_Dataset()
#    Logistic_Regression_Gradient_Descent()
#    Predict_Results()

if __name__ == "__main__":
    main()