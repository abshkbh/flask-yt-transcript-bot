from pathlib import Path
from llama_index import (
    GPTSimpleVectorIndex,
    SimpleDirectoryReader,
    LLMPredictor,
    ServiceContext
)
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.chat_models import ChatOpenAI


class LLMStore():
    """
    Stores the LLM model i.e. "index" on the filesystem.
    """

    def __init__(self):
        self.__data_dir = None

    # TODO: Find a way to pass this in the constructor.
    def set_data_path(self, data_dir: Path):
        self.__data_dir = data_dir

    def get_model(self, video_id: str) -> GPTSimpleVectorIndex:
        llm_index_path = self.__data_dir / f'{video_id}' / 'index.json'
        if not llm_index_path.is_file():
            raise FileNotFoundError(f'model not found for {video_id}')
        print(f'Loading model for {video_id} from disk')
        return GPTSimpleVectorIndex.load_from_disk(llm_index_path)

    def create_model(self, video_id: str) -> GPTSimpleVectorIndex:
        print(f'Creating model for {video_id}')
        # Define LLM model to use.
        llm_predictor = LLMPredictor(llm=ChatOpenAI(
            temperature=0, model_name='gpt-3.5-turbo'))
        service_context = ServiceContext.from_defaults(
            llm_predictor=llm_predictor)

        # Load data to input to the LLM.
        video_dir_path = self.__data_dir / f'{video_id}'
        video_transcript_dir_path = video_dir_path / 'transcript'
        documents = SimpleDirectoryReader(
            video_transcript_dir_path).load_data()

        # Create the LLM index and cache it on the disk for next time.
        llm_index = GPTSimpleVectorIndex.from_documents(
            documents, service_context=service_context)
        # Save the index to the disk.
        llm_index_path = video_dir_path / 'index.json'
        llm_index.save_to_disk(llm_index_path)
        return llm_index
