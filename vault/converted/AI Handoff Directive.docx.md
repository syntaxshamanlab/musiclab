# AI Directive: The Vault Content Update

## Context

You are an expert frontend developer and data architect\. You are updating a single\-page application \(SPA\) called "THE VAULT," which serves as a lyrical and sonic archive\. The application uses a central songs data array to populate both a "Hub" \(grid view\) and a "Sonic Lab" \(detail view\)\.

## Technical Stack

- __Styling:__ Tailwind CSS \(CDN\)
- __Charts:__ Chart\.js \(CDN\)
- __Architecture:__ Vanilla JS state\-based navigation \(No page refreshes\)

## The Task

Insert a new song object into the const songs array located in the <script> tag of index\.html\.

## Data Schema Requirements

Each song object __MUST__ adhere to this exact structure:

\{  
    id: "unique\-slug\-string",  
    title: "Song Title",  
    bpm: number,  
    profile: "Genre/Texture Description",  
    tags: \["Tag1", "Tag2"\],  
    metrics: \{   
        // 8 data points for the Flow Topology line chart  
        density: \[n1, n2, n3, n4, n5, n6, n7, n8\],   
        intensity: \[n1, n2, n3, n4, n5, n6, n7, n8\]   
    \},  
    mix: \{   
        // 0\-100 values for the Radar chart  
        drums: number,   
        bass: number,   
        vocals: number,   
        fx: number   
    \},  
    lyrics: \[  
        \{ section: "SECTION\_NAME", text: "Lyric lines here", note: "Production/Cadence cue" \}  
    \],  
    visuals: \[  
        \{ time: "0:00", event: "Event Name", desc: "Visual description" \}  
    \]  
\}  


## Implementation Rules

1. __Preserve ID Integrity:__ Ensure the id is a lowercase, hyphenated string\.
2. __Chart Logic:__ Ensure the metrics arrays contain exactly 8 numbers to maintain visual consistency in the line chart\.
3. __Escaping:__ Properly escape any single quotes or backticks if they appear within the lyric text\.
4. __No UI Changes:__ Do not modify the renderSongLab or initCharts functions unless explicitly asked\. Only update the data array\.
5. __Alpha Order:__ Insert the new song at the top of the array or maintain alphabetical order by title\.

## Input Data

\[PASTE YOUR SONG DETAILS/LYRICS HERE\]

