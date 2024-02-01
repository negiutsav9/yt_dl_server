# YouTube Downloader
<em>A Next.js application which can download YouTube videos without advertisements and YouTube Premium</em>

[Run the YouTube Downloader](https://yt-dl-frontend.vercel.app/)

## Idea
I usually download YouTube videos and audio streams to enjoy music offline and without annoying advertisements. Furthermore, paying a regular subscription fee for a plan that works only on one device is not really well valued as I use more than one device. I explored many other YouTube downloaders such as SaveFrom and Online Video Downloader; however, one of the major drawbacks of these sites are the pop-up advertisements and illegitimate download buttons. I can understand that these sites uses advertisements to compensate the cost incurred during development and deployment, but these advertisements can be potentially mallicious and affect the performance of the device. Through this downloader, I want to offer a simple and minimalistic experience to the users without any annoying advertisements and additional subscriptions.

## Usage
- Enter the YouTube Link in the input field and select 'Retrieve'
- After the video is retrieved, the user can download the video as well as the audio stream in available formats

## Behind the Scenes

### Synopsis
The application uses Next.js as the frontend which is deployed on a Vercel server. Alongside, the application uses PyTube Python library to retrieve the information about the video, its available streams and to download the video itself. The process is wrapped within a REST API server built using Flask. The Flask server is deployed on a Render cloud service.

### Under the Hood
- The user enters the YouTube link and clicks on 'Retrieve' button.
- The link is send to the Flask server and the link is verified by the server and return any exception incurred when the link is being processed.
- If the link is clear of any exceptions, the server will return some video information and a list of streams available for download.
- These information are presented to the user on the frontend.
- On selecting the available streams, the id associated with the stream is send to the server.
- The video and audio stream is downloaded by converting the file into ByteStream and returned to the frontend.
- The frontend process the ByteStream as a Blob oject and then converts the file into mp4 for video and mp4a for audio.

## Potential Updates
The application has a potential to download video from other sites such as Facebook, Vimeo and Instagram. Furthermore, the application currently supports lower resolution videos as the server is sending PyTube progressive streams. PyTube does offer support for adaptive streams for higher resolution; however, a way has to be devised to combine the audio and video streams which are seperately provided by PyTube. 

## Reference
The source code for the Youtube Downloader front-end can be accessed here: [ytdl_downloader](https://github.com/negiutsav9/yt_downloader)
