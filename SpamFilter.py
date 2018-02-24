# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 08:58:43 2018

@author: Aakash
"""

import numpy as np

################################################################################

Dictionary_Email_Labels = {}

Train_Probability_Spam = 0
Train_Probability_Ham = 0


################################################################################
def Read_Data(training_features_path, training_labels_path):

    
    #Creating dictionary of message id and their labels from file.
    message_id = 1
    with open(training_labels_path) as File_Training_Labels:
        for line in File_Training_Labels:
            Dictionary_Email_Labels[message_id] = int(line)
            message_id = message_id + 1
            
    File_Training_Labels.close()
    
    print(sum(Dictionary_Email_Labels.values()))
    
    
    
    
    

    

    
    
    
    







################################################################################
################################################################################

def main():
    
    training_features_path = 'C:\\Users\\Aakash\\Desktop\\NaiveBayesSpamFilter\\preprocdata\\train-features.txt'
    training_labels_path = 'C:\\Users\\Aakash\\Desktop\\NaiveBayesSpamFilter\\preprocdata\\train-labels.txt'

    Read_Data(training_features_path,training_labels_path)
#    CreateMatrix()
#    PerformFeatureScaling()
#    Spit_Dataset()
#    Logistic_Regression_Gradient_Descent()
#    Predict_Results()

if __name__ == "__main__":
    main()