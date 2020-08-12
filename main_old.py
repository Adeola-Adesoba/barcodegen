from flask import Flask, render_template, request
import os
# from app import gen_mbc
PEOPLE_FOLDER = os.path.join('static')


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route("/", methods = ['GET', 'POST'])
def home():
    # return None
    # if request.method == 'POST':
    #     video_id = request.form['videoid']
    #     # gen_mbc(video_id)
    #     return render_template("index.html", image = video_id)
    # else:
    return render_template("index.html")


@app.route("/seun", methods = ['GET', 'POST'])
def seun():
    from app import gen_mbc
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

# if __name__ == "__main__":
#     app.run(debug=True) 
