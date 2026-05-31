import os, json
from fastapi import FastAPI, Request, Response
from fastapi.responses import PlainTextResponse
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.request_validator import RequestValidator
from vertexai.generative_models import GenerativeModel
import vertexai

app = FastAPI()
vertexai.init(project=os.getenv("GCP_PROJECT"), location="us-central1")
model = GenerativeModel("gemini-1.5-flash-001")
with open("faq.json") as f:
    FAQ = json.load(f)

def validate_request(request: Request, form: dict) -> bool:
    validator = RequestValidator(os.getenv("TWILIO_AUTH_TOKEN", ""))
    url = str(request.url)
    signature = request.headers.get("X-Twilio-Signature", "")
    return validator.validate(url, form, signature)

@app.post("/voice")
async def voice(request: Request):
    form = await request.form()
    if not validate_request(request, form):
        return Response("Forbidden", status_code=403)
    
    speech = form.get("SpeechResult", "")
    response = VoiceResponse()
    
    if not speech:
        gather = Gather(input="speech", action="/voice", timeout=5, speech_timeout="auto")
        gather.say("Hi, thanks for calling Acme. How can I help you?")
        response.append(gather)
        response.redirect("/voice")
    else:
        context = json.dumps(FAQ)
        prompt = f"You are Acme phone support. Answer based only on this FAQ: {context}\n\nCaller said: {speech}\nAnswer in 1-2 sentences."
        answer = model.generate_content(prompt).text
        response.say(answer)
        gather = Gather(input="speech", action="/voice", timeout=5)
        gather.say("Anything else I can help with?")
        response.append(gather)
        response.hangup()
    
    return PlainTextResponse(str(response), media_type="application/xml")

@app.get("/health")
def health():
    return {"status": "ok"}
