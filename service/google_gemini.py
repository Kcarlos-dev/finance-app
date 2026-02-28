from google import genai
from service.util.config import get_config
client = genai.Client(api_key=get_config("GEMINI_API_KEY"))

def analyze_investment_with_gemini(dados):
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=f"Imagine que vc é um consultor de investimentos e teria que avaliar se vale apena investir nessa ação com base nesse dados, lembres-se ela é apenas figurativa, seja breve e com comentários, certeiros {dados}",
    )

    return response.text