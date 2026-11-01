"""AI analysis module for MoroccoDataHub."""

import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY introuvable dans .env")

client = Groq(api_key=api_key)


def analyze_dataset(dataset):
    prompt = f"""
    Tu es un expert en ingénierie des données.
    Analyse les métadonnées de ce dataset marocain.

    Titre : {dataset.get("title")}
    Description : {dataset.get("description")}
    Source : {dataset.get("source")}

    Retourne uniquement un JSON valide avec ces champs :
    {{
        "category": "demography, economy, education, employment,
                     agriculture, finance, health, transport ou other",
        "subcategory": "sous-catégorie",
        "country": "Morocco",
        "geographic_level": "national, regional, provincial,
                             communal ou unknown",
        "year": null,
        "summary": "résumé en une phrase",
        "relevance_score": 0.0
    }}

    Règles :
    - N'invente aucune information.
    - Si l'année est inconnue, retourne null.
    - relevance_score doit être entre 0 et 1.
    - Utilise uniquement les informations fournies.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "Tu es un assistant spécialisé dans la découverte et la classification des données."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
        response_format={"type": "json_object"}
    )

    result = json.loads(response.choices[0].message.content)

    dataset["ai_analysis"] = result
    dataset["discovery_method"] = "groq_llm"

    return dataset
