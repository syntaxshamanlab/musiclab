#!/usr/bin/env python3
"""
Convert processed JSON lyric files to THE VAULT song objects
"""

import json
import os
from pathlib import Path

def load_processed_songs(output_dir="vault/output"):
    """Load all processed JSON files and convert to song objects."""
    songs = []
    
    output_path = Path(output_dir)
    if not output_path.exists():
        print(f"Error: {output_dir} not found")
        return songs
    
    # Load each JSON file
    for json_file in sorted(output_path.glob("*.json")):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                song = {
                    "id": data.get("id", "unknown"),
                    "title": data.get("title", "Unknown").replace("\n", "").replace("\\", ""),
                    "bpm": data.get("bpm", 92),
                    "profile": data.get("profile", "Default Profile"),
                    "tags": data.get("tags", []),
                    "metrics": data.get("metrics", {
                        "density": [50]*8,
                        "intensity": [50]*8
                    }),
                    "mix": data.get("mix", {
                        "drums": 80,
                        "bass": 80,
                        "vocals": 100,
                        "fx": 50
                    }),
                    "lyrics": data.get("lyrics", []),
                    "visuals": data.get("visuals", [])
                }
                
                # Ensure metrics have exactly 8 values
                if "density" not in song["metrics"] or len(song["metrics"]["density"]) != 8:
                    song["metrics"]["density"] = [50]*8
                if "intensity" not in song["metrics"] or len(song["metrics"]["intensity"]) != 8:
                    song["metrics"]["intensity"] = [50]*8
                
                songs.append(song)
                print(f"Loaded: {song['title']}")
        except Exception as e:
            print(f"Error loading {json_file}: {e}")
    
    return songs

def generate_js_array(songs):
    """Generate JavaScript array string for embedding in HTML."""
    js_code = "const songs = [\n"
    
    for i, song in enumerate(songs):
        # Escape quotes and special chars in strings
        title = song["title"].replace('"', '\\"').replace("'", "\\'")
        profile = song["profile"].replace('"', '\\"').replace("'", "\\'")
        
        js_code += f'''            {{
                id: "{song['id']}",
                title: "{title}",
                bpm: {song['bpm']},
                profile: "{profile}",
                tags: {json.dumps(song['tags'])},
                metrics: {{
                    density: {json.dumps(song['metrics'].get('density', [50]*8))},
                    intensity: {json.dumps(song['metrics'].get('intensity', [50]*8))}
                }},
                mix: {{
                    drums: {song['mix'].get('drums', 80)},
                    bass: {song['mix'].get('bass', 80)},
                    vocals: {song['mix'].get('vocals', 100)},
                    fx: {song['mix'].get('fx', 50)}
                }},
                lyrics: {json.dumps(song['lyrics'])},
                visuals: {json.dumps(song['visuals'])}
            }}'''
        
        if i < len(songs) - 1:
            js_code += ",\n"
        else:
            js_code += "\n"
    
    js_code += "        ];\n"
    return js_code

def main():
    print("Loading processed lyric files...")
    songs = load_processed_songs()
    
    if not songs:
        print("No songs loaded. Exiting.")
        return
    
    print(f"\nSuccessfully loaded {len(songs)} songs")
    
    # Generate JavaScript array
    js_array = generate_js_array(songs)
    
    # Save to a separate file for easy reference
    with open("vault/songs.js", "w") as f:
        f.write(js_array)
    print(f"\nGenerated vault/songs.js with {len(songs)} songs")
    
    # Read index.html
    with open("index.html", "r") as f:
        html_content = f.read()
    
    # Find and replace the songs array
    import re
    pattern = r'const songs = \[.*?\];'
    match = re.search(pattern, html_content, re.DOTALL)
    if match:
        # Replace the existing array
        start = match.start()
        end = match.end()
        new_html = html_content[:start] + js_array.rstrip("\n") + html_content[end:]
        
        with open("index.html", "w") as f:
            f.write(new_html)
        print("Updated index.html with processed songs")
    else:
        print("Warning: Could not find const songs array in index.html")
    
    print("\nDone! You can now open index.html in a browser to view THE VAULT")

if __name__ == "__main__":
    main()
