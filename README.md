# Telegram Message Scheduler (Personal Account)

A Docker-based application that sends messages from your personal Telegram account to a specified recipient every 12 hours.

## Prerequisites

- Docker and Docker Compose installed on your system
- Your Telegram account phone number
- API credentials from Telegram (API ID and API Hash)

## Setup

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd telegramspam
   ```

2. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

3. Edit the `.env` file with your Telegram API credentials, phone number, recipient, and custom message:
   ```
   API_ID=12345
   API_HASH=your_api_hash_here
   PHONE_NUMBER=+12345678901
   RECIPIENT=@username_or_phone_number
   MESSAGE=Your custom message text here
   ```

### How to get Telegram API Credentials

1. Visit [https://my.telegram.org/](https://my.telegram.org/) and log in with your phone number
2. Click on "API Development Tools"
3. Fill in the required fields (you can put "Telegram Scheduler" as the app name and any other necessary details)
4. Submit the form to get your `API_ID` and `API_HASH`

### First-Time Setup

The first time you run the application, you'll need to authorize your Telegram account:

1. Start the container in interactive mode:
   ```bash
   docker-compose run --rm telegram-scheduler
   ```

2. You will be prompted to enter the confirmation code that Telegram sends to your account
3. Enter the code to complete the authorization process
4. After successful authorization, a session file will be created that allows the application to send messages without requiring further authorization

## Usage

### Running with Docker Compose (recommended)

```bash
docker-compose up -d
```

This will:
- Build the Docker image
- Start the container in detached mode
- Configure the container to restart automatically if it crashes or if the system reboots

### Running with Docker directly

```bash
docker build -t telegram-scheduler .
docker run -d --name telegram-scheduler --restart unless-stopped -v $(pwd)/.env:/app/.env -v $(pwd)/session:/app telegram-scheduler
```

## Logs

To view the logs and check if messages are being sent:

```bash
docker logs -f telegram-scheduler
```

## Stopping the service

```bash
docker-compose down
```

Or if you're using Docker directly:

```bash
docker stop telegram-scheduler
docker rm telegram-scheduler
```

## Configuration

You can modify the following environment variables in the `.env` file:

- `API_ID`: Your Telegram API ID (required)
- `API_HASH`: Your Telegram API hash (required)
- `PHONE_NUMBER`: Your Telegram account phone number with country code (required)
- `RECIPIENT`: The username, phone number, or chat ID of the recipient (required)
- `MESSAGE`: The message to send (optional, default message will be used if not specified)

## Customizing the Schedule

The default schedule is set to send messages every 12 hours. If you want to change this:

1. Edit the `telegram_scheduler.py` file
2. Locate the line: `schedule.every(12).hours.do(send_message)`
3. Modify it as needed (e.g., `schedule.every(6).hours.do(send_message)` for every 6 hours)
4. Rebuild and restart the Docker container

## Timezone

By default, the scheduler uses UTC time. You can change the timezone by editing the `TZ` environment variable in the `docker-compose.yml` file.

## Important Notes on Using a Personal Account

- **Rate Limits**: Telegram imposes rate limits on sending messages. If you hit these limits, the application will wait the required time before retrying.
- **Terms of Service**: Make sure your usage complies with Telegram's Terms of Service. Spam or abusive behavior may result in your account being banned.
- **Session Security**: The session file contains authentication information for your Telegram account. Keep it secure and don't share it.

## License

This project is open source and available under the MIT License. 