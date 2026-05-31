# voiceagent
AI voice agent for phone calls using Twilio, Gemini 1.5, and Cloud Run with auto-deploy CI/CD

markdown# Voice Concierge

AI phone agent that answers calls for your business using Twilio Voice, Gemini 1.5 Pro, and Cloud Run.

**Stack**: FastAPI + Gemini + Twilio + Cloud Run + GitHub Actions CI/CD

### How it works
1. Customer calls your Twilio number
2. Twilio hits `/voice` webhook on Cloud Run
3. App transcribes speech → queries Gemini with your FAQ/context
4. Gemini response → Twilio TwiML → spoken back to caller
5. Full conversation loop until hangup

### Features
- **RAG**: Answers from `faq.json` or Vertex AI Search
- **Low latency**: Gemini 1.5 Flash, Cloud Run min-instances=1
- **Auto-deploy**: Push to `main` = deployed in 3 min via GitHub Actions
- **Secure**: Twilio signature validation, secrets in Secret Manager

### Quick deploy
[[Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run?git_repo=https://github.com/YOUR_USER/voice-concierge)

### Manual setup
1. **Prereqs**: GCP project with billing, Twilio account + phone number
2. **Secrets**: 
   ```bash
   echo -n "your_twilio_auth_token" | gcloud secrets create TWILIO_AUTH_TOKEN --data-file=-Deploy: Push to main branch. GitHub Actions handles build + deploy.Twilio: Point your number's Voice webhook to https://SERVICE-URL/voice POSTLocal devbashpip install -r requirements.txt
uvicorn main:app --reload --port 8000
ngrok http 8000  # Use ngrok URL for Twilio testingCost
∼$0.0015 per call. $300 GCP credits = ∼200k calls. Cloud Run free tier covers <2M requests/mo.Repo structurejavascript├── main.py              # FastAPI app + Twilio webhook
├── requirements.txt     # Python deps
├── Dockerfile           # Container for Cloud Run
├── faq.json             # Knowledge base for RAG
└── .github/workflows/   # Auto-deploy to Cloud Run
    └── deploy.yml
