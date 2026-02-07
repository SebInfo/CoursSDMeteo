from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Page d'accueil"

@app.route("/about")
def about():
    return "À propos de l'application"

@app.route("/contact")
def contact():
    return "Page de contact"

@app.route("/user/<name>")
def user(name):
    return f"Bonjour {name}"

if __name__ == "__main__":
    app.run(debug=True)
