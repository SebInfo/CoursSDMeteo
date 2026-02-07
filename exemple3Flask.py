from flask import Flask, request

app = Flask(__name__)

@app.route("/meteo")
def meteo():
    # Récupération des paramètres GET
    ville = request.args.get("ville", "inconnue")
    temperature = request.args.get("temp", type=float)
    pluie = request.args.get("pluie", default="non")

    # Construction de la réponse
    if temperature is None:
        return "Température non fournie"

    return (
        f"Météo à {ville} : "
        f"{temperature} °C, "
        f"pluie : {pluie}"
    )

if __name__ == "__main__":
    app.run(debug=True)
