import requests
import json
import GPTEL
from GPTEL import gpt_query_class
from collections import defaultdict
import re

# Define the SPARQL query
endpoint_url = "https://query.wikidata.org/sparql"
headers = {"Accept": "application/sparql-results+json"}


def sparql_query_type(label):
    sparql_q1 = 'SELECT ?entity ?type ?typeLabel ?subclassLabel WHERE {?entity rdfs:label \"'+label+'\"@en . OPTIONAL { ?entity wdt:P31 ?type .} OPTIONAL {?entity wdt:P279 ?subclass.} FILTER (!bound(?type) || ?type != wd:Q4167410) SERVICE wikibase:label { bd:serviceParam wikibase:language "en".} }'
    
    sparql_q2 = 'SELECT ?entity ?type ?typeLabel ?entityDescription ?subclassLabel WHERE {?entity rdfs:label \"'+label+'\"@en . OPTIONAL { ?entity wdt:P31 ?type .} OPTIONAL {{ ?entity schema:description ?entityDescription. FILTER(LANG(?entityLabel) = "en") }} FILTER (!bound(?type) || ?type != wd:Q4167410) SERVICE wikibase:label { bd:serviceParam wikibase:language "en".} }'
    
    entity_uri = ''

    sparql_q4 ='SELECT ?entity ?classLabel ?subclassLabel WHERE {?entity rdfs:label /"'+label+'/"@en; wdt:P31 ?class. OPTIONAL {?class wdt:P279 ?subclass.} SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } } limit 10'

    response = requests.get(endpoint_url, headers=headers, params={'query': sparql_q1, 'format': 'json'})
    items_with_classes = defaultdict(list)
    # Process the response
    if response.ok:
        data = response.json()
        for result in data['results']['bindings']:
            #print(result)
            
            
            entity_uri = result['entity']['value'].split('/')[-1]
            type_label = result.get('typeLabel')
            subclass = result.get('subclassLabel')
            type_uri = ''
            class_uri = ''
            
            if type_label:
                type_uri = result['typeLabel']['value']
            
            if subclass:
                class_uri = result['subclassLabel']['value']
                
            #info = entity_uri #, type_uri
            if type_uri !='':
                items_with_classes[entity_uri].append(type_uri)
                
            if class_uri != '':
                items_with_classes[entity_uri].append(class_uri)
            
            
        return [(entity_uri, classes) for entity_uri, classes in items_with_classes.items()]   


def sparql_query_type_decs(label):

    sparql_q1 = 'SELECT ?entity ?type ?typeLabel ?entityDescription ?subclassLabel WHERE {?entity rdfs:label \"'+label+'\"@en . OPTIONAL { ?entity wdt:P31 ?type .} OPTIONAL {{ ?entity schema:description ?entityDescription. FILTER(LANG(?entityLabel) = "en") }} FILTER (!bound(?type) || ?type != wd:Q4167410) SERVICE wikibase:label { bd:serviceParam wikibase:language "en".} } limit 10'
    
    entity_uri = ''

    response = requests.get(endpoint_url, headers=headers, params={'query': sparql_q1, 'format': 'json'})
    items_with_classes = defaultdict(list)
    items_with_descr = defaultdict(list)
    # Process the response
    if response.ok:
        data = response.json()
        for result in data['results']['bindings']:
            #print(result)
            
            
            entity_uri = result['entity']['value'].split('/')[-1]
            type_label = result.get('typeLabel')
            subclass = result.get('subclassLabel')
            desc = result.get('entityDescription')
           
            type_uri = ''
            class_uri = ''
            descr = ''
            
            if type_label:
                type_uri = result['typeLabel']['value']
            
            if subclass:
                class_uri = result['subclassLabel']['value']
            
            if desc:
                descr = result['entityDescription']['value']
                

            if type_uri !='':
                items_with_classes[entity_uri].append(type_uri)
                
            if class_uri != '':
                items_with_classes[entity_uri].append(class_uri)
            
            if descr != '':
                if entity_uri not in items_with_descr or not items_with_descr[entity_uri]:
                    items_with_descr[entity_uri].append(descr)
                    
        return [(entity_uri, classes, items_with_descr[entity_uri]) for entity_uri, classes in items_with_classes.items()]      

def sparql_query_entity_uri(label):
    sparql_q1 = 'SELECT ?entity WHERE {?entity rdfs:label \"'+label+'\"@en . OPTIONAL { ?entity wdt:P31 ?type .} FILTER (!bound(?type) || ?type != wd:Q4167410)} limit 1'
    
    # Query with Ranking IDs based on sitelinkCount to select the popular one
    sparql_q2 = f"""SELECT ?entity (COUNT(?sitelink) AS ?sitelinkCount) WHERE {{
                  {{SELECT ?entity WHERE {{?entity rdfs:label "{label}"@en .  }}
                  }}
                  OPTIONAL {{ ?entity schema:about ?sitelink . 
                             ?sitelink schema:isPartOf [ a wikibase:Sitelink ] .
                           }}
                }} GROUP BY ?entity
                ORDER BY ASC(?sitelinkCount)
                limit 1
                """
    entity_uri = ''
    # Query for Disambiguation Restriction and Condition of Wikipedia page
    sparql_q3 = f"""
                SELECT ?entity WHERE {{
                  ?entity rdfs:label "{label}"@en .
                  FILTER NOT EXISTS {{ ?entity wdt:P31 wd:Q4167410 . }}
                  ?article schema:about ?entity ;
                           schema:isPartOf <https://en.wikipedia.org/> .
                }}
                """
        
    response = requests.get(endpoint_url, headers=headers, params={'query': sparql_q1, 'format': 'json'})
     
     # Process the response
    if response.ok:
        data = response.json()
        for result in data['results']['bindings']:
             entity_uri = result['entity']['value'].split('/')[-1]
             #if entity_uri==uri:
             #print(f"Entity URI: {entity_uri}")
                 #return entity_uri
             
             return entity_uri
         
            
def sparql_query_type_uri(label,clas):
    sparql_q1 = 'SELECT ?entity WHERE {?entity rdfs:label \"'+label+'\"@en . OPTIONAL { ?entity wdt:P31 ?type .} FILTER (!bound(?type) || ?type != wd:Q4167410)} limit 1'
    
    sparql_uri = 'SELECT ?entity ?entityLabel WHERE {?entity wdt:P31 wd:'+clas+'; rdfs:label \"'+ label + '\"@en. SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }} limit 1'
    
    if clas:
        sparql_q = sparql_uri
        
    else:
        sparql_q = sparql_q1
        
    response = requests.get(endpoint_url, headers=headers, params={'query': sparql_q, 'format': 'json'})
     
     # Process the response
    if response.ok:
        data = response.json()
        for result in data['results']['bindings']:
             entity_uri = result['entity']['value'].split('/')[-1]
             #if entity_uri==uri:
             #print(f"Entity URI: {entity_uri}")
                 #return entity_uri
             
             return entity_uri
        
def sparql_query_uri(label,clas):
    #print(clas)
    #q1 = f"?entity wdt:P31 wd:{clas};"
    #print(q1)
    sparql_uri = 'SELECT ?entity ?entityLabel WHERE {?entity wdt:P31 wd:'+clas+'; rdfs:label \"'+ label + '\"@en. SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }} limit 1'
    #print(sparql_uri)

    # Perform the request
    response = requests.get(endpoint_url, headers=headers, params={'query': sparql_uri, 'format': 'json'})

    # Process the response
    if response.ok:
        data = response.json()
        for result in data['results']['bindings']:
            entity_uri = result['entity']['value'].split('/')[-1]
            #print(f"Entity URI: {entity_uri}")
            return entity_uri

def sparql_query_uri_label(label,clas):
    #print(clas)
    #q1 = f"?entity wdt:P31 wd:{clas};"
    #print(q1)
    sparql_uri = 'SELECT ?entity ?entityLabel WHERE {?entity wdt:P31 wd:label \"'+clas+'\"@en; rdfs:label \"'+ label + '\"@en. SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }} limit 1'
    #print(sparql_uri)

    # Perform the request
    response = requests.get(endpoint_url, headers=headers, params={'query': sparql_uri, 'format': 'json'})
    print(response)
    # Process the response
    if response.ok:
        data = response.json()
        for result in data['results']['bindings']:
            entity_uri = result['entity']['value']
            print(f"Entity URI: {entity_uri}")
            return entity_uri
        
def sparql1_func(x):
    txt = str(x)
    querytype =('SELECT distinct ?item ?itemLabel ?type WHERE{ ?item ?label \"'+txt+
                    '\"@en. ?item wdt:P31 ?type. ?article schema:about ?item . ?article schema:isPartOf '
                    '<https://en.wikipedia.org/>. SERVICE wikibase:label '
                    '{ bd:serviceParam wikibase:language \"en\". } }')

    response = requests.get(endpoint_url, headers=headers, params={'query': querytype, 'format': 'json'})
    if response.ok:
        data = response.json()
        print(data)
        for result in data['results']['bindings']:
            entity_uri = result['entity']['value']
            print(f"Entity URI: {entity_uri}")
        
        
            return entity_uri

        #quri = results_df[['item.value']]
        #uri = quri.iloc[0]["item.value"]

        #qtype = results_df[['type.value']]
        #uritype = qtype.iloc[0]["type.value"]

        #return(uri,uritype)



def extract_wikidata_id(url):
    if url:
        return url.rsplit('/', 1)[-1]
    else:
        return


#entity_label = ""  # Example label variable
# #class_label= "university"
# #class_id1 = "Q3918"  # Example class ID for cities

#print (sparql_query_type(entity_label))
# query_text = "The University of Nanking (\u91d1\u9675\u5927\u5b66) was a private university in Nanjing, China"

# class_label = gpt_query_class(entity_label, query_text)
# print(class_label)

# class_url= sparql_query_type(class_label.lower())
# class_id= extract_wikidata_id(class_url)
# print(class_id)

# if class_id:
#     entity_url = sparql_query_uri(entity_label, class_id)
#     entity_id= extract_wikidata_id(entity_url)
#     if not entity_id:
#         entity_url = sparql_query_type(entity_label)
#         entity_id= extract_wikidata_id(entity_url)
# else:
#     entity_url = sparql_query_type(entity_label)
#     entity_id= extract_wikidata_id(entity_url)
    
# print(entity_id)







