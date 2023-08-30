from flask import Flask, jsonify, request, send_file
from pytube import YouTube, exceptions
from flask_cors import CORS, cross_origin
from io import BytesIO

app = Flask(__name__)

CORS(app, supports_credentials=True, allow_headers='Content-Type')

@app.route('/url', methods=['POST'])
@cross_origin(supports_credentials=True)
def createStream():
    global url
    url = request.json['url']
    try:
        yt = YouTube(url)
        test = yt.streams.fmt_streams
    except exceptions.AgeRestrictedError:
        return jsonify({'error': "Age Restricted"})
    except exceptions.ExtractError:
        return jsonify({"error": "Data Extraction Error"})
    except exceptions.LiveStreamError:
        return jsonify({"error": "Live Stream Error"})
    except exceptions.VideoUnavailable:
        return jsonify({'error': 'Video Unavailable'})
    return jsonify({"error": "None"})

@app.route('/data',methods=['GET'])
@cross_origin(supports_credentials=True)
def sendData():
    yt = YouTube(url)
    vaStreams = []
    voStreams = []
    audioStreams = []
    for stream in yt.streams.filter(only_audio=True).fmt_streams:
        audioStreams.append({'id':stream.itag, 'res':stream.resolution,'vc':stream.video_codec, 'ac':stream.audio_codec,'size':stream.filesize_mb})
    for stream in yt.streams.filter(progressive=True).fmt_streams:
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

@app.route('/download', methods=["POST"])
@cross_origin(supports_credentials=True)
def downloadStream():
    buffer = BytesIO()
    yt = YouTube(url)
    stream = yt.streams.get_by_itag(request.json['itag'])
    if stream.resolution is None:
        stream.stream_to_buffer(buffer)
        buffer.seek(0)
        res = send_file(buffer, as_attachment=True, download_name="audio.mp3")
        return res
    else:
        stream.stream_to_buffer(buffer)
        buffer.seek(0)
        res = send_file(buffer, as_attachment=True, download_name="video.mp4")
        return res

if __name__ == '__main__':
    app.run()
