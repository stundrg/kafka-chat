import json
import time
from kafka import KafkaProducer

def chatpro():
    bootstrap_servers = input("Kafka bootstrap 서버 주소 입력 : ").strip()
    topic = input("Kafka 토픽 이름 입력 : ").strip()

    try:
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    except Exception as e:
        print(f"Kafka Producer Create Failed: {e}")
        return

    print("input your Message (You wanna exit? 'exit' Input)")

    while True:
        msg_input = input("✉️ User: ").strip()
        if msg_input.lower() == 'exit':
            print("Nagaja.")
            break

        msg = {"msg": msg_input}

        try:
            print("📤 Sending...")
            producer.send(topic, msg)
        except Exception as e:
            print(f"Sending Error: {e}")

    producer.flush()
    producer.close()
    print("✅ All messages have been sent. Program terminated. 이상 짜치는 영어였습니다.(_ _)")

if __name__ == "__main__":
    chatpro()

