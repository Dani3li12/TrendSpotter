from flask import Flask, redirect, render_template, request, session, flash
from flask_session import Session
from search_linkedin_posts import search_posts
from summerizer_title_time_ import process_texts
import time

app = Flask(__name__)

# Flask session configuration
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('home_page.html')
#

@app.route('/process', methods=['GET'])
def process_inputs():
    field = request.args.get('field')
    courses = request.args.getlist('course')

    # Store inputs in session
    session['field'] = field
    session['courses'] = courses

    # Search and summarize posts
    posts = search_posts(field, courses)
    texts = process_texts(posts)

    summaries = []

    while len(summaries) < 3 :
        if len(texts) >= 3:
            summaries = [
                {"title": texts[0]['title'], "summary": texts[0]['summary'], "reading_time_minutes": texts[0]['reading_time_minutes']},
                {"title": texts[1]['title'], "summary": texts[1]['summary'], "reading_time_minutes": texts[1]['reading_time_minutes']},
                {"title": texts[2]['title'], "summary": texts[2]['summary'], "reading_time_minutes": texts[2]['reading_time_minutes']},
            ]
        else:
            time.sleep(0.2)  # Wait briefly before checking again

    # If still not enough, show fallback message or empty list
    if len(summaries) < 3:
        flash("Couldn't retrieve enough results. Try again.")
        return redirect("/")

    return render_template("trending.html", summaries=summaries)

if __name__ == '__main__':
    app.run(debug=False)


