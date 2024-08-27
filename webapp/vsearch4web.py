from flask import Flask, render_template, request, redirect
from vsearch import search4letters

app = Flask(__name__)

def log_request(req: 'flask_request', res: str)->None:
    with open('vsearch.log', 'a') as log:
        print(req.form, req.remote_addr, req.user_agent, res, file=log, sep='|')

@app.route('/')
def hello() -> 302:
    return redirect('/entry')

@app.route('/search4', methods=['POST'])   ######## page for search for letters
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    result= str(search4letters(phrase,letters))
    title = 'Here are your Results'
    log_request(request, result)
    return render_template('results.html', the_title = title, the_phrase = phrase, the_letters = letters, the_results = result)

@app.route('/entry') ####### entry page of search for letters
def entry_page() -> 'html':
    return render_template('entry.html',the_title='Welcome to search4letters on the web!')

@app.route('/viewlog')
def view_the_log()-> 'html':
    contents = []
    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(item)
    titles = ('Form Data', 'Remote Address', 'User Agent', 'Results')
    return render_template('viewlog.html', the_title = 'View Log', the_row_titles = titles, the_data = contents,)

app.run(debug=True)
