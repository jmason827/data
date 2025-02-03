import os
global CWD
CWD = os.getcwd()

import logging
logging.basicConfig( 
    filename=os.path.join(CWD, f"{ __file__.split('.')[0] }.log"), 
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8',
    filemode='w',
)

from flask import Flask, render_template
app = Flask(__name__)

@app.get('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
