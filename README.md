# libpyslack - Slack API Wrapper for Python3
LambdaからSlackに通知を送るためのLamdaLayer。libというほどのものでもない。

## LambdaLayer Building
### Building
```
$ make
or
$ make clean; make test; make build

```

### Upload to LambdaLayer
Upload to Lambda Layer


## Usage
```python
from libpyslack import PySlack, PostMessageBuilder

...
...
...

def lambda_handler(event, context):
    message = PostMessageBuilder()\
                .channel('TestChannel')\
                .username('Test User Bot')\
                .text('Message Body')\
                .description("Message Description")\
                .emoji(':thumbsup:')\
                .attachments([
                    PostMessageBuilder.attachment('title1', 'pretext1', 'text1', 'good', [
                        PostMessageBuilder.field('field-title 1', 'field-value 1', True),
                        PostMessageBuilder.field('field-title 2', 'field-value 2', True),
                        PostMessageBuilder.field('field-title 3', 'field-value 3', True),
                        PostMessageBuilder.field('field-title 4', 'field-value 4', True),
                        PostMessageBuilder.field('field-title 5', 'field-value 5'),
                        PostMessageBuilder.field('field-title 6', 'field-value 6')
                    ])
                ])\
                .build()
    
    py_slack = PySlack('[AuthToken]')
    
    response = py_slack.post_message(message)
    
    return {
        'statusCode': 200,
        'body': response
    }
```

