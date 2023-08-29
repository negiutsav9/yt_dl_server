from flask import Flask, jsonify, request, send_file
from pytube import YouTube
from flask_cors import CORS, cross_origin

app = Flask(__name__)

CORS(app, supports_credentials=True, allow_headers='Content-Type')

@app.route('/url', methods=['POST'])
@cross_origin(supports_credentials=True)
def createStream():
    global url
    url = request.json['url']
    return jsonify({'streams': 'recieved'})

@app.route('/data',methods=['GET'])
@cross_origin(supports_credentials=True)
def sendData():
    yt = YouTube(url)
    vaStreams = []
    voStreams = []
    audioStreams = []
    for stream in yt.streams.fmt_streams:
        if stream.resolution is None:
            audioStreams.append({'id':stream.itag, 'res':stream.resolution,'vc':stream.video_codec, 'ac':stream.audio_codec,'size':stream.filesize_mb})
        elif stream.audio_codec is None:
            voStreams.append({'id':stream.itag, 'res':stream.resolution,'vc':stream.video_codec, 'ac':stream.audio_codec,'size':stream.filesize_mb})
        else:
            vaStreams.append({'id':stream.itag, 'res':stream.resolution,'vc':stream.video_codec, 'ac':stream.audio_codec,'size':stream.filesize_mb})
    return jsonify({
        'title': yt.title,
        'url': url,
        'description': yt.description,
        'length': yt.length,
        'channel_url': yt.channel_url,
        'author': yt.author,
        'publish_date': yt.publish_date.strftime("%B %d, %Y"),
        'audioStream' : audioStreams,
        'videoOnlyStream' : voStreams,
        'videoAudioStream' : vaStreams
    })

@app.route('/download', methods=['POST'])
@cross_origin(supports_credentials=True)
def downloadStream():
    yt = YouTube(url)
    print(request.json)
    stream = yt.streams.get_by_itag(request.json['itag'])
    stream.download()

if __name__ == '__main__':
    app.run()
