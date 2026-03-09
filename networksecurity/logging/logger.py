# NETWORKSECURITY/networksecurity/logging/logger.py

import logging
import os
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE)
os.makedirs(logs_path,exist_ok=True)

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# stdout으로도 출력 (docker logs로 확인 가능, 컨테이너 내부에서 로그 파일로도 확인 가능)
logging.getLogger().addHandler(logging.StreamHandler())