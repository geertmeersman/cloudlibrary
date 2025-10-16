"""CloudLibraryClient module for Home Assistant integration.

This module provides a CloudLibraryClient class for interacting with
the Cloud Library API. It uses Home Assistant's aiohttp session and
does not manage its own session.

Usage:
    from .client import CloudLibraryClient
    client = CloudLibraryClient(barcode, pin, library, session)
    await client.login()
    data = await client.current()
"""

import logging
from urllib.parse import urlencode

from .const import BASE_URL, HEADERS

_LOGGER = logging.getLogger(__name__)


class CloudLibraryClient:
    """Cloud Library API client using Home Assistant's aiohttp session.

    This client requires a session from HA (`async_get_clientsession(hass)`)
    and does not manage its own session.
    """

    def __init__(
        self,
        barcode: str,
        pin: str,
        library: str,
        session,
        custom_headers: dict | None = None,
    ):
        """Initialize the CloudLibraryClient.

        Args:
            barcode (str): Patron barcode or email.
            pin (str): Patron PIN/password.
            library (str): Library ID.
            session (aiohttp.ClientSession): HA-managed aiohttp session.
            custom_headers (dict, optional): Optional headers to include in requests.

        """
        self.barcode = barcode
        self.pin = pin
        self.library = library
        self.session = session
        self.custom_headers = custom_headers or {}

    async def login(self) -> None:
        """Log in to the Cloud Library API using the provided session.

        Performs a two-step login:
        1. GET request to the library endpoint.
        2. POST request with login credentials.

        Raises:
            Exception: If any request fails.

        """
        data = {
            "action": "login",
            "barcode": self.barcode,
            "pin": self.pin,
            "library": self.library,
        }
        await self.request("GET", f"library/{self.library}", return_json=False)
        await self.request("POST", "?_data=root", data, return_json=False)

    async def request(
        self,
        method: str,
        path: str,
        data: dict | None = None,
        return_json: bool = True,
        expected_status: int = 200,
    ):
        """Send an HTTP request to the Cloud Library API.

        Args:
            method (str): HTTP method ("GET", "POST", etc.).
            path (str): Endpoint path (relative to BASE_URL).
            data (dict, optional): POST payload.
            return_json (bool): Return response as JSON if True.
            expected_status (int): Expected HTTP status code.

        Returns:
            dict | None: Response JSON or None if return_json is False.

        Raises:
            Exception: If the HTTP response code does not match expected_status.

        """
        endpoint = f"{BASE_URL}/{path}"

        if method.lower() == "get":
            async with self.session.get(
                endpoint, headers={**HEADERS, **self.custom_headers}
            ) as resp:
                if resp.status != expected_status:
                    raise Exception(f"GET {endpoint} failed with status {resp.status}")
                if return_json:
                    return await resp.json()
                return None

        async with self.session.post(
            endpoint,
            headers={**HEADERS, **self.custom_headers},
            data=urlencode(data or {}).replace("%27", "%22"),
        ) as resp:
            if resp.status != expected_status:
                raise Exception(f"POST {endpoint} failed with status {resp.status}")
            if return_json:
                return await resp.json()
            return None

    def get_path(self, route: str) -> str:
        """Generate the path for a specific user-related route.

        Args:
            route (str): Route identifier ("current", "holds", "history", "saved").

        Returns:
            str: Full path for the endpoint.

        """
        return f"library/{self.library}/mybooks/{route}?_data=routes/library.$name.mybooks.{route}"

    async def current(self):
        """Retrieve the patron's currently borrowed items.

        Returns:
            dict: JSON response containing current patron items.

        """
        return await self.request(
            "POST",
            self.get_path("current"),
            {"format": "", "sort": "BorrowedDateDescending"},
        )

    async def holds(self):
        """Retrieve the patron's holds.

        Returns:
            dict: JSON response containing patron holds.

        """
        return await self.request("POST", self.get_path("holds"), {"format": ""})

    async def history(self):
        """Retrieve the patron's borrowing history.

        Returns:
            dict: JSON response containing borrowing history.

        """
        return await self.request(
            "POST",
            self.get_path("history"),
            {"format": "", "sort": "BorrowedDateDescending", "status": ""},
        )

    async def saved(self):
        """Retrieve the patron's saved items.

        Returns:
            dict: JSON response containing saved items.

        """
        return await self.request(
            "POST", self.get_path("saved"), {"sort": "TitleAscending"}
        )

    async def featured(self):
        """Retrieve featured items from the library.

        Returns:
            dict: JSON response containing featured items.

        """
        return await self.request("GET", f"library/{self.library}/featured?_data=root")

    async def email(self):
        """Retrieve the patron's email settings.

        Returns:
            dict: JSON response containing email settings.

        """
        return await self.request(
            "GET", f"library/{self.library}/email?_data=routes%2Flibrary.%24name.email"
        )

    async def notifications(
        self, unread: str = "true", notification_id_to_archive: list | None = None
    ):
        """Retrieve or archive patron notifications.

        Args:
            unread (str): Filter for unread notifications ("true"/"false").
            notification_id_to_archive (list, optional): List of notification IDs to mark as archived.

        Returns:
            dict: JSON response containing notifications.

        """
        notification_id_to_archive = notification_id_to_archive or []
        path = f"library/{self.library}/notifications?_data=routes%2Flibrary.%24name.notifications"

        data = {"onlyUnread": unread}
        if notification_id_to_archive:
            data.update(
                {
                    "action": "markArchived",
                    "notificationIds": notification_id_to_archive,
                }
            )

        return await self.request("POST", path, data)
