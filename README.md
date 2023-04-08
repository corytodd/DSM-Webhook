# Synology Webhook Receiver

A bit of blue to turn Synology events into Gitea issues.

## DSM Setup

The Synology DiskStation started supporting webhooks at some point. I am
running DSM 7.1.1 and things mostly work. You have to manually tweak a
configuration file on the diskstation itself because the UI makes it
hard (impossible??) to setup correctly.

1. Manually create the webhook and wonder why the UI complains about
   the content type.
2. Edit `/usr/syno/etc/synowebhook.conf` and fix the req_header. Notice
   the placeholder @@FULLTEXT@@ is wrong and the req_param is empty.

Wrong

```
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

```
  "test": {
    "needssl": true,
    "port": 443,
    "prefix": "A new system event occurred on your %HOSTNAME% on %DATE% at %TIME%.",
    "req_header": "Content-Type:applycation/json\r",
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

