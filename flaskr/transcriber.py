from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi


class Transcriber():
    """
    Transcribes a video and stores it on the local file system.
    """

    def __init__(self):
        self.__data_dir = None

    # TODO: Find a way to pass this in the constructor.
    def set_data_path(self, data_dir: Path):
        self.__data_dir = data_dir

    def get_and_store_transcript(self, video_id: str):
        "Gets the transcript and store it."

        print(
            f'Fetching {video_id} transcript into directory {self.__data_dir}')
        transcripts = YouTubeTranscriptApi.get_transcript(video_id)
        captions_list = []
        for items in transcripts:
            captions_list.append(items['text'])
        transcript = '.'.join(captions_list)

        dest_dir = self.__data_dir / f'{video_id}' / 'transcript'
        dest_dir.mkdir(parents=True, exist_ok=True)

        # Create a file in |dest_dir| and write the transcript to it
        with open(dest_dir / 'transcript.txt', "w", encoding='utf-8') as file:
            file.write(transcript)

        print(transcript)
