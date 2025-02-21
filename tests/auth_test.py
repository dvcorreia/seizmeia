from __future__ import annotations

from datetime import timedelta
from io import StringIO

import yaml

from seizmeia.user.config import Config, EncryptionAlgorithm


def test_config_from_yaml():
    secret = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    doc = f"""
    secretKey: {secret}
    encrytionAlgorithm: HS256
    tokenExpirationTime: P7DT0H0M0S # ISO 8601
    """

    reader = StringIO(doc)

    conf = Config(**yaml.safe_load(reader))

    assert conf == Config(
        secretKey=secret,
        encrytionAlgorithm=EncryptionAlgorithm.HS256,
        tokenExpirationTime=timedelta(days=7),
    )
