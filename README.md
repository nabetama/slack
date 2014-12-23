# Slacky

A Python package for Slack's [JSON REST API](https://api.slack.com/).

## Examples

```python

from slacky import Slacky

slack = Slacky(token='<Your slack api token>')

# Send a message to #general channel.
slack.chat.post_message('#general', 'Hello from slacky')

# If you want a JSON result.
print slack.chat.post_message('#general', 'Hello from slacky').json()
> => {u'ok': True,  u'ts': u'1234567890.000001',  u'channel': u'XXXXXXXXX'}

# Get user list.
slack.users.list.json(['members'])

# Upload a file.
slack.files.upload(file='hello.png')

```

## Installation

```sh
pip install slacky
```

