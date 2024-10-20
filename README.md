# mathviz

## Install

'''sh
sudo apt update

# Required Dependencies

sudo apt install build-essential python3-dev libcairo2-dev libpango1.0-dev ffmpeg

# Optional Dependencies

sudo apt install texlive texlive-latex-extra
poetry install
'''

## Run a scene

'poetry run python -m manim -ql scenes/<scene>.py'
