#!/usr/bin/env python3

# 発表資料を見て FIXME の部分を修正しましょう

import pulsar
import logging
from employee import Employee, employeeSchema

# log level を設定
# client を作成
logger = logging.getLogger('pulsar')
logger.setLevel('INFO')
client = pulsar.Client('pulsar://pulsar:6650', logger=logger)

# 先程作った tenant と namespace 上の topic に subscribe する consumer を作る
# topic は自動で作られる
#topic = 'persistent://my-tenant/my-namespace/my-topic'
#consumer = client.subscribe(topic, 'my-subscription')
topic = 'persistent://my-tenant/my-namespace/schema-topic'
consumer = client.subscribe(topic=topic, subscription_name='my-subscription', schema=employeeSchema)

print('sending message')

# producer を作り、message を送信する
#producer = client.create_producer(topic)
producer = client.create_producer(topic=topic, schema=employeeSchema)
# byte 列として message を送信する
#producer.send('hello!'.encode())
producer.send(Employee(id_=100, firstName='Taro', lastName='Yamada', title='Manager'))

print('receiving message')

# message を受信する
message = consumer.receive()
#print(f'id: {message.message_id()}, data: {message.value().decode()}')
print(message.value())
print(f'firstName: {message.value().firstName}')

# acknowledge (受信した事を broker に通知) する
# これをしないと message は broker から削除されない (設定によっては再送される)
consumer.acknowledge(message)

# 最後に client, producer, consumer を閉じる
# 閉じないと program 終了後も接続が残る
producer.close()
consumer.close()
client.close()
