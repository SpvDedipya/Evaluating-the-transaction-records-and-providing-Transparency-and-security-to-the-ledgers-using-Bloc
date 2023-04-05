// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.2 <0.9.0;

contract GanacheAccountContract {
    
    struct Account {
        address accountAddress;
        string name;
        bytes32 aadharHash;
        bytes32 emailHash;
    }

    mapping (address => bool) private addressExists;
    mapping (bytes32 => bool) private aadharExists;
    mapping (bytes32 => bool) private emailExists;
    mapping (uint => Account) private accounts;
    uint private accountCount;

    function addAccount(address _accountAddress, string memory _name, string memory _aadharNumber, string memory _email) public {
        require(!addressExists[_accountAddress], "Account address already exists");

        bytes memory aadharBytes = bytes(_aadharNumber);
        require(aadharBytes.length == 12, "Invalid Aadhaar number length");

        bytes32 aadharHash = keccak256(aadharBytes);

        bytes memory emailBytes = bytes(_email);
        bool emailValid = false;
        for (uint i = 0; i < emailBytes.length; i++) {
            if (emailBytes[i] == 0x40) { // '@' symbol in ASCII encoding
                emailValid = true;
                break;
            }
        }
        require(emailValid, "Invalid email address");

        bytes32 emailHash = keccak256(emailBytes);

        require(!aadharExists[aadharHash], "Aadhaar number already exists");
        require(!emailExists[emailHash], "Email already exists");

        accounts[accountCount] = Account(_accountAddress, _name, aadharHash, emailHash);
        addressExists[_accountAddress] = true;
        aadharExists[aadharHash] = true;
        emailExists[emailHash] = true;
        accountCount++;
    }

    function getAccount(uint _index) public view returns (address, string memory) {
        require(_index < accountCount, "Invalid index");
        Account storage account = accounts[_index];
        return (account.accountAddress, account.name);
    }

    function getAllAccounts() public view returns (address[] memory, string[] memory, bytes32[] memory, bytes32[] memory) {
        address[] memory accountAddresses = new address[](accountCount);
        string[] memory names = new string[](accountCount);
        bytes32[] memory aadharHashes = new bytes32[](accountCount);
        bytes32[] memory emailHashes = new bytes32[](accountCount);
        for (uint i = 0; i < accountCount; i++) {
            Account storage account = accounts[i];
            accountAddresses[i] = account.accountAddress;
            names[i] = account.name;
            aadharHashes[i] = account.aadharHash;
            emailHashes[i] = account.emailHash;
        }
        return (accountAddresses, names, aadharHashes, emailHashes);
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
    
    function transferEther(address payable receiver, uint256 amount) public {
       require(addressExists[receiver], "Receiver address does not exist");
       receiver.transfer(amount);
    }


    
    function getAccountIndex(address accountAddress) private view returns (uint256) {
        for (uint256 i = 0; i < accountCount; i++) {
            if (accounts[i].accountAddress == accountAddress) {
                return i;
            }
        }
        return accountCount;
    }

    function verifyAccount(address _accountAddress, string memory _name, string memory _aadharNumber, string memory _email) public view returns (string memory) {
    bytes memory aadharBytes = bytes(_aadharNumber);
    require(aadharBytes.length == 12, "Invalid Aadhaar number length");
    bytes32 aadharHash = keccak256(aadharBytes);

    bytes memory emailBytes = bytes(_email);
    bool emailValid = false;
    for (uint i = 0; i < emailBytes.length; i++) {
        if (emailBytes[i] == 0x40) { // '@' symbol in ASCII encoding
            emailValid = true;
            break;
        }
    }
    require(emailValid, "Invalid email address");
    bytes32 emailHash = keccak256(emailBytes);

    uint accountIndex = getAccountIndex(_accountAddress);
    if (accountIndex == accountCount) {
        return "Sorry!! No account found"; // account does not exist
    }

    Account storage account = accounts[accountIndex];
    if (keccak256(bytes(account.name)) != keccak256(bytes(_name))) {
        return "Sorry!! Invalid account name"; // name does not match
    }
    if (account.aadharHash != aadharHash) {
        return "Sorry!! Invalid account aadhaar number"; // Aadhaar number does not match
    }
    if (account.emailHash != emailHash) {
        return "Sorry!! Invalid account email"; // email does not match
    }

    return "Yes!! Valid account details"; // all values match
}


}