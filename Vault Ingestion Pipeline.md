# 🟦 THE VAULT INGESTION PIPELINE — CODESPACE HANDOFF
**Purpose:** Automate the conversion of .docx song files into fully structured Vault song objects for the SPA.
## 🟩 Directory Layout
Ensure your repository is structured as follows for the script to execute correctly:
/vault/  
/raw/ # Place all .docx files here  
/converted/ # Auto-generated markdown  
/output/ # Final JSON song objects  
ingest.py # Main ingestion script  
schema.json # Vault object schema  
config.yaml # Normalization rules  
## 🟧 Devcontainer Setup
Add this to .devcontainer/devcontainer.json to ensure the Codespace auto-installs all dependencies:
{  
"name": "Vault Ingestion",  
"image": "\[mcr.microsoft.com/devcontainers/python:3.11\](https://mcr.microsoft.com/devcontainers/python:3.11)",  
"postCreateCommand": "pip install python-docx pyyaml mammoth slugify jsonschema",  
"customizations": {  
"vscode": {  
"extensions": \[  
"ms-python.python",  
"ms-python.vscode-pylance"  
\]  
}  
}  
}  
## 🟥 The Ingestion Script (ingest.py)
This script handles the heavy lifting of extraction, normalization, and validation.
import os, json, yaml  
from slugify import slugify  
from jsonschema import validate  
import mammoth  
RAW\_DIR = "vault/raw"  
CONVERTED\_DIR = "vault/converted"  
OUTPUT\_DIR = "vault/output"  
\# Load Schemas and Configs  
with open("vault/schema.json") as f:  
SCHEMA = json.load(f)  
with open("vault/config.yaml") as f:  
CONFIG = yaml.safe\_load(f)  
def convert\_docx\_to\_md(path):  
with open(path, "rb") as docx\_file:  
result = mammoth.convert\_to\_markdown(docx\_file)  
return result.value  
def extract\_fields(md\_text):  
lines = \[l.strip() for l in md\_text.split("\\n") if l.strip()\]  
if not lines: return None  
title = lines\[0\]  
tags = \[t.replace("#", "") for t in lines if t.startswith("#")\]  
lyrics = \[\]  
current\_section = None  
buffer = \[\]  
for line in lines:  
if line.startswith("\[") and "\]" in line:  
if current\_section:  
lyrics.append({  
"section": current\_section.strip("\[\]"),  
"text": " / ".join(buffer).strip(),  
"note": ""  
})  
current\_section = line  
buffer = \[\]  
elif not line.startswith("#") and line != title:  
buffer.append(line)  
if current\_section:  
lyrics.append({  
"section": current\_section.strip("\[\]"),  
"text": " / ".join(buffer).strip(),  
"note": "Extracted via Ingest Pipeline"  
})  
return {"title": title, "tags": tags, "lyrics": lyrics}  
def normalize(obj):  
obj\["id"\] = slugify(obj\["title"\])  
obj\["bpm"\] = CONFIG\["defaults"\]\["bpm"\]  
obj\["profile"\] = CONFIG\["defaults"\]\["profile"\]  
obj\["metrics"\] = CONFIG\["defaults"\]\["metrics"\]  
obj\["mix"\] = CONFIG\["defaults"\]\["mix"\]  
obj\["visuals"\] = CONFIG\["defaults"\]\["visuals"\]  
return obj  
def main():  
os.makedirs(CONVERTED\_DIR, exist\_ok=True)  
os.makedirs(OUTPUT\_DIR, exist\_ok=True)  
for filename in os.listdir(RAW\_DIR):  
if not filename.endswith(".docx"): continue  
path = os.path.join(RAW\_DIR, filename)  
md = convert\_docx\_to\_md(path)  
with open(os.path.join(CONVERTED\_DIR, f"{filename}.md"), "w") as f:  
f.write(md)  
obj = extract\_fields(md)  
if obj:  
obj = normalize(obj)  
validate(instance=obj, schema=SCHEMA)  
with open(os.path.join(OUTPUT\_DIR, f"{obj\['id'\]}.json"), "w") as f:  
json.dump(obj, f, indent=4)  
print("Ingestion complete. Objects in vault/output/")  
if \_\_name\_\_ == "\_\_main\_\_":  
main()  
## 🟨 Schema and Config Files
**vault/schema.json**
{  
"type": "object",  
"required": \["id", "title", "bpm", "profile", "tags", "metrics", "mix", "lyrics", "visuals"\],  
"properties": {  
"id": { "type": "string" },  
"title": { "type": "string" },  
"bpm": { "type": "number" },  
"profile": { "type": "string" },  
"tags": { "type": "array", "items": { "type": "string" } },  
"metrics": {  
"type": "object",  
"properties": {  
"density": { "type": "array", "items": { "type": "number" }, "minItems": 8, "maxItems": 8 },  
"intensity": { "type": "array", "items": { "type": "number" }, "minItems": 8, "maxItems": 8 }  
}  
},  
"mix": { "type": "object" },  
"lyrics": { "type": "array" },  
"visuals": { "type": "array" }  
}  
}  
**vault/config.yaml**
defaults:  
bpm: 92  
profile: "Processed Reality / Street-Born Fate"  
metrics:  
density: \[50, 50, 50, 50, 50, 50, 50, 50\]  
intensity: \[50, 50, 50, 50, 50, 50, 50, 50\]  
mix: { drums: 80, bass: 80, vocals: 100, fx: 50 }  
visuals:  
\- time: "0:00"  
event: "Initialization"  
desc: "Default visual protocol engaged."