from dotenv import load_dotenv
import os

load_dotenv()

DEEPSTACK_URL = os.getenv('DEEPSTACK_URL')
CAM_URL = os.getenv('CAM_URL')