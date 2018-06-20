"""OneSignal App Client class."""
from .base_client import OneSignalBaseClient


class OneSignalAppClient(OneSignalBaseClient):
    """OneSignal Client."""
    ENDPOINTS = {
        'notifications': 'notifications',
        "view_notifications":'notifications?app_id=%s',
        'cancel_notification': 'notifications/%s?app_id=%s',
        'csv_export': 'players/csv_export?app_id=%s'
    }

    AVAILABLE_EXTRA_FIELDS = ['location', 'country', 'rooted']

    def __init__(self, app_id, app_api_key):
        """
        Initializes the OneSignal Client.

        :param app_id: OneSignal App ID.
        Found under OneSignal Dashboard > App Settings > Keys & IDs
        :type app_id: string
        :param app_api_key: Application REST API key.
        Found under OneSignal Dashboard > App Settings > Keys & IDs
        :type app_api_key: string
        """
        self.app_id = app_id
        self.app_api_key = app_api_key
        self.mode = self.MODE_APP
    def get_notifications(self):
        endpoint = self.ENDPOINTS['view_notifications'] % (self.app_id)
        return self.get (self._url(endpoint))

    def get_headers(self):
        """
        Build default headers for requests.
        :return: Returns dict which contains the headers
        """
        return self._get_headers()

    def create_notification(self, notification):
        """
        Creates a new notification.
        :param notification: onesignalclient.notification.Notification object
        """
        payload = notification.get_payload_for_request()
        return self.post(self._url(self.ENDPOINTS['notifications']),
                         payload=payload)

    def cancel_notification(self, notification_id):
        """
        Cancel a notification.
        :param notification_id: Notification identifier
        """
        endpoint = self.ENDPOINTS['cancel_notification'] % (notification_id,
                                                            self.app_id)
        return self.delete(self._url(endpoint))

    def csv_export(self, extra_fields=[]):
        """
        Request a CSV export from OneSignal.
        :return: Returns the request result.
        """
        payload = {'extra_fields': []}

        if isinstance(extra_fields, list) and len(extra_fields) > 0:
            payload['extra_fields'] = [
                x for x in extra_fields if x in self.AVAILABLE_EXTRA_FIELDS
            ]

        endpoint = self.ENDPOINTS['csv_export'] % (self.app_id)
        return self.post(self._url(endpoint), payload=payload)
