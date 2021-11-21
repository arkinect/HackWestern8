# imports and setup
from flask import Flask, render_template
import main
app = Flask(__name__)

# testing shit
# print(main.main(100, "victoria hospital"))

#calling a template and creating a webpage
@app.route("/")
def inputPage():
    return render_template("index.html")



@app.route("/output")
def outputPage():
    return render_template("output.html", output=main.main(100, "victoria hospital"))




# closing out
if __name__ == "__main__":
    app.run(debug=True)
