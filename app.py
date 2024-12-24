from flask import Flask, render_template, request, jsonify




app = Flask(__name__)


# Home Page
@app.route("/", methods=["POST", "GET"])
def index():
    return render_template('index.html')





# Runner
if __name__ in '__main__':
    app.run(debug=True)