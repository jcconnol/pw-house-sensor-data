#Pulls in changes from github then 
# runs the facial recognition program and speech bot in background

git checkout main

git fetch origin

git pull origin main


python3 index.py &

#python3 speechMain.py &
