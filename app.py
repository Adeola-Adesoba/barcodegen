from flask import Flask, render_template, request
import os
from main import gen_mbc


UPLOAD_FOLDER = os.path.join('static')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# UPLOAD_FOLDER ='static/'
# MYDIR = os.path.dirname(__file__)
# app = Flask(__name__, static_url_path="/static")

# APP CONFIGURATIONS
# app.config['SECRET_KEY'] = 'mbc'  
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024


@app.route("/", methods = ['GET', 'POST'])
def home():

    # return None
    # if request.method == 'POST':
    #     video_id = request.form['videoid']
    #     # gen_mbc(video_id)
    #     return render_template("index.html", image = video_id)
    # else:
    return render_template("index.html")


@app.route("/mbc_endpoint", methods = ['GET', 'POST'])
def mbc_endpoint():
    # return None
    # full_filename = os.path.join(a.config['UPLOAD_FOLDER'], 'g8vHhgh6oM0/g8vHhgh6oM0.png')
    # return render_template("index.html", user_image = full_filename)
    if request.method == 'POST':
        video_id = request.form['videoID']
        # full_filename = os.path.join(a.config['UPLOAD_FOLDER'], 'shovon.jpg')
        # return render_template("index.html", user_image = full_filename)
        # print('--------', video_id)
        gen_mbc(video_id)
        return video_id

        #
        # return render_template("index.html", image = video_id)
    else:
        return render_template("index.html")
        

if __name__ == "__main__":
    app.run(debug=True) 


