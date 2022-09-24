from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"

@app.route('/')
def survey_home():

    return render_template("start_survey.html", survey=survey)


@app.route("/start", methods=["POST"])
def start_survey():

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")


@app.route("/questions/<int:qid>")
def show_question(qid):
    """Shows the current question"""
    responses = session.get(RESPONSES_KEY)

    if responses is None:
        """ sends back to the home page if the user tries to access the quesiton page before clicking start"""
        return redirect("/")
    
    if len(responses) == len(survey.questions):
        """once all questions have been answered, send them to the completed page """
        return redirect("/complete")

    if len(responses) != qid:
        """an message will display if the user attempts to skip ahead or enter an invalid question number"""
        flash(f"Invalid question number: {qid}")
        return redirect(f"/questions/{len(responses)}")
       
    question = survey.questions[qid]
    return render_template("question.html", question_num=qid, question=question)


@app.route('/answer', methods=["POST"])
def question_response():

    # adds the answer to the response list
    choice = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if len(responses) == len(survey.questions):
        """confirms all questions have been answered and sends them to the completion page"""
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/complete")
def completed():
    """Survey has been completed, display completion page"""
    return render_template("completed.html")