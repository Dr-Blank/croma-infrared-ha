"""Common fixtures for the Croma Infrared tests."""

from collections.abc import Generator
from typing import override
from unittest.mock import MagicMock, patch

from infrared_protocols.commands import Command
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry
from pytest_homeassistant_custom_component.syrupy import HomeAssistantSnapshotExtension
from syrupy.assertion import SnapshotAssertion

from homeassistant.components.infrared import DATA_COMPONENT, InfraredEmitterEntity
from homeassistant.components.infrared.const import DOMAIN as INFRARED_DOMAIN
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component

from custom_components.croma_infrared import PLATFORMS
from custom_components.croma_infrared.codes import CromaTVCode
from custom_components.croma_infrared.const import (
    CONF_INFRARED_EMITTER_ENTITY_ID,
    DOMAIN,
)

MOCK_INFRARED_EMITTER_ENTITY_ID = "infrared.test_ir_emitter"


class MockInfraredEmitterEntity(InfraredEmitterEntity):
    """Infrared emitter that records what it was asked to send."""

    _attr_has_entity_name = True
    _attr_name = "Test IR emitter"
    _attr_unique_id = "test_ir_emitter"

    def __init__(self) -> None:
        """Initialize the emitter."""
        self.send_command_calls: list[Command] = []

    @override
    async def async_send_command(self, command: Command) -> None:
        """Record the command."""
        self.send_command_calls.append(command)


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations: None) -> None:
    """Load the integration from custom_components."""


@pytest.fixture
def snapshot(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    """Serialize snapshots the way Home Assistant core does.

    The syrupy plugin registers its own ``snapshot`` fixture after
    pytest-homeassistant-custom-component, so its override never takes effect.
    """
    return snapshot.use_extension(HomeAssistantSnapshotExtension)


@pytest.fixture
async def init_infrared(hass: HomeAssistant) -> None:
    """Set up the infrared integration."""
    assert await async_setup_component(hass, INFRARED_DOMAIN, {})
    await hass.async_block_till_done()


@pytest.fixture
async def mock_infrared_emitter_entity(
    hass: HomeAssistant, init_infrared: None
) -> MockInfraredEmitterEntity:
    """Add an infrared emitter entity."""
    entity = MockInfraredEmitterEntity()
    await hass.data[DATA_COMPONENT].async_add_entities([entity])
    assert entity.entity_id == MOCK_INFRARED_EMITTER_ENTITY_ID
    return entity


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Return a mock config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        entry_id="01JTEST0000000000000000000",
        title="Croma TV",
        data={CONF_INFRARED_EMITTER_ENTITY_ID: MOCK_INFRARED_EMITTER_ENTITY_ID},
        unique_id=MOCK_INFRARED_EMITTER_ENTITY_ID,
    )


@pytest.fixture
def platforms() -> list[Platform]:
    """Return platforms to set up."""
    return PLATFORMS


@pytest.fixture
def mock_croma_to_command() -> Generator[MagicMock]:
    """Patch ``CromaTVCode.to_command`` to return the code itself.

    This lets tests assert on the code enum rather than on raw NEC timings.
    """
    with patch.object(
        CromaTVCode,
        "to_command",
        autospec=True,
        side_effect=lambda self, **kwargs: self,
    ) as mock:
        yield mock


@pytest.fixture
async def init_integration(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_infrared_emitter_entity: MockInfraredEmitterEntity,
    mock_croma_to_command: MagicMock,
    platforms: list[Platform],
) -> MockConfigEntry:
    """Set up the Croma Infrared integration for testing."""
    mock_config_entry.add_to_hass(hass)

    with patch("custom_components.croma_infrared.PLATFORMS", platforms):
        await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

    return mock_config_entry
