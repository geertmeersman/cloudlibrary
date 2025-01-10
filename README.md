<img src="https://github.com/geertmeersman/cloudlibrary/raw/main/images/brand/logo.png"
     alt="cloudLibrary"
     align="right"
     style="width: 200px;margin-right: 10px;" />

# cloudLibrary for Home Assistant

A Home Assistant integration to monitor cloudLibrary

## Features

cloudLibrary sensors for

- current(): Fetches the current patron items.
- history(): Retrieves the patron's borrowing history.
- holds(): Retrieves the patron's holds.
- saved(): Retrieves the patron's saved items.
- featured(): Retrieves the patron's featured items.
- email(): Retrieves the patron's email settings.
- notifications(): Retrieves patron notifications (unread or archived).

---

<!-- [START BADGES] -->
<!-- Please keep comment here to allow auto update -->

[![maintainer](https://img.shields.io/badge/maintainer-Geert%20Meersman-green?style=for-the-badge&logo=github)](https://github.com/geertmeersman)
[![buyme_coffee](https://img.shields.io/badge/Buy%20me%20an%20Omer-donate-yellow?style=for-the-badge&logo=buymeacoffee)](https://www.buymeacoffee.com/geertmeersman)
[![discord](https://img.shields.io/discord/1094198226493636638?style=for-the-badge&logo=discord)](https://discord.gg/QhvcnzjYzA)

[![MIT License](https://img.shields.io/github/license/geertmeersman/cloudlibrary?style=flat-square)](https://github.com/geertmeersman/cloudlibrary/blob/master/LICENSE)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=flat-square)](https://github.com/hacs/integration)

[![Open your Home Assistant instance and open the repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg?style=flat-square)](https://my.home-assistant.io/redirect/hacs_repository/?owner=geertmeersman&repository=cloudlibrary&category=integration)

[![GitHub issues](https://img.shields.io/github/issues/geertmeersman/cloudlibrary)](https://github.com/geertmeersman/cloudlibrary/issues)
[![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/geertmeersman/cloudlibrary.svg)](http://isitmaintained.com/project/geertmeersman/cloudlibrary)
[![Percentage of issues still open](http://isitmaintained.com/badge/open/geertmeersman/cloudlibrary.svg)](http://isitmaintained.com/project/geertmeersman/cloudlibrary)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](https://github.com/geertmeersman/cloudlibrary/pulls)

[![Hacs and Hassfest validation](https://github.com/geertmeersman/cloudlibrary/actions/workflows/validate.yml/badge.svg)](https://github.com/geertmeersman/cloudlibrary/actions/workflows/validate.yml)
[![Python](https://img.shields.io/badge/Python-FFD43B?logo=python)](https://github.com/geertmeersman/cloudlibrary/search?l=python)

[![manifest version](https://img.shields.io/github/manifest-json/v/geertmeersman/cloudlibrary/master?filename=custom_components%2Fcloudlibrary%2Fmanifest.json)](https://github.com/geertmeersman/cloudlibrary)
[![github release](https://img.shields.io/github/v/release/geertmeersman/cloudlibrary?logo=github)](https://github.com/geertmeersman/cloudlibrary/releases)
[![github release date](https://img.shields.io/github/release-date/geertmeersman/cloudlibrary)](https://github.com/geertmeersman/cloudlibrary/releases)
[![github last-commit](https://img.shields.io/github/last-commit/geertmeersman/cloudlibrary)](https://github.com/geertmeersman/cloudlibrary/commits)
[![github contributors](https://img.shields.io/github/contributors/geertmeersman/cloudlibrary)](https://github.com/geertmeersman/cloudlibrary/graphs/contributors)
[![github commit activity](https://img.shields.io/github/commit-activity/y/geertmeersman/cloudlibrary?logo=github)](https://github.com/geertmeersman/cloudlibrary/commits/main)

<!-- [END BADGES] -->

## Table of contents

- [cloudLibrary for Home Assistant](#cloudlibrary-for-home-assistant)
  - [Features](#features)
  - [Table of contents](#table-of-contents)
  - [Installation](#installation)
    - [Using HACS (recommended)](#using-hacs-recommended)
    - [Manual](#manual)
  - [Configuration](#configuration)
  - [Contributions are welcome!](#contributions-are-welcome)
  - [Troubleshooting](#troubleshooting)
    - [Enable debug logging](#enable-debug-logging)
    - [Disable debug logging and download logs](#disable-debug-logging-and-download-logs)
  - [Lovelace examples](#lovelace-examples)

## Installation

### Using [HACS](https://hacs.xyz/) (recommended)

**Click on this button:**

[![Open your Home Assistant instance and open the repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg?style=flat-square)](https://my.home-assistant.io/redirect/hacs_repository/?owner=geertmeersman&repository=cloudlibrary&category=integration)

**or follow these steps:**

1. Simply search for `cloudLibrary` in HACS and install it easily.
2. Restart Home Assistant
3. Add the 'cloudLibrary' integration via HA Settings > 'Devices and Services' > 'Integrations'
4. Provide your Robonect account details

### Manual

1. Copy the `custom_components/cloudlibrary` directory of this repository as `config/custom_components/cloudlibrary` in your Home Assistant installation.
2. Restart Home Assistant
3. Add the 'cloudLibrary' integration via HA Settings > 'Devices and Services' > 'Integrations'
4. Provide your cloudLibrary account details

This integration will set up the following platforms.

| Platform       | Description                               |
| -------------- | ----------------------------------------- |
| `cloudlibrary` | Home Assistant component for cloudLibrary |

## Configuration

The integration needs 3 inputs:

- barcode: Your cloudLibrary login
- pin: Your cloudLibrary password
- library id: Your cloudLibrary ID (this you can fetch from the url when you connect to the website: https://ebook.yourcloudlibrary.com/library/< HERE YOU FIND THE LIBRARY ID >/mybooks/current)

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Troubleshooting

### Enable debug logging

To enable debug logging, go to Settings -> Devices & Services and then click the triple dots for the cloudLibrary integration and click Enable Debug Logging.

![enable-debug-logging](https://raw.githubusercontent.com/geertmeersman/cloudlibrary/main/images/screenshots/enable-debug-logging.gif)

### Disable debug logging and download logs

Once you enable debug logging, you ideally need to make the error happen. Run your automation, change up your device or whatever was giving you an error and then come back and disable Debug Logging. Disabling debug logging is the same as enabling, but now you will see Disable Debug Logging. After you disable debug logging, it will automatically prompt you to download your log file. Please provide this logfile.

![disable-debug-logging](https://raw.githubusercontent.com/geertmeersman/cloudlibrary/main/images/screenshots/disable-debug-logging.gif)

## Lovelace examples

![current-books](https://raw.githubusercontent.com/geertmeersman/cloudlibrary/main/images/screenshots/current_books.png)

<details><summary>Show markdown code</summary>

```yaml
type: markdown
title: Current books
content: >-
  <table> {% for item in
  states.sensor.cloudlibrary_current.attributes.patron_items -%}
      <tr>
          <td width="140">
              <img height="180px" alt="{{ item.title }}" src="{{ item.imageLink }}">
          </td>
          <td valign="top">
              <strong>{{ item.title }}</strong><br>
              {% for author in item.contributors -%}
                  {% if 'name' in author -%}
                      <u>{{ author.name }}</u>&nbsp;
                  {% endif -%}
              {% endfor -%}
              <br><br>
              {% if item.borrowedDate != None -%}
                  Borrowed on <strong>{{ item.borrowedDate }}</strong><br>
              {% endif -%}
              {% if item.returnedDate != None -%}
                  Returned on <strong>{{ item.returnedDate }}</strong><br>
              {% endif -%}
              {% if item.dueDate != None -%}
                  Due on <strong>{{ item.dueDate }}</strong><br>
              {% endif -%}
              {% if item.holdAvailableDate != None -%}
                  Available on <strong>{{ item.holdAvailableDate }}</strong><br>
              {% endif -%}
          </td>
      </tr>
  {% endfor %} </table>
```

</details>
