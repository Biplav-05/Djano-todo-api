Feature: User Creation
    Scenario: Creating a User
    given the api is running
    when the user sends a POST request to '/accounts/create-user/' with the following data:
    |firstname           |lastname   |email            |password      |confirm_password |
    |Nirvan1               |Yonjan1    |nirvan1@example.com  |testpassword1 |testpassword1     |
    then the response status code should be 201