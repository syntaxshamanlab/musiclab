#!/usr/bin/env python3
"""
Quick Reference: Working with THE VAULT processed data

This file demonstrates how to work with the processed song JSON files
for Suno AI integration, analysis, or further processing.
"""

import json
import os
from pathlib import Path

def load_all_songs(output_dir="vault/output"):
    """Load all processed songs from vault."""
    songs = {}
    for json_file in Path(output_dir).glob("*.json"):
        with open(json_file) as f:
            data = json.load(f)
            songs[data["id"]] = data
    return songs

def filter_songs_by_tag(songs, tag):
    """Find all songs with a specific tag."""
    return [song for song in songs.values() if tag in song.get("tags", [])]

def get_song_by_id(songs, song_id):
    """Get a specific song by ID."""
    return songs.get(song_id)

def get_song_lyrics(song):
    """Extract all lyrics from a song."""
    if not song.get("lyrics"):
        return "No lyrics extracted"
    
    result = f"## {song['title']}\n\n"
    for section in song["lyrics"]:
        result += f"[{section['section']}]\n"
        result += f"{section['text']}\n\n"
    return result

def generate_suno_prompt(song):
    """
    Generate a Suno AI prompt from song metadata.
    
    This creates a structured prompt for Suno's music generation API.
    """
    profile = song.get("profile", "Default")
    tags = ", ".join(song.get("tags", ["ambient"]))
    bpm = song.get("bpm", 92)
    mix = song.get("mix", {})
    
    prompt = f"""
SONG: {song['title']}
BPM: {bpm}
VIBE: {profile}
TAGS: {tags}

AUDIO MIX:
- Drums: {mix.get('drums', 80)}%
- Bass: {mix.get('bass', 80)}%
- Vocals: {mix.get('vocals', 100)}%
- Effects: {mix.get('fx', 50)}%

[LYRICS]
"""
    
    for section in song.get("lyrics", []):
        prompt += f"\n[{section['section']}]\n{section['text']}"
    
    return prompt

def export_songs_to_csv(songs, filename="vault_export.csv"):
    """Export all songs to CSV for spreadsheet analysis."""
    import csv
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Title", "BPM", "Profile", "Tags", "Lyric Sections", "Visuals"])
        
        for song in songs.values():
            writer.writerow([
                song["id"],
                song["title"],
                song["bpm"],
                song["profile"],
                "; ".join(song.get("tags", [])),
                len(song.get("lyrics", [])),
                len(song.get("visuals", []))
            ])
    
    print(f"Exported {len(songs)} songs to {filename}")

def create_suno_batch(songs, output_file="suno_batch.jsonl"):
    """
    Create a batch file for Suno AI processing.
    
    Output format: JSONL (one JSON object per line)
    Each line is a complete prompt for Suno's API.
    """
    with open(output_file, 'w') as f:
        for song in songs.values():
            prompt = generate_suno_prompt(song)
            batch_item = {
                "id": song["id"],
                "title": song["title"],
                "prompt": prompt,
                "bpm": song["bpm"],
                "tags": song.get("tags", [])
            }
            f.write(json.dumps(batch_item) + "\n")
    
    print(f"Created batch file: {output_file}")

def analyze_song_stats(songs):
    """Print statistics about the song collection."""
    print("\n=== VAULT STATISTICS ===\n")
    print(f"Total Songs: {len(songs)}")
    print(f"Average BPM: {sum(s.get('bpm', 92) for s in songs.values()) / len(songs):.1f}")
    
    # Tag analysis
    all_tags = []
    for song in songs.values():
        all_tags.extend(song.get("tags", []))
    print(f"Unique Tags: {len(set(all_tags))}")
    print(f"Most Common Tags:")
    from collections import Counter
    for tag, count in Counter(all_tags).most_common(5):
        print(f"  - {tag}: {count}")
    
    # Lyric analysis
    total_lyrics = sum(len(s.get("lyrics", [])) for s in songs.values())
    print(f"\nTotal Lyric Sections: {total_lyrics}")
    print(f"Avg Sections per Song: {total_lyrics / len(songs):.1f}")
    
    # Visual cues analysis
    total_visuals = sum(len(s.get("visuals", [])) for s in songs.values())
    print(f"Total Visual Cues: {total_visuals}")

def main():
    """Example usage of vault processing functions."""
    
    print("Loading songs from vault...")
    songs = load_all_songs()
    print(f"✓ Loaded {len(songs)} songs\n")
    
    # Show statistics
    analyze_song_stats(songs)
    
    # Example: Get first song
    if songs:
        first_song_id = list(songs.keys())[0]
        song = songs[first_song_id]
        
        print(f"\n=== SAMPLE SONG ===\n")
        print(f"Title: {song['title']}")
        print(f"BPM: {song['bpm']}")
        print(f"Profile: {song['profile']}")
        print(f"Tags: {', '.join(song.get('tags', []))}")
        
        if song.get("lyrics"):
            print(f"\nFirst 200 chars of lyrics:")
            first_lyric = song["lyrics"][0]["text"]
            print(f"{first_lyric[:200]}...")
    
    # Optional: Uncomment to generate export files
    # export_songs_to_csv(songs)
    # create_suno_batch(songs)

if __name__ == "__main__":
    main()
