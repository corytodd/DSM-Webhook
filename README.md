# Synology Webhook Receiver

A bit of glue to turn Synology events into Gitea issues.

## DSM Setup

The Synology DiskStation started supporting webhooks at some point. I am
running DSM 7.1.1 and things mostly work. You have to manually tweak a
configuration file on the diskstation itself because the UI makes it
hard (impossible??) to setup correctly.

1. Manually create the webhook and wonder why the UI complains about
   the content type.
2. Edit `/usr/syno/etc/synowebhook.conf` and fix the req_header. Notice
   the Content-Type is wrong and that the req_param is empty.

Use `sudo -i` to enter root, assuming your user has admin rights.

Wrong

```json
  "test": {
    "needssl": true,
    "port": 443,
    "prefix": "A new system event occurred on your %HOSTNAME% on %DATE% at %TIME%.",
    "req_header": "Content-Type:@@FULLTEXT@@\r",
    "req_method": "post",
    "req_param": "{}",
    "sepchar": " ",
    "template": "https://example.com",
    "type": "custom",
    "url": "https://example.com"
  }
```

Right

```json
  "test": {
    "needssl": true,
    "port": 443,
    "prefix": "A new system event occurred on your %HOSTNAME% on %DATE% at %TIME%.",
    "req_header": "Content-Type:application/json\r",
    "req_method": "post",
    "req_param": "{\"description\": \"@@TEXT@@\", \"title\": \"@@PREFIX@@\"}",
    "sepchar": " ",
    "template": "https://example.com",
    "type": "custom",
    "url": "https://example.com"
  }
```

Once that is settled, you should be able to shoot webhooks from your DSM
without error. Unfortunately the webhook GUI editor will still be wonky.

## Gitea Setup

You need at least one Gitea user and an access token that can file issues.
The easiest solution is to make yourself a token with `repo` permissions.
Be sure to add your username and token to your `.env` file.

## Service Setup

The service file assumes that you are running this listener on a server
that has a user named `bot`. The application runs from `/srv/hook` which
itself owned by `bot`. Don't forget to create a venv and install the
requirements.

For example

```
useradd bot
mkdir -p /srv/hook
git clone https://github.com/corytodd/DSM-Webhook.git /srv/hook
cd /srv/hook
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp hook.service /etc/systemd/system
chown -R bot:bot /srv/hook
systemctl enable hook.service
systemctl start hook.service
systemctl status hook.service
```