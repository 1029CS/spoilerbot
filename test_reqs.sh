#!/bin/sh
python3 -m pip freeze > requirements.txt
sudo docker build . -t dev
sudo docker run dev