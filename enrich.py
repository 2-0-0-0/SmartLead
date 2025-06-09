import requests
from bs4 import BeautifulSoup
import json
import re
import ast

TOGETHER_API_KEY = "f911b02e47529b2fd90620523a399ee695074ea45ab2b3b5873df3ead8911de5"
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
TOGETHER_MODEL = "mistralai/Mistral-7B-Instruct-v0.1"

def get_text_from_url(url):
    if not url.startswith("http"):
        url = "https://" + url
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        for script in soup(["script", "style"]):
            script.decompose()
        return soup.get_text(separator="\n", strip=True)
    except Exception as e:
        return f"Error fetching website: {e}"

def enrich_lead(domain):
    website_text = get_text_from_url(domain)

    if website_text.startswith("Error"):
        return {
            "company": "N/A",
            "description": website_text,
            "score": 0
        }

    prompt = f"""
Extract the following information from the company website text provided below.
Respond in JSON format with the following keys:
- company_name
- industry
- services
- contact_info

Website content:
\"\"\"
{website_text[:4000]}
\"\"\"
"""

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": TOGETHER_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        response = requests.post(TOGETHER_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        response_json = response.json()
        content = response_json['choices'][0]['message']['content']

        try:
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if not match:
                raise ValueError("No valid JSON object found in response")
            json_str = match.group(0)
            try:
                data = json.loads(json_str)
            except json.JSONDecodeError:
                data = ast.literal_eval(json_str)
        except Exception as e:
            return {
                "company": "N/A",
                "description": f"Failed to parse JSON: {str(e)}",
                "score": 0
            }

        score = 0
        if data.get("company_name"): score += 20
        if data.get("industry"): score += 20
        if data.get("services"): score += 20
        if data.get("contact_info"): score += 20
        if len(website_text) > 1000: score += 20

        return {
            "company": data.get("company_name", "Unknown"),
            "industry": data.get("industry", "N/A"),
            "services": data.get("services", "N/A"),
            "contact_info": data.get("contact_info", "N/A"),
            "score": score
        }

    except Exception as e:
        return {
            "company": "N/A",
            "description": f"API error: {str(e)}",
            "score": 0
        }
