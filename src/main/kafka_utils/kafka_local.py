from kafka_connector import KafkaConnectorFactoryImpl
class KafkaConnection:
    def __init__(self, config):
        factory = KafkaConnectorFactoryImpl()
        self.kafka_connector = factory.create_kafka_connector(config)
        print ("Kafka connection successful")

    def connection(self):
        # Define a test topic, key, and value
        test_topic = 'feed-topic-normal'
        test_key = 'test_key'
        test_value = 'test_value'

        # Publish the test message
        self.kafka_connector.publish_message(test_topic, test_key, test_value)
        print("publish successful")
        # Consume the test message
        message = None

        message = self.kafka_connector.consume_message([test_topic],5.0)
        #message = self.kafka_connector.continuous_consume([test_topic], 5.0)
        print(message.key().decode('utf-8'))


        # Verify that the consumed message matches the published message

        if message:
            assert message.topic() == test_topic
            assert message.key().decode('utf-8') == test_key
            assert message.value().decode('utf-8') == test_value
        else:
            raise Exception('Failed to consume message from Kafka')

        print('Kafka connection test passed.')


config = {
    'bootstrap.servers': '127.0.0.1:9092',
    'group.id': 'feed-cg',
    'auto.offset.reset': 'earliest',
}

test = KafkaConnection(config)
test.connection()