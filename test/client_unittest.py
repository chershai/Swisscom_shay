import time
import unittest
import httpx
from unittest import mock
from src.api_client import Client


class ClientUnittest(unittest.TestCase):

    @mock.patch("httpx.post")
    def test_post_method(self, mock_post_method):
        mock_post_method.return_value = httpx.Response(200, json={1: "passed"},
                                                       request=httpx.Request("POST", 'http://v1/group/'),)
        client = Client()
        assert client._post_method(1, "passed").status_code == 200

    @mock.patch("httpx.post")
    def test_adding_items(self, mock_post_method):
        mock_post_method.return_value = httpx.Response(
        200,
        json={1: "passed"},
        request=httpx.Request("POST", 'http://v1/group/'),
        )
        client = Client()
        assert client.adding_data(1, "passed") is True

    @mock.patch("httpx.delete")
    @mock.patch("httpx.get")
    @mock.patch("src.api_client.Client._get_method")
    @mock.patch("src.api_client.Client._delete_method")
    def test_removing_items(self, mock_delete_method, mock_get_method, mock_get_client, mock_delete_client):
        mock_delete_method.return_value = httpx.Response(
        200,
        json={'groupId': "passed"},
        request=httpx.Request("DELETE", 'http://v1/group/1/'),
        )
        mock_get_method.return_value = httpx.Response(
        200,
        json={'groupId': "passed"},
        request=httpx.Request("GET", "http://v1/group/1/"),
        )
        client = Client()
        mock_get_client.return_value = mock_get_method
        mock_delete_client.return_value = mock_delete_method
        while True:
            assert client.removing_data(1) is True
            time.sleep(60)



