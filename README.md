usage: start.py [-h] [--max-count MAX_COUNT] [--nseconds NSECONDS]
                [--timeout TIMEOUT]
                host port

Утилита для проверки целостности и качества соединений в сетях на основе
TCP/IP

positional arguments:
  host                  host of server
  port                  target port

optional arguments:
  -h, --help            show this help message and exit
  --max-count MAX_COUNT
                        maximum count of requests DEFAULT: 100
  --nseconds NSECONDS   count seconds between sending requests DEFAULT: 1
  --timeout TIMEOUT     maximum seconds for waiting server receive DEFAULT: 2
