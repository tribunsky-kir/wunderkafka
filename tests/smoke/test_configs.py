import time
from typing import Any

import pytest
from pydantic import ValidationError

from wunderkafka import SRConfig, BytesConsumer, BytesProducer, ConsumerConfig, ProducerConfig
from tests.smoke.conftest import RawConfig


def test_init_consumer(boostrap_servers: str) -> None:
    config = ConsumerConfig(group_id="my_group", bootstrap_servers=boostrap_servers)
    consumer = BytesConsumer(config)
    print(consumer)

    with pytest.raises(AttributeError):
        consumer.config = ConsumerConfig(  # type: ignore
            group_id="my_other_group",
            bootstrap_servers=boostrap_servers,
        )
    assert consumer.config == config

    consumer.close()


def test_init_producer(boostrap_servers: str) -> None:
    config = ProducerConfig(bootstrap_servers=boostrap_servers)
    BytesProducer(config)


def test_init_no_krb_consumer(non_krb_config: RawConfig) -> None:
    config = ConsumerConfig(group_id="my_group", **non_krb_config)
    consumer = BytesConsumer(config)
    print(consumer)

    with pytest.raises(AttributeError):
        consumer.config = ConsumerConfig(  # type: ignore
            group_id="my_other_group",
            **non_krb_config,
        )
    assert consumer.config == config

    consumer.close()


def test_init_no_krb_producer(non_krb_config: RawConfig) -> None:
    config = ProducerConfig(**non_krb_config)
    BytesProducer(config)


def test_sr_required_url() -> None:
    with pytest.raises(ValidationError):
        SRConfig()


def test_group_id_required() -> None:
    with pytest.raises(ValidationError):
        ConsumerConfig()


def dummy_oauth_cb(_: Any) -> tuple:
    return "", int(time.time())


def test_init_consumer_oauth_cb(boostrap_servers: str) -> None:
    config = ConsumerConfig(group_id="my_group", bootstrap_servers=boostrap_servers, oauth_cb=dummy_oauth_cb)
    consumer = BytesConsumer(config)
    print(consumer)

    with pytest.raises(AttributeError):
        consumer.config = ConsumerConfig(  # type: ignore
            group_id="my_other_group",
            bootstrap_servers=boostrap_servers,
        )
    assert consumer.config == config

    consumer.close()


def test_init_producer_oauth_cb(boostrap_servers: str) -> None:
    config = ProducerConfig(bootstrap_servers=boostrap_servers, oauth_cb=dummy_oauth_cb)
    BytesProducer(config)
