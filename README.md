From my understanding I need to create a client service that uses the API examples in the assignment.
I've created the 2 methods removing_data, adding_data that are getting the data and the group and trying to update the nodes.
If I am getting 5xx error code or timeout I will try to roll back the request by checking if the data exists or not according to what we tried to do.
I am guessing that if the get method is returning data, that means that the adding data has successfully implemented. if it doesn't return data that means the there is no data on the nodes.
There is no method to check for partial data, if there was it would be better for me to implement the roll back - because then I will know if the the adding/removing was interrupted in the middle and where I should go from here.

In order to use my code you should use the methods: removing_data, adding_data.
when you want to add data use: adding_data method with the parameters group_id - an integer number which will be the group id and the data parameter which will be the data the will be stored on that group.
When you want to delete a group - you should use removing_data method with the parameter: group id so it will know which group to remove.