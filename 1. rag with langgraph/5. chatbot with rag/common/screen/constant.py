import enum 


class ROLE_TYPE(enum.Enum):
  user = (enum.auto(), "사용자")
  assistant = (enum.auto(), "LLM 모델")

class HISTORY_INFO(enum.Enum):
  role = (enum.auto(), "메세지 생성자")
  content = (enum.auto(), "메세지")




