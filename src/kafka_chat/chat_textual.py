from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Static, Input
from kafka import KafkaConsumer, KafkaProducer
from threading import Thread
from datetime import datetime
import json

# Kafka 설정
SERVER_IP = "34.22.64.33"
TOPIC = "quickstart-events"
USERNAME = "광진구 화이팅!"

class KafkaChatApp(App):
    CSS_PATH = "chat_ui.tcss"

    def compose(self) -> ComposeResult:
        self.chat_area = VerticalScroll(id="chat_area")
        yield self.chat_area
        yield Input(placeholder="메시지를 입력하세요...", id="chat_input")

    def on_mount(self):
        # Kafka Producer 생성
        self.producer = KafkaProducer(
            bootstrap_servers=f"{SERVER_IP}:9092",
            value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode("utf-8")
        )

        # Kafka Consumer 생성
        self.consumer = KafkaConsumer(
            TOPIC,
            bootstrap_servers=f"{SERVER_IP}:9092",
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            group_id=None,
            auto_offset_reset='earliest'
        )

        # 수신 쓰레드 시작
        Thread(target=self.consume_messages, daemon=True).start()

    def consume_messages(self):
        for msg in self.consumer:
            data = msg.value
            if data.get("user") != USERNAME:
                timestamp = datetime.now().strftime("%H:%M")
                display = f"[{data['user']} | {timestamp}] {data['msg']}"
                self.call_from_thread(self.display_message, display)

    def display_message(self, msg: str):
        # 아래쪽에 메시지 추가
        self.chat_area.mount_bottom(Static(msg))

    def on_input_submitted(self, event: Input.Submitted) -> None:
        message = event.value.strip()
        if message:
            timestamp = datetime.now().strftime("%H:%M")
            formatted_msg = f"[{timestamp}] {message}"

            self.producer.send(TOPIC, {
                "user": USERNAME,
                "msg": message
            })

            self.display_message(f"[나 | {timestamp}] {message}")
        event.input.value = ""

    def on_shutdown_request(self):
        self.producer.close()
        self.consumer.close()

if __name__ == "__main__":
    KafkaChatApp().run()

