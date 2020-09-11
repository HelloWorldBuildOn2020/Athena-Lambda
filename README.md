Athena Lambda function
----
Run function
1. Start docker
2. Build you code when you edited it.
```bash
sam build
```
3. Run command follow below:
```bash
sam local invoke -e events/event.json
```
> *Name of function is in template.yaml next line on Resource
----