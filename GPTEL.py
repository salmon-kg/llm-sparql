#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 13:47:59 2024

@author: salman
"""

import requests
import json
import openai


openai.api_key = "PUT YOUR KEY HERE"

def gpt_query_class(label,text):
    # API endpoint - Replace with the actual API endpoint URL
    #endpoint_url = "https://api.openai.com/v1/completions"
    
    # Your API key - Replace with your actual API key
    #openai.api_key = "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"



    completion = openai.ChatCompletion.create(
        #model="gpt-3.5-turbo",
        model="gpt-4",
        #model = "gpt-4-0125-preview",
        #temperature=0.1,
        messages = [{"role": "user", "content" : f"Given the reference text below, return wikidata class label of entity '{label}' with case-sensitivity. \n Do not respond anything if not clear or reference text is not enough to identify the class. Your response should include class label only i.e. university, town, country, and city etc. \nReference Text: {text} \n Examples: \n {examples1}"}]
        )
    response = completion['choices'][0]['message']['content']
    #print(response)
    return response

def gpt_query_class1(label,text):
    # API endpoint - Replace with the actual API endpoint URL
    #endpoint_url = "https://api.openai.com/v1/completions"
    
    # Your API key - Replace with your actual API key
    #openai.api_key = "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"



    completion = openai.ChatCompletion.create(
        #model="gpt-3.5-turbo",
        model="gpt-4",
        #model = "gpt-4-0125-preview",
        #temperature=0.1,
        messages = [{"role": "user", "content" : f"Given the reference context below, return the Wikidata exact-Class label of the Entity Label  with case sensitivity. Return the class label only. \nFor 'Person' or 'Human' class, return their occupation.\nDo not respond anything if not clear or reference text is not enough to identify the class. \nEntity: {label} \nReference Text: {text} \n Examples: \n {examples1}"}]
        )
    response = completion['choices'][0]['message']['content']
    #print(response)
    return response

def gpt_query_uri(label,text):
    # API endpoint - Replace with the actual API endpoint URL
    #endpoint_url = "https://api.openai.com/v1/completions"
    
    # Your API key - Replace with your actual API key


    completion = openai.ChatCompletion.create(
        #model="gpt-3.5-turbo",
        model="gpt-4",
        #model = "gpt-4-0125-preview",
        #model="text-davinci-003",
        #temperature=0.1,
        messages = [{"role": "user", "content" : f"""Given the context information and examples below, return Wikidata ID of entity label '{label}'.\n
                     Reference Sentence = {text}\n
                     Identify the wikidata class of '{label}' based on reference sentence. 
                     Identify the correct wikidata ID of '{label}' which is an instance of identified wikidata class.\n
                     Your response should include just ID i.e, Q123456. 
                     \n Do not respond anything if not clear or reference sentenve is not enough to identify the Wikidata ID.\n
        
        
        
        Example 1: \n
          Sentence = Besides CSIRO, Australian National University is located in Canberra.\n
          Entity Label = Australian National University\n
          Wikidata Class = university\n
          Q127990
          
        \nExample 2:\n  
          Sentence = Mantell was born in Bridgwater, Somerset, and studied at the University of Bath.\n
          Entity Label = Bridgwater\n
          Wikidata Class = town\n
          Q914015
        
        """}]
        )
    response = completion['choices'][0]['message']['content']
    #print(response)
        
    return response

def gpt_query_uri1(label,text,clas):
    completion = openai.ChatCompletion.create(
        #model="gpt-3.5-turbo",
        model="gpt-4",
        #model = "gpt-4-0125-preview",
        #model="text-davinci-003",
        #temperature=0.1,
        messages = [{"role": "user", "content" : f"""Given the context information and examples below, return Wikidata ID of entity label '{label}'.\n
                     Reference Sentence = {text}\n
                     Wikidata Class = {clas}. 
                     What is the correct wikidata ID of '{label}'.\n
                     Your response should include just ID i.e, Q123456. 
                     \n Do not respond anything if not clear or reference sentenve is not enough to identify the Wikidata ID.\n
        
        
        
        Example 1: \n
          Sentence = Besides CSIRO, Australian National University is located in Canberra.\n
          Entity Label = Australian National University\n
          Wikidata Class = Q3918\n
          Q127990
          
        \nExample 2:\n  
          Sentence = Mantell was born in Bridgwater, Somerset, and studied at the University of Bath.\n
          Entity Label = Bridgwater\n
          Wikidata Class = Q3957\n
          Q914015
        
        """}]
        )
    response = completion['choices'][0]['message']['content']
    #print(response)
        
    return response

def label_check(uri):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        #model="gpt-4",
        #model = "gpt-4-0125-preview",
        #temperature=0.1,
        messages = [{"role": "user", "content" : f"Return wikidata label of Wikidata URL: {uri}."}]
        )
    response = completion['choices'][0]['message']['content']
    print(response)
    return response

prompt2 = '''Given the reference text and examples below, just return Wikidata ID of string '{Label}'\n

Reference Text: {text}\n

Example 1: \n
  Text: Besides CSIRO, Australian National University is located in Canberra.\n
  String: Australian National University\n
  Wikidata ID: Q127990\n
  
Example 2:\n  
  Text: Mantell was born in Bridgwater, Somerset, and studied at the University of Bath.\n
  String: Bridgwater\n
  Wikidata ID: Q914015\n

'''

prompt1 = '''Given the follwing referenced text, return the Wikidata ID of String. Some examples are also provided in the following.

  Text: {{text}}
  \nString:{{label}}
  \nWikidata-ID:?\n"'''    

examples =''' Example1:\n
\nText: Besides CSIRO, Australian National University is located in Canberra.\n
Entity: Australian National University\n
Class: University\n
Q127990\n

Example2:\n
Text: Mantell was born in Bridgwater, Somerset, and studied at the University of Bath.\n
Entity: Bridgwater\n
Class: Town\n
Q914015\n'''

examples1 =''' Example1:\n
\nText: Besides CSIRO, Australian National University is located in Canberra.\n
Entity: Australian National University\n
university\n

Example2:\n
Text: Mantell was born in Bridgwater, Somerset, and studied at the University of Bath.\n
Entity: Bridgwater\n
town\n
'''

# query_label = 'University of Nanking'
# query_text = "The University of Nanking (\u91d1\u9675\u5927\u5b66) was a private university in Nanjing, China"
# wikidataclass = gpt_query_class(query_label,query_text)

# # wikidataID = gpt_query_uri(query_label,query_text)

# print(wikidataclass)


def gpt_query_best_candid(entity_label,candid, query_text):
    
    
    prompt_candid = f"""I am analyzing the entity '{entity_label}'. 
            Consider the reference sentence: '{query_text}'.
            Here are the class labels and their corresponding Wikidata IDs: \n {candid}
            Based on the class labels and the context provided by the reference sentence, which Wikidata ID is the best fit for the entity '{entity_label}'?
            Please provide the single most suitable Wikidata ID for '{entity_label}' as described in the context."""
    
    completion = openai.ChatCompletion.create(
        #model="gpt-3.5-turbo",
        model="gpt-4",
        #model = "gpt-4-0125-preview",
        #temperature=0.1,
        messages = [{"role": "user", "content" : f"{prompt_candid}"}]
        )
    response = completion['choices'][0]['message']['content']
    #print(response)
    return response
    


