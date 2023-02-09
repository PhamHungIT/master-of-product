import pandas as pd
from fuzzywuzzy import fuzz
from elasticsearch import Elasticsearch, helpers
import csv
import requests

'''
This function analyze the dataset and create a unique value list for every useful attribute, return the matrix of atrribute value list
'''

def analyzeData():
    # Import dataset laptop
    docs = pd.read_csv('static/data/data.csv')
    # Create unique value lists for every useful attribute
    brands = docs['brand'].unique()
    products = docs['name'].unique()
    docs['scrsize'] = docs['scrsize'].apply(lambda x: str(x))
    inches = docs['scrsize'].unique()
    cpus = docs['cpu'].unique()
    cpu_brands = docs['cpu_brand'].unique()
    # docs['ram'] = docs['ram'].apply(lambda x: str(x).strip() + 'GB')
    rams = docs['ram'].unique()
    # docs['memory'] = docs['memory'].apply(lambda x: str(x).strip() + 'GB SSD')
    memories = docs['memory'].unique()
    gpus = docs['gpu'].unique()
    gpu_brands = docs['gpu_brand'].unique()
    opsys = docs['opersystem'].unique()
    # Create attribute unique value matrix
    attrs = [brands, products, inches, cpus, cpu_brands, rams, memories, gpus, gpu_brands, opsys]
    return attrs

# Create a list of attribute names maintained, so that we know which attribute we find out when iterating through the terms
attrsNames = ["brand", "name", "scrsize",
              "cpu", "cpu_brand", "ram", "memory", "gpu", "gpu_brand", "opersystem"]

'''
The Core function to analyze the query, takes 2 params, attribute unique value matrix and text query
Check what kind of attributes are covered in the query, query is a splited list of query words
I use fuzz module to match the term with every list of values, keep the average score
Finally the attribute list that gets the highest score would mostly likely be the atrribute that this value matches
Return a dictionary that store the matched attribute as key and term as value for search use later
'''

def detectAttr(attrs, query):
    """
    
    Args:
        attrs: (list of str) attributes 
    
    """
    query = query.split()
    # The returned value
    searchQuery = {}
    # Match every term in the query with the matrix of unique values
    for term in query:
        # Iterate through every atrribute value list except for weight and price which people often use adjectives
        attrScores = []
        for i in range(len(attrs)):
            # Call the function matchTitle to see if the term is contained in the list
            avgScore = matchTitleScore(term, attrs[i])
            attrScores.append(avgScore)
        # Get the index of the most matched attribute
        idx = attrScores.index(max(attrScores))
        # Store the term as value and attribute as key for later use when searching
        if attrsNames[idx] in searchQuery:
            searchQuery[attrsNames[idx]] += " " + term
        else:
            searchQuery[attrsNames[idx]] = term
    
    return searchQuery

'''
Function called by detectAttr to calculate the average score of a term is similar to values in the unique value list, add fuzziness to tolerant spelling error
Return the avarage score of fuzz match
'''
def matchTitleScore(term, attrs):
    scores = []
    for i in attrs:
        # return 100 if got a complete match
        if fuzz.token_set_ratio(term, i) == 100:
            return 100
        # otherwise calculate the average for scores
        scores.append(fuzz.token_set_ratio(term, i))
    return sum(scores)/len(scores)

'''
elasticsearch object class 
'''
class ElasticObj:
    def __init__(self, index_name, index_type):
        self.index_name = index_name
        self.index_type = index_type
        self.es = Elasticsearch('https://localhost:9200', verify_certs=False, http_auth=('elastic', 'lgQvfhqlWQjH*78GaSzA'))

    '''
    Main function that import data from csv file and adding documents to elastic index
    '''
    def importData(self, filename):
        with open(filename, encoding='ISO-8859-1') as f:
            reader = csv.DictReader(f)
            helpers.bulk(self.es, reader, index=self.index_name)

    '''
    Function that handles search queries, do a most_fields search 
    '''
    def search(self, query, attr):
        # query doc, most fields search
        subLst = []

        lstQuery = []
        for key, val in attr.items():
            subDct = {}
            subDct[key] = val
            subLst.append(subDct)
        for item in subLst:
            dct = {}
            dct['match'] = item
            lstQuery.append(dct)

        doc = {
            "size": 30,
            "query": {
                "bool": {
                    "should": lstQuery
                }
            }}

        res = self.es.search(index=self.index_name, body=doc)
        return res


if __name__ == "__main__":

    # Run a analysis for the data, collect information for analyze query
    attrs = analyzeData()
    # Check connection
    # requests.get('http://localhost:9200')
    # Create elastic search object and build index
    obj = ElasticObj("my_index", "docs")
    obj.importData('static/data/data.csv')