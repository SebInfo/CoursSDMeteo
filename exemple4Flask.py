from flask import Flask, request

app = Flask(__name__)

@app.route("/meteo", methods=["POST"])
def meteo_post():
    ville = request.form.get("ville")
    temperature = request.form.get("temp")

    return f"Donnée reçue : {ville}, {temperature} °C"

if __name__ == "__main__":
    app.run(debug=True)