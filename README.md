[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/AHFn7Vbn)
# Superjoin Hiring Assignment

### Welcome to Superjoin's hiring assignment! 🚀

### Objective
Build a solution that enables real-time synchronization of data between a Google Sheet and a specified database (e.g., MySQL, PostgreSQL). The solution should detect changes in the Google Sheet and update the database accordingly, and vice versa.

### Problem Statement
Many businesses use Google Sheets for collaborative data management and databases for more robust and scalable data storage. However, keeping the data synchronised between Google Sheets and databases is often a manual and error-prone process. Your task is to develop a solution that automates this synchronisation, ensuring that changes in one are reflected in the other in real-time.

### Requirements:
1. Real-time Synchronisation
  - Implement a system that detects changes in Google Sheets and updates the database accordingly.
   - Similarly, detect changes in the database and update the Google Sheet.
  2.	CRUD Operations
   - Ensure the system supports Create, Read, Update, and Delete operations for both Google Sheets and the database.
   - Maintain data consistency across both platforms.
   
### Optional Challenges (This is not mandatory):
1. Conflict Handling
- Develop a strategy to handle conflicts that may arise when changes are made simultaneously in both Google Sheets and the database.
- Provide options for conflict resolution (e.g., last write wins, user-defined rules).
    
2. Scalability: 	
- Ensure the solution can handle large datasets and high-frequency updates without performance degradation.
- Optimize for scalability and efficiency.

## Submission ⏰
The timeline for this submission is: **Next 2 days**

Some things you might want to take care of:
- Make use of git and commit your steps!
- Use good coding practices.
- Write beautiful and readable code. Well-written code is nothing less than a work of art.
- Use semantic variable naming.
- Your code should be organized well in files and folders which is easy to figure out.
- If there is something happening in your code that is not very intuitive, add some comments.
- Add to this README at the bottom explaining your approach (brownie points 😋)
- Use ChatGPT4o/o1/Github Co-pilot, anything that accelerates how you work 💪🏽. 

Make sure you finish the assignment a little earlier than this so you have time to make any final changes.

Once you're done, make sure you **record a video** showing your project working. The video should **NOT** be longer than 120 seconds. While you record the video, tell us about your biggest blocker, and how you overcame it! Don't be shy, talk us through, we'd love that.

We have a checklist at the bottom of this README file, which you should update as your progress with your assignment. It will help us evaluate your project.

- [x] My code's working just fine! 🥳
- [] I have recorded a video showing it working and embedded it in the README ▶️
- [x] I have tested all the normal working cases 😎
- [x] I have even solved some edge cases (brownie points) 💪
- [x] I added my very planned-out approach to the problem at the end of this README 📜

## Got Questions❓
Feel free to check the discussions tab, you might get some help there. Check out that tab before reaching out to us. Also, did you know, the internet is a great place to explore? 😛

We're available at techhiring@superjoin.ai for all queries. 

All the best ✨.


## Developer's Section

#### Demo Video



#### Architecture 
![IMG_4023](https://github.com/user-attachments/assets/e27a06be-e5ee-4bbc-afd2-34cdfc3449c4)

- My Solution is built on event driven architecture using Kafka for high Scalability and performance.
- Achieved 10,000 edits in 75 - 90 sec.
- When there is edit in Google sheets, a trigger has been set up using AppScript(service provided by google) this will hit my local server with is exposed using ngrok. 
- The updated values will be sent to the kafka topic (Sheets2DB) 
- Consumer form the other end will recieve these values and update the database
- When there is change in MYSQL database, a trigger has been set up to update event log
- Producer(DB2Sheets) will poll for every 2 sec and push the data into kafka
- Conusmer will get those values and update the Google sheets using Google API (Rate limited)

#### Problems faced
* Finding out that I had to expose my server, the request was not sent from the browser but from GCP

#### Setup
* Create a virtual Enviornment if needed(preferred)
* Clone this repository
* Install all the dependencies

```
pip install -r requirements.txt
```
* Run Kafka the server (preferably with KRAFT)(for windows in command prompt)
```
.\bin\windows\kafka-server-start.bat .\config\kraft\server.properties
```

* Create two Kafka topics 
```
.bin\windows\kafka-topics.bat --create --topic Sheets2DB --bootstrap-server localhost:9092
.bin\windows\kafka-topics.bat --create --topic DB2Sheets --bootstrap-server localhost:9092
```




Install ngrok to expose local server (DB2Sheets-producer)
We need to expose the server to receive data when a Google Sheets trigger is sent from GCP.

* Run all the four services in four different terminals
```
python consumer_DB2Sheets.py
python consumer_Sheets2BD.py
python producer_DB2Sheets.py
python producer_Sheets2DB.py
```
* Expose the port 5000 
```
ngrok http 5000
```
* Update the Address in the app script(Google sheets) to hit the end point

* Setup MYSQL server and Google Sheets as required


