# Croma Infrared for Home Assistant

> [!IMPORTANT]
> This is a preview of the Croma Infrared integration proposed for Home Assistant core in [home-assistant/core#187873](https://github.com/home-assistant/core/pull/187873). It already includes what is planned to follow that pull request, such as the remote's buttons. It uses the same `croma_infrared` domain, so your config entry and entities carry over. Once the core integration matches this one, this repository will be archived: remove it from HACS and restart, and the built-in integration takes over.

Control a Croma Google TV from Home Assistant through an infrared transmitter. Croma TVs are sold in India by Croma, the Tata Group electronics retailer.

Infrared only goes one way, so Home Assistant cannot read what the TV is doing. It remembers the last command it sent and restores that state after a restart, and the media player shows it as an assumed state.

## Supported devices

Verified with the Croma 43-inch 4K UHD QLED Google TV, 2026 model (CREL043UGQ024652), using the Google TV remote shipped with it. Croma ships the same remote with its other 2026 Google TV models, so they are likely to work too.

## Requirements

- Home Assistant 2026.10.0 or newer.
- An infrared transmitter set up in Home Assistant as an infrared entity, for example an ESPHome device with an IR LED and the infrared proxy, in line of sight of the TV.

## Entities

| Entity | Type | What it does |
| --- | --- | --- |
| Croma TV | media player | Turn on, turn off, volume up and down, mute, play, pause, stop, and select source. |
| Power | button | Sends the power key without changing the media player's state. Use it to bring the TV and Home Assistant back in step. |
| Up, Down, Left, Right, OK | button | Navigation. |
| Back, Exit, Home, Menu, Settings, Apps | button | The remote's keys of the same name. Exit acts like Back on this TV. |
| Input, Info, Guide | button | Source, Info and EPG keys. |
| Account, Voice, Subtitles | button | The remote's keys of the same name. Speaking to the assistant still needs the Bluetooth remote. |
| Program up, Program down | button | P+ and P-, for Live TV. |
| Fast forward, Rewind | button | Not on the remote, but the TV accepts them. |
| Free hotkey | button | Opens the app you assign to the free hotkey on the TV. |

Sources are YouTube, Netflix, Prime Video and Live TV. Selecting one sends the matching app key from the remote, which opens that app on the TV.

The Menu key and an unassigned Free hotkey are received by the TV (its standby light blinks) but do nothing on the tested model.

## Installation

### HACS (recommended)

This is a custom repository, so HACS has to be told about it once. After that it updates like any other HACS integration.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Dr-Blank&repository=croma-infrared-ha&category=integration)

Click the badge above, then **Download**. It fills the repository in for you.

If the badge does not work, add it by hand:

1. **HACS > ⋮ (top right) > Custom repositories**.
2. Repository `https://github.com/Dr-Blank/croma-infrared-ha`, type **Integration**, then **Add**.
3. Search HACS for **Croma Infrared** and **Download** it.

Either way, **restart Home Assistant** afterwards — custom integrations are only loaded at startup.

### Manual

Copy `custom_components/croma_infrared` into your Home Assistant `config/custom_components/` directory and restart Home Assistant.

### Setup

**Settings > Devices & services > Add integration > Croma Infrared**, then pick the infrared transmitter that can see the TV.

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=croma_infrared)

## Removal

Delete the integration from **Settings > Devices & services**, then remove it in HACS.

## Known limitations

- The TV has a single power key that switches between on and off, so turning it on and turning it off send the same key, even when Home Assistant already shows the state you asked for. An automation that turns off a TV that is already off turns it on; add a state condition to guard against that. The mute key works the same way.
- Presses on the physical remote are not tracked.
- Volume control is step-based only. You cannot set an absolute volume level.
- The TV's HDMI inputs cannot be selected directly, because the remote only has a key that opens the input menu.
- Mute and the current source are not restored after a restart.

## Troubleshooting

**The TV does not respond.** Infrared needs a clear line of sight to the TV's IR window, usually at the bottom edge of the screen. Point the transmitter at it, move it closer, and check that the infrared entity is available in Home Assistant.

**Home Assistant shows the wrong state.** Someone used the remote, or a command did not reach the TV. Use the action for the state you want: if the TV is on but Home Assistant shows it off, turn the media player off, and both agree again. Or press the **Power** button, which switches the TV without changing what Home Assistant shows.
