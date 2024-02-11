# clara-bot

Un bot Telegram utilisant les modèles de langage de Mistral et de OpenAI.

## Prérequis

- Docker
- Un compte [Mistral](https://console.mistral.ai/user/api-keys/) ou [OpenAI](https://platform.openai.com/api-keys)
- Un token de [bot Telegram](https://www.commentcoder.com/bot-telegram/)

## Configuration

1. Renommez le fichier ```.env.example``` en  ```.env```
2. Modifiez le fichier ```.env``` en renseignant votre [clé API Mistral](https://console.mistral.ai/user/api-keys/) (ou [OpenAI](https://platform.openai.com/api-keys)) et le token du bot Telegram.
Choisissez également le modèle à utiliser : ```mistral``` pour **mistral-tiny** ou ```openai``` pour **gpt-3.5-turbo**.

```bash
MISTRAL_API_KEY=
OPENAI_API_KEY=
BOT_TOKEN=
MODEL=mistral
```

## Lancer le bot

```bash
docker build -t clara-bot .
docker run --name clara --rm clara-bot
```

Ou si vous êtes sous Linux, vous pouvez simplement faire :

```bash
make
```

## Stopper le bot

Faites ```CTRL+C``` pour stopper le bot.
