#!/usr/bin/env python3

'''
usage:
    $(virtual_env) python app.py -> This runs the default test for a single video

    # Two youtube links are added one for a single video, the other one is a playlist. If you switch to playlist
    $(virtual_env) python app.py -> This runs the default playlist version of the script
                                |_> You can change the playlist url by adding the url parameter to command line

    $(virtual_env) python app.py --yturl "youtube playlist link"
                   |_> This may take time based on the video length or number of videos as well as internet speed

'''

import cv2                                                                                     # opencv version is 4.0.0
import numpy as np
import os, sys
import argparse
import datetime
import pafy
import yaml
import json
import pprint
import httplib2

# TODO: Accelerate video streaming?
# TODO: Make loggins with python logger
# TODO: Make path assigns with Python pathlib

# if you're lazy, you can use this url to test the code works for you.
# default_single = 'https://www.youtube.com/watch?v=E85arQdPNfs'
# default_single = 'https://www.youtube.com/watch?v=-fgmAEgwddk'
# default_playlist = 'https://www.youtube.com/playlist?list=PLhjLO-ekrsRvxL-aGqP82qgAgJlzKPDw7'

# command-line arguments -> for more info check the usage section (top of the file)


# config.yaml parse and assign to pafy api
def yaml_parser(yaml_file):
    import os
    # print('here', os.getcwd())
    # yaml_file =  os.getcwd()+'/static/config.yaml'
    with open(yaml_file) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data["key"]


# check if youtube link is a video list
def identify_url(url):
    status = "empty"
    if url is None:
        raise ValueError("url is empty!")
    elif "playlist" in url:
        if arg_verbose:
            print('vvveeerbose in playlist',arg_verbose)
            print("url is a playlist")
        status = "playlist"
    elif "watch" in url:
        if arg_verbose:
            print('vvveeerbose in watch',arg_verbose)
            print("url is a single video")
        status = "single"
    print('status',status)
    return status


# validate url to make sure the link is alive
def validate_url(url):
    c = httplib2.Http()
    resp = c.request(url, "HEAD")
    return int(resp[0]["status"])


# count number of frames that this video have
def frame_count(YTURL):
    """
    :param
        YTURL: youtube video url -> it should be a single video.
    :return:
        number of frames in the video

    :usage
        n_frames = frame_count(YTURL)
    """

    video = cv2.VideoCapture(YTURL)

    # if you have opencv 3 then call quick solution
    if int(cv2.__version__.split(".")[0]) == 4:
        if arg_verbose:
            print("[{} | INFO] Lucky! You have opencv 4.x version.".format(datetime.datetime.now().time()))
        num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    else:
        if arg_verbose:
            print("[{} | INFO] It seems you don't have opencv 3.x version.".format(datetime.datetime.now().time()))

        num_frames = 0

        while True:
            # read frame-by-frame where the show begins!
            ret, frame = video.read()
            num_frames += 1

    return num_frames


# get the best available youtube video url from pafy object
def get_url(YTURL):
    """
    :param
        YTURL: youtube video url -> it should be a single video.
    :return:
        best available download link of the video

    :usage
        best_specs.url = get_url(YTURL)
    """

    video_pafy = pafy.new(YTURL)
    # best_specs = video_pafy.getbest(preftype="webm")  # TODO: Make dynamic this step. get the most basic ones.
    best_specs = video_pafy.getbest()  # TODO: Make dynamic this step. get the most basic ones.

    # if arg_verbose:                                          # if you'd like to see the video url before download.
    #     print("[{} | INFO] YTURL: {}.".format(datetime.datetime.now().time(), best_specs.url))

    # print other information about video
    pp = pprint.PrettyPrinter(indent=2)

    print("-"*(len(video_pafy.title) + 18))
    print("| Video Title:    {}".format(video_pafy.title))
    print("| Video duration: {}".format(video_pafy.duration))
    print("| Video rating:   {}".format(video_pafy.rating))
    print("| Video author:   {}".format(video_pafy.author))
    print("| Video length:   {}".format(video_pafy.length))
    print("| Video url   :   {}".format(video_pafy.getbest().url))

    # print("| Video keywords: {}".format(video_pafy.keywords))            # if you would like to see keywords in a line

    # If you would like to visualize the object as dictionary
    # pprint.pprint(video_pafy, depth=1)

    print("| Video keywords:")
    pp.pprint(video_pafy.keywords)
    print("| Video thumb:    {}".format(video_pafy.thumb))
    print("| Video videoid:  {}".format(video_pafy.videoid))
    print("| Video viewcount:{}".format(video_pafy.viewcount))
    print("-"*(len(video_pafy.title) + 18))

    return video_pafy.getbest().url


# generate json and png files.
def generate_barcode(video):
    """
    :param
        video: video object.
    :return:
        average R, G, B values of each frame in a video

    :usage
        avgs = generate_barcode(video)
    """

    if video is None:
        raise ValueError("[{} | ERROR] video object is empty!".format(datetime.datetime.now().time()))

    # mean value for each frame of the video
    avgs = []

    while True:
        # get the frame
        (ret, frame) = video.read()

        if not ret:
            break

        if arg_display:
            cv2.imshow("video", frame)

        frame_avg = cv2.mean(frame)[:3]
        avgs.append(frame_avg)

    if arg_verbose:
        print("[{} | INFO] video barcode is ready. Size:{}".format(datetime.datetime.now().time(), len(avgs)))

    return avgs


# visualize the barcode on your screen
def vis_barcode(png_file_name=None):
    """
    :param
        None
    :return:
        None

    :usage
        Would you like to see the movie barcode on action?
    """

    # load the averages file and convert it to a NumPy array
    avgs = json.loads(open(arg_json).read())
    np_avgs = np.array(avgs, dtype="int")

    # grab the individual bar width and allocate memory for
    # the barcode visualization
    bw = 1
    barcode = np.zeros((250, len(np_avgs) * bw, 3), dtype="uint8")

    # loop over the averages and create a single 'bar' for
    # each frame average in the list
    for (i, avg) in enumerate(np_avgs):
        # cv2.rectangle(barcode, (int(i * bw), 0), (int((i + 1) * bw), 250), tuple(avg), 3)
        cv2.rectangle(barcode, (int(i * bw), 0), (int((i + 1) * bw), 250), (int(avg[0]), int(avg[1]), int(avg[2])), 3)

    # write the video barcode visualization to file and then
    # display it to our screen
    if arg_barcode is not None:
        cv2.imwrite(arg_barcode, barcode)

    if png_file_name is not None:
        cv2.imwrite(png_file_name, barcode)

    if arg_display:
        cv2.imshow("Barcode", barcode)  # TODO: Add another option to visualize the image such as PIL, or scikit-image
        cv2.waitKey(0)
        if sys.platform == "linux":
            cv2.destroyAllWindows()


# scan and parse playlist into a list of single youtube video links
def parse_playlist(playlist):
    # we believe the playlist is alive and it's a playlist url

    video_ids = []
    # get the request return for pafy object for playlist
    playlist_return = pafy.get_playlist(playlist)

    if arg_verbose:
        print("Number of videos in this play list: {}".format(len(playlist_return["items"])))

    for video in playlist_return["items"]:
        video_ids.append(video['pafy'].videoid)
        if arg_verbose:
            print("{} | {}".format(video['pafy'].videoid, video['pafy'].title))

    return video_ids



# Main function, like we have in many C based languages
# Heroku asked for commnad line arguments which could not be parsed
# so all arguments were removed and made Global variables in gen_mbc as shown below
def gen_mbc(video_id):
    global arg_json
    global arg_barcode
    global arg_verbose
    global arg_video
    global arg_display

    arg_json = None
    arg_video = True
    arg_verbose = 1
    arg_barcode = None
    arg_display = 0

    # home = os.path.join(os.getcwd(), "")
    home = os.getcwd()
    print('cwd------')

    # key = yaml_parser(home + r'\static\config.yaml')
    pafy.set_api_key(key='AIzaSyDK_7oWbudGzLl4VNxxO-CX_HgnfNzkhLA')

    # use an if statement to check if the length of the video id received is ==11 
    # then concatenate the video_id to a YouTube url
    if len(video_id)==11:
        yturl = f'https://www.youtube.com/watch?v={video_id}'
    else:
        yturl = video_id
    # yturl = f'{barcode}'

    print('-------',yturl)

    
    # Make sure video url is alive
    if validate_url(yturl) == 200:
        if arg_verbose:
            print("[{} | INFO] YouTube url is valid!.".format(datetime.datetime.now().time()))
    else:
        raise ValueError("[{} | ERROR] YouTube url is not valid!.".format(datetime.datetime.now().time()))

    # TODO: Call identify function to check if the video is playlist or a single video
    status = identify_url(yturl)
    if status == "single":
        # Do the steps for a single video
        # Verify experiment environment

        # output_directory = home + "\\static" + "\\" + yturl.split("=")[-1]
        # added an extra k to the folders to the due to the debugging
        output_directory = r'static/'+ yturl.split("=")[-1]+'k'

        print('here2', output_directory)
        if not os.path.exists(output_directory):
            os.mkdir(output_directory,0o775) # this is to solve the permission errors
            
        if arg_json is None:
            json_file = output_directory + "/" + yturl.split("=")[-1] + ".json"
            arg_json = json_file

        if arg_barcode is None:
            png_file = output_directory + "/" + yturl.split("=")[-1] + ".png"
            arg_barcode = png_file

        video_url = get_url(YTURL= yturl.split("=")[-1])
        print('videourl -----',video_url)
        num_frames = frame_count(video_url)

        video = cv2.VideoCapture(video_url)

        if arg_verbose:
            print("[{} | INFO] Number of frames: {}".format(datetime.datetime.now().time(), num_frames))

        # Write barcode data to json file
        # Check if the file is already available, delete it.
        static_path = os.getcwd() +'/'+ output_directory
        print("staic path >>>>>>>>..",static_path)
        # filenamejson =  yturl.split("=")[-1] + ".json"
        print('argjson>>>>>>>>',arg_json)

        if not os.path.exists(static_path):
            os.mkdir(static_path +'\\',0o775) # to solve the permisson error
            with open(os.getcwd() +'/'+arg_json, "w") as file:
                file.write(json.dumps(generate_barcode(video=video)))
                
        else:
            # os.remove(static_path+'\\',0o666)
            # os.mkdir(static_path+'\\',0o666)
            with open(os.getcwd() +'/'+arg_json, "w") as file:
                file.write(json.dumps(generate_barcode(video=video)))

        video.release()

        if arg_verbose:
            print("[{} | INFO] json file is being written to {}".format(datetime.datetime.now().time(), arg_json))

        vis_barcode()

    elif status == "playlist":
        video_ids = parse_playlist(yturl)
        # Do the steps for a playlist

        # Verify experiment environment
        for video_idx in video_ids:
            output_directory = home + "/static" + "/" + str(video_idx)
            print('here3', output_directory)
            if not os.path.exists(output_directory):
                os.mkdir(output_directory)
                if arg_verbose:
                    print("[{} | INFO] Output directory is created: {}".format(datetime.datetime.now().time(),
                                                                               output_directory))
            if arg_json is None:
                json_file = output_directory + "/" + str(video_idx) + ".json"
                arg_json = json_file
                if arg_verbose:
                    print("[{} | INFO] JSON file is assigned to : {}".format(datetime.datetime.now().time(), json_file))

            if arg_barcode is None:
                png_file = output_directory + "/" + str(video_idx) + ".png"
                arg_barcode = png_file
                if arg_verbose:
                    print("[{} | INFO] Barcode file is assigned to : {}".format(datetime.datetime.now().time(),
                                                                                png_file))

            video_url = 'https://www.youtube.com/watch?v=' + str(video_idx)
            if arg_verbose:
                print("[{} | INFO] Video url : {}".format(datetime.datetime.now().time(), video_url))

            # TODO: make a function after this line
            video_link = get_url(video_url)
            num_frames = frame_count(video_link)

            video = cv2.VideoCapture(video_link)

            if arg_verbose:
                print("[{} | INFO] Number of frames: {}".format(datetime.datetime.now().time(), num_frames))

            # Write barcode data to json file
            # Check if the file is already available, delete it.
            if not os.path.exists(arg_json):
                with open(arg_json, "w") as json_file:
                    json_file.write(json.dumps(generate_barcode(video=video)))
            elif os.path.exists(arg_json):
                os.remove(arg_json)
                with open(arg_json, "w") as json_file:
                    json_file.write(json.dumps(generate_barcode(video=video)))

            video.release()

            if arg_verbose:
                print("[{} | INFO] json file is being written to {}".format(datetime.datetime.now().time(), arg_json))

            vis_barcode(png_file_name=png_file)
            if arg_verbose:
                print("[{} | INFO] png file is being written to {}".format(datetime.datetime.now().time(), png_file))

            # free arguments for a new video
            arg_json = None
            arg_barcode = None


