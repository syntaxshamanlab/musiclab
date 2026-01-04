import os, json, yaml
from slugify import slugify
from jsonschema import validate
import mammoth

RAW_DIR = "vault/raw"
CONVERTED_DIR = "vault/converted"
OUTPUT_DIR = "vault/output"

# Load Schemas and Configs
with open("vault/schema.json") as f:
    SCHEMA = json.load(f)

with open("config.yaml") as f:
    CONFIG = yaml.safe_load(f)

def convert_docx_to_md(path):
    with open(path, "rb") as docx_file:
        result = mammoth.convert_to_markdown(docx_file)
        return result.value

def extract_fields(md_text):
    lines = [l.strip() for l in md_text.split("\n") if l.strip()]
    if not lines: return None

    title = lines[0].lstrip("#").strip()
    tags = [t.replace("#", "").strip() for t in lines[1:] if t.startswith("#")]
    lyrics = []
    current_section = None
    buffer = []

    for i, line in enumerate(lines):
        if i == 0: continue
        if line.startswith("[") and "]" in line:
            if current_section:
                lyrics.append({
                    "section": current_section.strip("[]"),
                    "text": " / ".join(buffer).strip(),
                    "note": ""
                })
            current_section = line
            buffer = []
        elif not line.startswith("#"):
            buffer.append(line)

    if current_section:
        lyrics.append({
            "section": current_section.strip("[]"),
            "text": " / ".join(buffer).strip(),
            "note": "Extracted via Ingest Pipeline"
        })

    return {"title": title, "tags": tags, "lyrics": lyrics}

def normalize(obj):
    obj["id"] = slugify(obj["title"])
    obj["bpm"] = CONFIG["defaults"]["bpm"]
    obj["profile"] = CONFIG["defaults"]["profile"]
    obj["metrics"] = CONFIG["defaults"]["metrics"]
    obj["mix"] = CONFIG["defaults"]["mix"]
    obj["visuals"] = CONFIG["defaults"]["visuals"]
    return obj

def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(CONVERTED_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for filename in os.listdir(RAW_DIR):
        if not filename.endswith(".docx"): continue

        path = os.path.join(RAW_DIR, filename)
        md = convert_docx_to_md(path)

        with open(os.path.join(CONVERTED_DIR, f"{filename}.md"), "w") as f:
            f.write(md)

        obj = extract_fields(md)
        if obj:
            obj = normalize(obj)
            validate(instance=obj, schema=SCHEMA)

            with open(os.path.join(OUTPUT_DIR, f"{obj['id']}.json"), "w") as f:
                json.dump(obj, f, indent=4)

    print("Ingestion complete. Objects in vault/output/")

if __name__ == "__main__":
    main()