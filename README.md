# Tamagotchi Pet - Streamlit App

A simple Tamagotchi-style pet game built with Streamlit.

## Features

- **Three core stats**: Hunger, Energy, and Happiness (0–100)
- **Three actions**: Feed, Play, and Sleep
- **Dynamic mood system**: State changes based on stats
- **Random negative events**: 40% chance per action
- **Periodic speech**: Messages reflect current mood
- **Game Over**: If any stat reaches 0, you lose
- **Clean Streamlit UI** with progress bars and speech bubbles

## Actions

| Action | Hunger | Energy | Happiness |
|---|---|---|---|
| Feed | +20 | +5 | +5 |
| Play | -5 | -10 | +20 |
| Sleep | -8 | +25 | +5 |

## Pet States

| State | Condition |
|---|---|
| Critical | Any stat ≤ 10 |
| Very tired and sad | Any stat 11–20 |
| Tired | Any stat 21–40 |
| Normal | All 41–59 |
| Good | All ≥ 60 |
| Fantastic | All ≥ 80 |

## Run it

```powershell
cd "C:\Users\deban\OneDrive\Documentos\Mascota"
pip install -r requirements.txt
streamlit run app.py
```

## Project Structure

```text
Mascota/
├── app.py
├── pet.py
├── requirements.txt
└── README.md
```
