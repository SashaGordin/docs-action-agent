import asyncio

import pytest

from docs_action_agent.provider import (
    FakeTextProvider,
    ProviderResult,
    ProviderTimeout,
    ProviderUsage,
)


def test_successful_fake_provider() -> None:
    usage = ProviderUsage(input_tokens=10, output_tokens=15)

    res = ProviderResult(answer="A land far far away", usage=usage)

    fake_provider = FakeTextProvider(res)
    assert asyncio.run(fake_provider.generate(question="where is the soap?")) == res


def test_failure_fake_provider() -> None:
    timeout = ProviderTimeout("provider timed out")

    fake_provider = FakeTextProvider(timeout)

    with pytest.raises(ProviderTimeout):
        asyncio.run(fake_provider.generate(question="boom"))
