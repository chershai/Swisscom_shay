import time
import httpx


class Client:
    def rolling_back(self, func, *args):
        """
        This function is rolling back changes that was made by the API request that failed
        :param func: the relevant api function to be called
        :param args: the arguments for the api function
        """
        relevant_status_code = 404 if args[2] == 'post' else 200
        try:
            while self._get_method(args[0]).status_code == relevant_status_code:
                func(args[0], args[1])
                time.sleep(1.5)
        except httpx.HTTPError as e:
            self.rolling_back(func, args)
        except Exception as e:
            return

    def _get_method(self, group_id: int):
        """
        This function is the post request function
        :param group_id: the group id we want to add
        :return: the response of the request
        """
        res = httpx.get(f'http://v1/group/{group_id}/')
        return res

    def _post_method(self, group_id: int, data: str):
        """
        This function is the post request function
        :param group_id: the group id we want to add
        :param data: the data we want to put in the group
        :return: the response of the request
        """
        res = httpx.post('http://v1/group/', json={group_id: data}, headers={"Content-Type": "application/json"})
        return res

    def _delete_method(self, group_id: int, data: str):
        """
        This function is the delete request function
        :param group_id: the group id we want to add
        :param data: the data we want to put in the group
        :return: the response of the request
        """
        res = httpx.delete(f'http://v1/group/{group_id}',
                           headers={"Content-Type": "application/json"})  # delete method doesn't have a request body
        return res

    def adding_data(self, group_id: int, data: str):
        """
        This function is for adding data to the nodes in the cluster, if the API has failed it will call
            the rollback function
        :param group_id: the group id we want to add
        :param data: the data we want to put in the group
        """
        try:
            res = self._post_method(group_id, data)
            if res.status_code >= 500:
                raise httpx.TimeoutException
        except (httpx.TimeoutException, httpx.UnsupportedProtocol) as e:
            self.rolling_back(self._delete_method, group_id, data, 'delete')
        return True

    def removing_data(self, group_id: int):
        """
        This function is for removing data from the nodes in the cluster, if the API has failed it will call
            the rollback function
        :param group_id: the group id we want to remove
        """
        response = self._get_method(group_id)
        data = response.json()['groupId']
        try:
            res = self._delete_method(group_id, data)
            if res.status_code >= 500:
                raise httpx.TimeoutException
        except (httpx.TimeoutException, httpx.UnsupportedProtocol) as e:
            self.rolling_back(self._post_method, group_id, data, 'post')
        return True
