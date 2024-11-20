from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/recherche', methods=['GET'])
def recherche_synonymes():
    # Récupérer le mot recherché à partir des paramètres de la requête
    mot = request.args.get('synonyme', '').strip()
    if not mot:
        return jsonify({"error": "Veuillez fournir un mot à chercher avec le paramètre 'synonyme'."}), 400
    
    # URL cible
    url = f"https://www.synonymo.fr/synonyme/{mot}"

    try:
        # Envoyer une requête GET au site
        response = requests.get(url)
        response.raise_for_status()  # Vérifie les erreurs HTTP

        # Analyser le contenu HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Extraire les synonymes
        synonymes = [li.text.strip() for li in soup.select(".synos li a.word")]

        # Vérifier si des synonymes ont été trouvés
        if not synonymes:
            return jsonify({"message": f"Aucun synonyme trouvé pour '{mot}'."}), 404

        return jsonify({
            "mot": mot,
            "synonymes": synonymes
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Erreur lors de la connexion au site.", "details": str(e)}), 500

# Configurer l'application pour être accessible sur Host 0.0.0.0 et le port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
