__author__ = 'vkostov'

from cement.core import foundation

app = foundation.CementApp('aws-prod')
try:
    app.setup()
    app.run()
    print('app starting')
finally:
    app.close()