
from flask import Flask, redirect, render_template, request, session, flash
from flask_session import Session

from flask_bootstrap import Bootstrap4

app = Flask(__name__)

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.route('/', methods=['POST', 'GET'])
def homepage():
    return render_template('home_page.html')


@app.route('/process', methods=['GET'])
def process_inputs():
    field = request.args.get('field')
    courses = request.args.getlist('course')  # handles multiple 'course' inputs
    # Now use `field` and `courses` in your ML model

    # The putput of the model is going to be in summaries
    summaries = [
        {"title": "ML in Production: Challenges & Wins", "summary": "Deploying ML models can be complex..."},
        {"title": "Top 5 ML Frameworks in 2025", "summary": "PyTorch and TensorFlow continue to dominate..."},
        {"title": "How to Break into ML", "summary": "Build projects, learn Python, and understand math fundamentals..."},
    ]
    return render_template("trending.html", summaries=summaries)


if __name__ == '__main__':  # run the app
    app.run(debug=True)
    print("Flask app is running...")

