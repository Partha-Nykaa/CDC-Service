from abc import ABC, abstractmethod
from confluent_kafka import Producer, Consumer, KafkaException

class KafkaConnectorFactory(ABC):
    @abstractmethod
    def create_kafka_connector(self, config):
        pass

class KafkaConnectorFactoryImpl(KafkaConnectorFactory):
    def create_kafka_connector(self, config):
        return KafkaConnector(config)

class KafkaConnector:
    def __init__(self, config):
        try:
            self.producer = Producer(config)
            self.consumer = Consumer(config)
        except KafkaException as e:
            print(f"Failed to initialize Kafka producer/consumer: {e}")
            raise

    def publish_message(self, topic, key, value):
        try:
            self.producer.produce(topic, key=key, value=value)
            self.producer.flush()
        except KafkaException as e:
            print(f"Failed to publish message: {e}")

    def consume_message(self, topics,timeout=1.0):
        self.consumer.subscribe(topics)
        try:
            msg = self.consumer.poll(timeout)
            if msg is None:
                return None
            if msg.error():
                raise KafkaException(msg.error())
            else:
                return msg
        except KafkaException as e:
            print(f"Failed to consume message: {e}")
        finally:
            self.consumer.close()

    def continuous_consume(self, topics,timeout=1.0):
        self.consumer.subscribe(topics)
        try:
          while True:
            msg = self.consumer.poll(timeout)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                print(f"Received message: {msg.value().decode('utf-8')}")
        except KafkaException as e:
          print(f"Failed to consume message: {e}")
        finally:
           self.consumer.close()