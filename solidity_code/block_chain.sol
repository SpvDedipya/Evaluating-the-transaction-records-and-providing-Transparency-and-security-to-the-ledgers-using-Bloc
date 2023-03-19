// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.2 <0.9.0;

contract GanacheAccountContract {
    
    struct Account {
        address accountAddress;
        string name;
        string aadharNumber;
        string email;
    }

    mapping (address => bool) private addressExists;
    mapping (string => bool) private aadharExists;
    mapping (string => bool) private emailExists;
    mapping (uint => Account) private accounts;
    uint private accountCount;

    function addAccount(address _accountAddress, string memory _name, string memory _aadharNumber, string memory _email) public {
        require(!addressExists[_accountAddress], "Account address already exists");
        bytes memory aadharBytes = bytes(_aadharNumber);
        require(aadharBytes.length == 12, "Invalid Aadhaar number length");
        bytes memory truncatedAadharBytes = new bytes(12);
        for (uint i = 0; i < 12; i++) {
            truncatedAadharBytes[i] = aadharBytes[i];
        }
        string memory truncatedAadharNumber = string(truncatedAadharBytes);
        require(!aadharExists[truncatedAadharNumber], "Aadhaar number already exists");
        
        bytes memory emailBytes = bytes(_email);
        bool emailValid = false;
        for (uint i = 0; i < emailBytes.length; i++) {
            if (emailBytes[i] == 0x40) { // '@' symbol in ASCII encoding
                emailValid = true;
                break;
            }
        }
        require(emailValid, "Invalid email address");

        require(!emailExists[_email], "Email already exists");

        accounts[accountCount] = Account(_accountAddress, _name, truncatedAadharNumber, _email);
        addressExists[_accountAddress] = true;
        aadharExists[truncatedAadharNumber] = true;
        emailExists[_email] = true;
        accountCount++;
    }

    function getAccount(uint _index) public view returns (address, string memory) {
        require(_index < accountCount, "Invalid index");
        Account storage account = accounts[_index];
        return (account.accountAddress, account.name);
    }

    function getAllAccounts() public view returns (address[] memory, string[] memory, string[] memory, string[] memory) {
        address[] memory accountAddresses = new address[](accountCount);
        string[] memory names = new string[](accountCount);
        string[] memory aadharNumbers = new string[](accountCount);
        string[] memory emails = new string[](accountCount);
        for (uint i = 0; i < accountCount; i++) {
            Account storage account = accounts[i];
            accountAddresses[i] = account.accountAddress;
            names[i] = account.name;
            aadharNumbers[i] = account.aadharNumber;
            emails[i] = account.email;
        }
        return (accountAddresses, names, aadharNumbers, emails);
    }

    function showAccountNames() public view returns (string[] memory) {
        string[] memory names = new string[](accountCount);
        for (uint i = 0; i < accountCount; i++) {
            Account storage account = accounts[i];
            names[i] = account.name;
        }
        return names;
    }

    function recieveEther() public payable {
    }
    
    function transferEther(address payable add,uint amt) public {
        add.transfer(amt);
    }

    function getAccountIndex(address accountAddress) private view returns (uint256) {
        for (uint256 i = 0; i < accountCount; i++) {
            if (accounts[i].accountAddress == accountAddress) {
                return i;
            }
        }
        return accountCount;
    }
}