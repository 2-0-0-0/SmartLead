SmartLead – AI-Powered Lead Quality Intelligence Tool
Caprae Capital AI Readiness Pre-Screening Challenge Submission

SmartLead is a next-generation lead intelligence tool developed within a strict 5-hour challenge window. It empowers businesses to move beyond traditional lead scraping by offering a robust system to search, enrich, validate, and score leads using web intelligence and generative AI models. Tailored for sales enablement and strategic outreach, SmartLead bridges the gap between raw data and actionable insight.

Key Features:

1.Domain + Location Based Search
                   Uses [SerpAPI] to fetch relevant company websites based on user-defined domain and location keywords. We parse top-ranked organic Google search results to prioritize relevance and visibility.

2. Company Enrichment via Together.ai
                    We utilized Together.ai’s Mistral-7B model to extract structured information such as:

                               Company Name

                               Industry

                               Services/Products Offered

                               Contact Information

                               Though powerful, this method faced limitations due to non-uniform website structures. We flag this as a point for future enhancement (see below).

 Export: Users can export enriched lead data as a CSV for further analysis or CRM integration.

3. Fake Website Detection (Heuristic)

To filter out non-genuine or low-quality leads, we implemented:

SSL (HTTPS) check

Presence of Contact Us / About Us sections

Domain age and trust-based keywords (e.g., "established", "clients", "partners")

Minimum meaningful text threshold

4. Lead Scoring
Each company is assigned a score out of 100 based on the quality and completeness of extracted metadata, helping users prioritize their outreach efforts.

Tech Stack Overview:

Area	Tools / Libraries
Frontend	Streamlit – rapid UI deployment
Scraping	requests, BeautifulSoup, SerpAPI
LLM Enrich	Together.ai (Mistral-7B)
Validation	SSL socket check, heuristics, keyword scans
Scoring	Custom logic based on metadata completeness


Limitations & Future Improvements:

While LLMs are powerful in understanding unstructured text, relying solely on them for structured data extraction from varied websites can result in inconsistencies and sparse outputs. We propose the following improvements:

1. Hybrid Extraction: Combine LLM output with rule-based schema scraping for precision.

2. CRM Integration: Leverage APIs like Clearbit, Apollo, or Crunchbase for enriched data.

3. ML-Based Scoring: Replace rule-based scoring with ML models trained on lead conversion datasets.

4. Data Cleanup: Use NLP pipelines to filter noise and extract cleaner metadata from webpages.


SCREEN RECORDING DRIVE LINK :

https://drive.google.com/drive/folders/1aj4gHsO3NucCy4_XYHN7ynCd3eU97eqG?usp=drive_link
