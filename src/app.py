import elasticsearch_model.search_model as SearchModel
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def index():
   return render_template('index.html')

@app.route('/search.html', methods = ['POST', 'GET'])
def search():
   if request.method == 'POST':
      query = request.form['query']
      # Call the detectAttr to analyze the query
      searchQuery = SearchModel.detectAttr(SearchModel.attrs, query)
      # Get the list of matched attribute titles
      fields = list(searchQuery.keys())
      # Get the new query string that has filtered out the attribute titles
      text = " ".join(list(searchQuery.values()))
      # Call the search method to retrieve docs based on new query and matched fields
      res = SearchModel.obj.search(text, searchQuery)

      dct = {}
      for doc in res['hits']['hits']:
         dct[doc['_source']['name']] = doc['_source']

      print(query)
      print("Located attributes: " + " ".join(fields))
      corresponding_attributes = ", ".join(fields)
      print(dct)
      no_results = len(dct)
      return render_template('search.html', query = query, results = dct, no_results = no_results,
            corresponding_attributes=corresponding_attributes)

   if request.method == 'GET':
      return render_template('search.html')

@app.route('/about.html')
def about():
   return render_template('about.html')

@app.route('/data.html')
def data():
   return render_template('data.html')

@app.route('/references.html')
def references():
   return render_template('references.html')

if __name__ == '__main__':
   app.run(debug=True)