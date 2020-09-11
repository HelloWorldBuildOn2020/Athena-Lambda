Athena Lambda function
----
Run function
```bash
sam local invoke "Name of Function" -e events/event.json
#Example
sam local invoke "HelloWorldFunction" -e events/event.json
```
