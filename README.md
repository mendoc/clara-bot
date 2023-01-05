# clara-bot
Un bot Telegram basé sur chatGPT

## Prérequis
- Python 3.7 ou supérieur
- Un compte [OpenAI](https://beta.openai.com/account/api-keys)
- Un token de [bot Telegram](https://www.commentcoder.com/bot-telegram/)


## Installation
```bash
virtualenv .clara
virtualenv -p /usr/bin/python3.7 .clara
source .clara/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Modifiez le fichier ```.env``` en renseignant les clés API OpenAI et du bot Telegram
```bash
OPENAI_API_KEY=
BOT_TOKEN=
```

## Lancement
```bash
python bot.py
```
```CTRL+C``` pour stopper le bot.


## Désactiver environnement Python
```bash
deactivate
```