import time
import httpx


def rolling_back(func, *args):
    """
    This function is rolling back changes that was made by the API request that failed
    :param func: the relevant api function to be called
    :param args: the arguments for the api function
    """
    relevant_status_code = 404 if args[2] == 'post' else 200
    try:
        while get_method(args[0]).status_code == relevant_status_code:
            func(args[0], args[1])
            time.sleep(1.5)
    except httpx.HTTPError as e:
        rolling_back(func, args)
    except Exception as e:
        return


def get_method(group_id: int):
    """
    This function is the post request function
    :param group_id: the group id we want to add
    :return: the response of the request
    """
    res = httpx.get(f'/v1/group/{group_id}/')
    return res


def post_method(group_id: int, data: str):
    """
    This function is the post request function
    :param group_id: the group id we want to add
    :param data: the data we want to put in the group
    :return: the response of the request
    """
    with httpx.Client() as client:
        res = client.post('/v1/group/', json={group_id: data}, headers={"Content-Type": "application/json"})
    return res


def delete_method(group_id: int, data: str):
    """
    This function is the delete request function
    :param group_id: the group id we want to add
    :param data: the data we want to put in the group
    :return: the response of the request
    """
    res = httpx.delete(f'/v1/group/{group_id}',
                       headers={"Content-Type": "application/json"})  # delete method doesn't have a request body
    return res


def adding_data(group_id: int, data: str):
    """
    This function is for adding data to the nodes in the cluster, if the API has failed it will call
        the rollback function
    :param group_id: the group id we want to add
    :param data: the data we want to put in the group
    """
    try:
        res = post_method(group_id, data)
        if res.status_code >= 500:
            raise httpx.TimeoutException
    except (httpx.TimeoutException, httpx.UnsupportedProtocol) as e:
        rolling_back(delete_method, group_id, data, 'delete')


def removing_data(group_id: int):
    """
    This function is for removing data from the nodes in the cluster, if the API has failed it will call
        the rollback function
    :param group_id: the group id we want to remove
    """
    response = get_method(group_id)
    data = response.json()['groupId']
    try:
        res = delete_method(group_id, data)
        if res.status_code >= 500:
            raise httpx.TimeoutException
    except (httpx.TimeoutException, httpx.UnsupportedProtocol) as e:
        rolling_back(post_method, group_id, data, 'post')



