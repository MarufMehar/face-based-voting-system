## Overview
The Face Recognition Voting System is a biometric-based e-voting application designed to provide a secure and efficient voting experience. The system uses face recognition technology to authenticate voters, ensuring that only registered individuals can cast their votes. This project aims to revolutionize the traditional voting process by leveraging advanced technologies, such as machine learning and computer vision, to enhance the accuracy, transparency, and integrity of elections.

The system consists of two primary components: the registration module and the voting module. In the registration module, users enroll by providing their Aadhar number, name, and country, and undergo a face capture process. The captured face data is then stored in a database for future reference. In the voting module, the user's face is recognized, and if authenticated, they are presented with a party selection interface to cast their vote.

This innovative system offers several benefits, including:

* **Efficient voter verification**: Face recognition technology ensures that only registered voters can participate in the election, reducing the risk of fraudulent activities.
* **Enhanced voter experience**: The system provides a convenient and user-friendly interface for voters to cast their votes, reducing waiting times and improving overall satisfaction.
* **Increased transparency and accuracy**: The automated voting process minimizes human error and ensures that votes are accurately recorded and counted.

Overall, the Face Recognition Voting System has the potential to transform the electoral process, promoting greater trust, security, and efficiency in democratic elections.
## INSTALLATION

To set up and run the Face Recognition Voting System, follow these steps:

### Prerequisites

* Python 3.x (tested on Python 3.9)
* pip package manager
* OpenCV (cv2) library
* tkinter and ttk for GUI
* sklearn for KNeighborsClassifier
* win32com.client for text-to-speech functionality
* PIL for image processing

### Installation Steps

1. **Install required packages**:
	* Open a terminal or command prompt and run the following command:
	```
	pip install opencv-python tk messagebox pillow scikit-learn pywin32
	```
	* Alternatively, you can install packages individually using pip.
2. **Clone the repository**:
	* Clone this repository to a local directory using Git or download the ZIP file.
3. **Navigate to the project directory**:
	* Open a terminal or command prompt and navigate to the project directory.
4. **Run the application**:
	* Run the `voting_system.py` script using Python:
	```
	python voting_system.py
	```
	* The Face Recognition Voting System GUI will launch.

Remember to register a new voter by providing the required information and capturing their face. The system will then allow the registered voter to vote.
## FEATURES

### Face Recognition Voting System

This system provides a robust and secure face recognition-based voting system that ensures accurate and efficient voting processes.

### Advanced Face Capture and Recognition Technology

The system utilizes advanced face capture and recognition technology, powered by OpenCV, to detect and recognize faces in real-time, ensuring high accuracy and speed.

### Multi-Party Support

The system supports multiple parties, allowing voters to select from a variety of parties, including BJP, CONGRESS, AAP, and NONE.

### Real-Time Voting and Results

The system provides real-time voting and results, allowing voters to submit their votes and view the results instantly.

### Secure and Reliable Data Storage

The system stores voter data, face data, and vote data securely and reliably, ensuring the integrity and confidentiality of the voting process.

### User-Friendly Interface

The system features a user-friendly interface, making it easy for voters to register, vote, and view results.

### Speech Assistance

The system provides speech assistance, allowing voters to receive audio feedback during the voting process.