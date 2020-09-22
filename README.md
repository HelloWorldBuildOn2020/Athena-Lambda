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

### Multiple version python seperate by **pipenv**
For first time.
1. Install python 3.8 on Ubuntu 18.04
  - `sudo apt install python3.8`
2. Check version python 3.8
  - `python3.8 --version`
3. Install python 3.8 on virtual environment (pipenv)
  - `pipenv --python 3.8 install`
4. Shell to enviroment
  - `pipenv shell`
5. Check version in pipenv
  - `python --version`

Enjoy~

#### Next time ~~~
```bash
pipenv shell
```
-----
