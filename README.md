## Deta Slack Bot

Slack Bot Deployed on [Deta](https://deta.sh).

Sends new users a direct message.

### Configuration and Deployment

Clone the repository and create a new Deta micro with `deta new` in the cloned repository.

Requires subscription to the `team_join` event on slack.

Requires the following oauth permissions in your slack app.

- `users:read`
- `channels:manage`
- `groups:read`
- `im:write`
- `mpim:write`

Requires the following environment variables.

- `SECRET_TOKEN`: signing secret of your app (found under `App Credentials` of your slack app's `Basic Information` Page)
- `AUTH_TOKEN`: app's oauth token that you get after you install a app in a slack workspace

Create a `.env` file with these environment variables and update them with `deta update -e .env`

The message sent is defined in `utils.welcome_message` method. Change the message and deploy the micro with `deta deploy` to send your own message.