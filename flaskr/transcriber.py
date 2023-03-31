from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi


class Transcriber():
    """
    Transcribes a video and stores it on the local file system.
    """

    def __init__(self, data_dir: Path):
        self.__data_dir = data_dir

    def get_and_store_transcript(self, video_id: str):
        "Gets the transcript and stored it. If already cached does nothing."

        dest_dir = self.__data_dir / f'{video_id}' / 'transcript'
        dest_dir.mkdir(parents=True, exist_ok=True)
        transcript_file = dest_dir / 'transcript.txt'
        if transcript_file.exists():
            print(
                f'Transcript for {video_id} exists at {transcript_file}')
            return

        print(
            f'Fetching {video_id} transcript into directory {self.__data_dir}')
        transcripts = YouTubeTranscriptApi.get_transcript(video_id)
        captions_list = []
        for items in transcripts:
            captions_list.append(items['text'])
        transcript = '.'.join(captions_list)
        print(f'{video_id} Transcript: {transcript}')

        # Write the transcript to the file.
        with open(transcript_file, "w", encoding='utf-8') as file:
            file.write(transcript)
