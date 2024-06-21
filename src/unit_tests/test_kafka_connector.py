import pytest
from unittest.mock import MagicMock, patch
from confluent_kafka import Producer, Consumer, KafkaException
from src.main.kafka_utils.kafka_connector import KafkaConnector

class TestKafkaConnector:
    @patch('confluent_kafka.Producer')
    @patch('confluent_kafka.Consumer')
    def setup_method(self, mock_consumer, mock_producer):
        config = {
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'mygroup',
            'auto.offset.reset': 'earliest',
        }
        self.kafka_connector = KafkaConnector(config)
        self.mock_producer = mock_producer
        self.mock_consumer = mock_consumer

    def test_publish_message(self):
        topic = 'test_topic'
        key = 'test_key'
        value = 'test_value'
        self.kafka_connector.publish_message(topic, key, value)
        self.mock_producer.produce.assert_called_once_with(topic, key=key, value=value)
        self.mock_producer.flush.assert_called_once()

    def test_consume_message(self):
        topics = ['test_topic']
        self.kafka_connector.consume_message(topics)
        self.mock_consumer.subscribe.assert_called_once_with(topics)
        self.mock_consumer.poll.assert_called_once()

    def test_continuous_consume(self):
        topics = ['test_topic']
        with pytest.raises(KafkaException):
            self.kafka_connector.continuous_consume(topics)
        self.mock_consumer.subscribe.assert_called_once_with(topics)
        self.mock_consumer.poll.assert_called()

    def teardown_method(self):
        self.kafka_connector = None
        self.mock_producer = None
        self.mock_consumer = None