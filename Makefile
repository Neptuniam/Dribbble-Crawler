include .env

all: toDribbble

# Sends the post to the War-Room Dribbble Channel
toDribbble:
	pipenv run python3 main.py ${HOOK}

# Sends the post to my DM's for testing channels without spamming everyone
toMe:
	pipenv run python3 main.py ${DEVHOOK}

help:
	pipenv run python3 -c "import main; help(main)"
