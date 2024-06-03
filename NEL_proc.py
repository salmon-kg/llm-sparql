#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 14:09:46 2024

@author: salman
"""

import GPTEL
import SparqlEL

import re
import csv
import json
import os

# Path to your JSON file
file_path = './data/test.json'
P,R,F = 0,0,0
n=0
# Reading the JSON data from the file


def uri_extraction(e_label,e_class,model):
    if e_class:
        entity_uri = model(e_label, e_class)
        k=1
        while not entity_uri and k<5:
           entity_uri = model(e_label, e_class)
           k+=1
           
    else:
        entity_uri = model(e_label)
        k=1
        while not entity_uri and k<5:
           entity_uri = model(e_label)
           k+=1
           
    
    if not entity_uri:
        entity_uri = model(e_label)
        k=1
        while not entity_uri and k<5:
           entity_uri = model(e_label)
           k+=1   

def find_case_sensitive_term(text, search_term):
    # Compile a regex pattern for case-insensitive matching
    pattern = re.compile(re.escape(search_term), re.IGNORECASE)
    
    # Find all matches in the text
    matches = pattern.findall(text)
    if matches:
        return matches[0]
    else:
        return search_term

with open(file_path, 'r') as file:
    data = json.load(file)
    for content in data:
        entity_label = content['string']
        query_text = content['text']
        c_id = content['correct_id']
        #print(n,entity_label, query_text)
        n+=1
        
        entity_label = find_case_sensitive_term(query_text, entity_label)
        
        # wiki_class_label = GPTEL.gpt_query_class1(entity_label, query_text)
        
        # if wiki_class_label:
        #      wiki_class = SparqlEL.sparql_query_type(wiki_class_label)

        #      while not wiki_class and k<5:
        #         wiki_class = SparqlEL.sparql_query_type(wiki_class_label)
        #         k+=1
                
        # #print(n, entity_label, wiki_class_label, wiki_class)
        # classcheck = query_text, entity_label, wiki_class_label, wiki_class
        
        # with open(path + 'GPT4-class1-info4.csv', 'a') as file:
        #       writer = csv.writer(file, delimiter=',')
        #       writer.writerow(classcheck)
        
        
        
 #############################################################################        
      ###### SCRIPT FOR SPARQL QUERY WITH WIKIDATA CLASS OR WITHOUT CLASS
 #############################################################################      
  
        # if wiki_class:
        #     entity_uri = SparqlEL.sparql_query_uri(entity_label, wiki_class)
        #     k=1
        #     while not entity_uri and k<5:
        #         entity_uri = SparqlEL.sparql_query_uri(entity_label, wiki_class)
        #         k+=1
               
        # else:
        #     entity_uri = SparqlEL.sparql_query_type(entity_label)
        #     k=1
        #     while not entity_uri and k<5:
        #         entity_uri = SparqlEL.sparql_query_type(entity_label)
        #         k+=1
               
        entity_uri = SparqlEL.sparql_query_type_decs(entity_label)
        if not entity_uri:
            entity_uri = SparqlEL.sparql_query_type_decs(entity_label)
            k=1
            while not entity_uri and k<5:
                entity_uri = SparqlEL.sparql_query_type_decs(entity_label)
                k+=1       
        
        
        
        
 #############################################################################        
      ###### SCRIPT FOR SPARQL QUERY WITH WIKIDATA CLASS OR WITHOUT CLASS
 #############################################################################      




       
        
        
 #############################################################################       
        ##### FOR GPT URI EXTRACTION BASED ON REFERENCED INFORMATION
 #############################################################################       
 
        # if wiki_class:
        #     entity_uri = GPTEL.gpt_query_uri1(entity_label, query_text, wiki_class)
        # else:
        #     entity_uri = GPTEL.gpt_query_uri(entity_label, query_text)
        

        




        ##################################       
            ### PERFORMANCE CHECK
        ##################################
        candidates = ""
        # for item_id, classes in entity_uri:
        #     # print(f"({item_id}, {classes})")
        #     candidates = candidates + entity_label +": " + item_id + ": " + str(classes) + "\n"
        
        
        if entity_uri:
            for item_id, classes, description in entity_uri:
            # print(f"({item_id}, {classes})")
                candidates = candidates + entity_label +": " + item_id + ": " + str(classes) + ":" + str(description) +"\n"
        
        print(n, "List of Candidates:\n", candidates)
        
        
        #print(n,entity_label,c_id, entity_uri)
        if entity_uri:
            R+=1
            
        candids = n, candidates
        

print("Performance for Named Entity Mapping With Wikidata")
print (f"Total = {n}, Exact Match = {P}, Response = {R}")
print(f"Precision: {P/n}%,  Recall: {R/n},  Fmeasure: {2*P*R/(P+R)}%")
        
        
