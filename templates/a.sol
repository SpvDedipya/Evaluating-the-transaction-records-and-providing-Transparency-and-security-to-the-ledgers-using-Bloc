//SPDX-License-Identifier:GPL-3.0
pragma solidity >=0.7.0<0.9.0;

contract UserValidation {
    // Declare a mapping to store users.
    mapping(address => User) public users;

    // Declare a struct to represent a user.
    struct User {
        string name;
        bool isValid;
    }

    // Declare a public variable to store the number of users.
    uint public userCount;

    // Declare a function to add a new user to the contract.
    function addUser(string memory _name) public {
        // Increment the user count.
        userCount++;

        // Add the new user to the mapping.
        users[msg.sender] = User({
            name: _name,
            isValid: true
        });
    }

    // Declare a function to validate a user.
    function validateUser(address _user) public {
        // Get the user from the mapping.
        User storage user = users[_user];

        // Set the user's isValid flag to true.
        user.isValid = true;
    }

    // Declare a function to invalidate a user.
    function invalidateUser(address _user) public {
        // Get the user from the mapping.
        User storage user = users[_user];

        // Set the user's isValid flag to false.
        user.isValid = false;
    }

    // Declare a function to check if a user is valid.
    function isValidUser(address _user) public view returns (bool) {
        // Get the user from the mapping.
        User storage user = users[_user];

        // Return the value of the user's isValid flag.
        return user.isValid;
    }
}