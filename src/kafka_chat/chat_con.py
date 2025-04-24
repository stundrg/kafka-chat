import threading
import time
from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
from datetime import datetime
import sys

def create_producer(server_ip: str) -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=f"{server_ip}:9092",
        value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode("utf-8")
    )

def create_consumer(server_ip: str, topic: str) -> KafkaConsumer:
    return KafkaConsumer(
        topic,
        bootstrap_servers=f'{server_ip}:9092',
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        group_id=None,  # 각자 모든 메시지 수신
    )

def get_formatted_msg(msg: str) -> str:
    now = datetime.now().strftime("%H:%M")
    return f"[{now}] {msg}"

def end_chat(producer: KafkaProducer):
    producer.flush()
    producer.close()

    print("Good bye!")
    sys.exit()

def show_chat(consumer: KafkaConsumer):
    try:
        for msg in consumer:
            value = msg.value
            if 'msg' in value:
                print(f"{value['user']}: {value['msg']}")
            else:
                print(f"ERROR: {value['error']}")
    except Exception:
        print("Good bye!")
    finally:
        consumer.close()


def main():
    print("Chat program")

    server_ip = input("Server IP: ")
    topic = input("Topic name: ")
    nickname = input("Your nickname: ")

    producer = create_producer(server_ip)
    consumer = create_consumer(server_ip, topic)

    # 백그라운드 쓰레드 시작
    thread = threading.Thread(target=show_chat, args=(consumer,), daemon=True)
    thread.start()

    # 사용자 입력 받기
    print("메시지를 입력하세요 (종료하려면 'exit' 입력)")

    try:
        while True:
            msg = input()
            if msg.lower() == "exit":
                break

            msg = get_formatted_msg(msg)
            producer.send(topic, {"user": nickname, "msg": msg})
            producer.flush()
    except Exception as e:
        error_msg = get_formatted_msg(f"An error occurred: {str(e)}")
        producer.send(topic, {"user": nickname, "error": error_msg})
    finally:
        end_chat(producer)

