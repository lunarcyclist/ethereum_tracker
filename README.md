Ethereum Deposit Tracker
This project is an Ethereum Deposit Tracker application that monitors and records ETH deposits to the Beacon Deposit Contract in real-time. The application uses Alchemy’s API to query blockchain data and supports both contract-based and regular deposit transactions.

This Ethereum Deposit Tracker allows you to:
Track ETH deposits in real-time.
Differentiate between contract-based and regular transactions.
Fetch transaction data and display it in the terminal.
The tracker uses Alchemy’s API to interact with the Ethereum blockchain and the Beacon Deposit Contract. It continuously monitors new blocks and analyzes the transactions for deposits.

Prerequisites:
Before running the Ethereum Deposit Tracker, ensure you have the following installed:
Python 3.7+
pip
You’ll also need an Alchemy API key to query Ethereum blockchain data.

Setup Instructions
1. Create an Alchemy Account
Go to Alchemy's website.
Sign up for a free account.
Once signed in, create a new Ethereum application:
Go to the Dashboard.
Click on Create App.
Select Ethereum Mainnet as the network.
Once created, you will get an API key. This will be used in the project.
2. Clone the Repository
Next, clone the repository that contains the Ethereum Deposit Tracker code. Use the following command to clone the repository:bash, Copy code: git clone https://github.com/your-username/ethereum-deposittracker.gitcd ethereum-deposit-tracker
3. Install Dependencies
Navigate to the root folder of the project and install the required dependencies by running:


4. Configure API Keys
Inside your cloned repository, locate or create the configuration file for storing your API key. In the current project structure, the API key is hardcoded, but it can be externalized to make things cleaner.

In the script:
Copy code
ALCHEMY_API_URL = 'https://eth-mainnet.g.alchemy.com/v2/your-alchemy-api-key'
Replace 'your-alchemy-api-key' with the key you obtained from Alchemy.

Real-Time Monitoring:
The script runs in an infinite loop, checking for new blocks every 10 seconds. For each block, it fetches all transactions, checks if they are deposits to the Beacon Deposit Contract, and prints relevant transaction details.


Error Handling:
The script handles basic error scenarios such as:

Failed API requests – If the request to Alchemy’s API fails, an error message is printed, but the tracker continues to monitor for deposits.
Invalid Transactions – If no value is found in a transaction, the script will skip handling that transaction.
If you encounter SSL errors, make sure you have a stable internet connection, and that your system's SSL certificates are up to date.


