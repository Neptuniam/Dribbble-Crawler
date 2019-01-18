# Dribbble-slack
A simple python web scraper to pull the top daily Dribbble content into slack.

### Installing

Install all of the required dependencies:

```
pipenv install
```

### Running

Execute the crawler manually by running:
```
pipenv python3 main.py <slackHook>
```


or


Set up an environment variable file to use the included makefile
```
*create/open a file called '.env' that contains the following*
HOOK='<INSERT YOUR MAIN HOOK HERE>'
DEVHOOK='<INSERT YOUR DEV HOOK HERE (OPTIONAL, USED FOR make toMe)>'
```

Run the script
```
make
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
