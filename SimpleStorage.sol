// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0; // version

contract SimpleStorage {
    // this will be initialized to 0
    uint256 internal favoriteNumber; // index 0

    //------------------------------------------------------------------------------------------
    //creating a function to update favoriteNumber
    function store(uint256 _fav_num_) public returns(uint256) {
        favoriteNumber = _fav_num_;
        return favoriteNumber;
    }

    //------------------------------------------------------------------------------------------
    //view-> we are not making transactions we are only reading the value and pure-> cannot access the evironment variables and can only perform some pure maths
    function retrive() public view returns (uint256) {
        return favoriteNumber;
    }

    //------------------------------------------------------------------------------------------
    // creating a custom data type
    struct People {
        uint256 age; // index 0
        string name; // index 1
    }
    //creating a new variable using custom datatype
    People public person1 = People({age: 17, name: "Sambhav Kaushik"});
    //------------------------------------------------------------------------------------------
    // dynamic array
    People[] public users;
    //mapping
    mapping(string => uint256) public nameToAge;
    // fixed array-1
    People[1] public unique;

    // function to add a user to the array
    // memory(keyword) is used to store the data only when function is being executed
    // storage(keyword) is used to store the data even after the function is executed
    //string is solidity is not value type, it is actualy an array of bytes so we have to store it some where
    function addUser(uint256 _age, string memory _name) public {
        users.push(People({age: _age, name: _name}));
        nameToAge[_name] = _age;
    }
    //------------------------------------------------------------------------------------------
}
