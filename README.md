# 📤 Kafka Chat Producer CLI (`chat-pro`)

Kafka로 메시지를 전송하는 커맨드라인 도구입니다.  
`pdm`으로 개발하고 `chat-pro`라는 명령어로 실행할 수 있습니다.

---

## 📦 설치 및 실행

### 1. 프로젝트 클론

```bash
git clone https://github.com/your-repo/kafka-chat.git
cd kafka-chat
```

### 2. 의존성 설치

```bash
pdm install
```

> `pdm`이 없다면 [설치 가이드](https://pdm.fming.dev/latest/#installation)를 참고하세요.

### 3. CLI 등
록
```bash
pip install -e .
```

---

## 🚀 사용 방법

```bash
chatpro
```

### 실행 흐름:

1. Kafka bootstrap 서버 주소 입력 (예: `localhost:9092`)
2. Kafka 토픽 이름 입력 (예: `quickstart-events`)
3. 메시지 입력 (`exit` 입력 시 종료)
4. 메시지는 JSON 형식으로 Kafka에 전송됨

---

## 💬 예시

```bash
Kafka bootstrap 서버 주소 입력 : localhost:9092
Kafka 토픽 이름 입력 : test-topic
input your Message (You wanna exit? 'exit' Input)
✉️ User: 안녕하세요
📤 Sending...
✉️ User: exit
Nagaja.
✅ All messages have been sent. Program terminated. 이상 짜치는 영어였습니다.
```

---

## 📁 디렉토리 구조

```text
.
├── pyproject.toml
├── README.md
└── src/
    └── kafka_chat/
        ├── __init__.py
        └── chat_pro.py  ← CLI 실행 함수(chatpro) 정의
```

---

## 🛠 기술 스택

- Python 3.10+
- [kafka-python](https://github.com/dpkp/kafka-python)
- [pdm](https://pdm.fming.dev)
- tqdm (전송 상태 표시용)

---


