# summarizer

## summarize-email

- Need to place the `.env` on the `project_root`:
```.env
GMAIL_ADDRESS=<replace_with_username>@gmail.com
GMAIL_APP_PASSWORD=<replace_with_password>
#GMAIL_LABEL=INBOX
GMAIL_LIMIT=3
GMAIL_UNREAD_ONLY=true
#GMAIL_TOKEN_PATH=token.json
#GMAIL_CLIENT_SECRET_FILE=credentials.json
```

- Need to place the `credentials.json` on the `project_root`:
  - Setup OAuth: Go to the Google Cloud Console.
  - Create a Desktop OAuth Client.
  - Download the JSON file and save it as `credentials.json`
```example_credentials.json`
{"installed":{"client_id":"<some-alphanumeric>.apps.googleusercontent.com","project_id":"<project_name>-426921","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"<real_secret_alphanumeric>","redirect_uris":["http://localhost"]}}
```

- MAKE sure the `.gitignore` contains
```
# Gmail OAuth / local secrets
.env
token.json
credentials.json
```