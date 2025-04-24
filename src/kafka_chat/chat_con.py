import threading
import time
from kafka import KafkaProducer, KafkaConsumer
import json

# Kafka 설정
KAFKA_SERVER = "34.47.84.43:9092"  # 또는 GCP 외부 IP:9092
TOPIC_NAME = "quickstart-events"
GROUP_ID = "광진구 화이팅!"

def print_auto():
    # ✅ Kafka Consumer
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_SERVER,
        group_id=GROUP_ID,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )

    for message in consumer:
        try:
            payload = message.value
            print(f"\n📩 [받음] {payload['msg']}\n>>> ", end="")
        except Exception as e:
            print(f"\n⚠️ 메시지 파싱 실패: {e} | 원본 메시지: {message.value}\n>>> ", end="")

def chatcon():
    # ✅ Kafka Producer
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVER,
            value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8')
        )
    except Exception as e:
        print(f"❌ KafkaProducer 생성 실패: {e}")
        return

    # 백그라운드 Consumer 쓰레드 시작
    thread = threading.Thread(target=print_auto, daemon=True)
    thread.start()

    # 사용자 입력 → 메시지 전송
    while True:
        user_input = input(">>> ")
        if user_input.lower() == 'exit':
            print("프로그램 종료")
            break
        else:
            msg = {
            "user": GROUP_ID,
            "text": user_input
            }           
producer.send(TOPIC_NAME, msg)
            try:
                producer.send(TOPIC_NAME, msg)
                producer.flush()
            except Exception as e:
                print(f"⚠️ 메시지 전송 실패: {e}")

if __name__ == "__main__":
    chatall()

