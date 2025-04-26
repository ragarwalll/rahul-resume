#!/bin/bash
echo "data.json has been changed. Running the command..."
# Example command: cat the contents of data.json
poetry --directory vitagen run start-module --input ../data.json --output ../processor/python-data.tex
