---
# These are optional metadata elements. Feel free to remove any of them.
status: "proposed"
date: {2024-10-10}
decision-makers: {Connor Wright, Waris Ali, David Ani}
---

# How will the Database be designed

## Context and Problem Statement
What database will be used to store data for our solution? What database will be the most optimum for the requirements of the system? This is where all data 

## Decision Drivers

* Scalability - The application needs to be scalable currently with 20% of England's population using AML with an expected growth of 10% annually and have no downtime while scaling
* Avalability - Maintain consistent performance and Ensure high availability
* Autonomy - Automatically scale up server capacity & databases

## Considered Options

*Dynamo DB 
*Mongo DB 
*MySQL

## Pros and Cons of the Options
### Dynamo DB
# Pros

# Cons
### Mongo DB
# Pros

# Cons
### MySQL
# Pros
* High Performance – MySQL can handle large amounts of data and traffic without slowing down
* User-Friendly - MySQL is known for being relatively easy to install, set up, and manage, especially for new users
* Strong Security Features – MySQL offers strong security features, including user authentication, encryption, and access control


# Cons
* Poor Performance in High Loads -  for such high volumes of data MySQL does not provide adequate support for reading/write operations
* Single Point of Failure - MySQL uses a master-slave replication model by default, where all writes go to a single master server. This can create a bottleneck and limit scalability, as the master server can become a single point of failure.
* Data Consistency - Replication Lags in master-slave setups, leading to delays in data consistency across instances, especially under heavy load.

## Decision Outcome

Chosen option: Dynamo DB

### Confirmation

* Check github repository, database will be in DynamoDB

### Consequences


### References
https://feeddi.com/why-is-mysql-not-scalable
https://aspiringyouths.com/advantages-disadvantages/mysql/#google_vignette

