import getopt
import sys
import config

from app import app

port = config.DEFAULT_PORT

try:
    opts, args = getopt.getopt(sys.argv[1:], "p:", ["port="])
    for option, argument in opts:
        if (option in '-p', 'port'):
            try:
                port = int(argument)
            except ValueError:
                pass
except getopt.GetoptError as error:
    pass

app.run(debug=True,
        port=port)
