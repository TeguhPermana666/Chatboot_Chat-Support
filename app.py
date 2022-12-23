from flask import Flask, jsonify, render_template, request

from chat import get_response

app = Flask(__name__)


@app.get("/") #@app.route("/", methods=["GET"]) -> old methode
def index_get():
    return render_template("base.html")

#post request
@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    # TODO : CHeck if text is valid
    response = get_response(text)
    message = {"answer":response}
    return jsonify(message)


if __name__ == "__main__":
    app.run(debug=True)