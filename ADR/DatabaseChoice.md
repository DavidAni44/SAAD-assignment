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

* Scalability - The application needs to be scalable currently with 20% of England's population using ALM with an expected growth of 10% annually and have no downtime while scaling
* Availability - Maintain consistent performance and Ensure high availability
* Autonomy - Automatically scale up server capacity & databases

## Considered Options

* Dynamo DB 
* Mongo DB 
* MySQL

## Pros and Cons of the Options
### Dynamo DB
#### Pros
* Scalability and Avaliability - DynamoDB automatically scales up or down based on demand, making it ideal for applications with variable or unpredictable workloads. It also offers Global Tables, which automatically replicate data across multiple AWS regions, enabling high availability, low latency, and disaster recovery.
* Performance - Single-Digit Millisecond Latency  - DynamoDB is optimized for low-latency performance, making it an excellent choice for real-time applications.
* Schema-Less Data Storage - DynamoDB uses a schema-less model, storing data in JSON-like format and allowing each item to have different attributes
#### Cons
* Limited Query Capabilities - DynamoDB lacks support for complex joins, aggregations, and SQL-like queries, Queries are limited to key-value lookups or specific indexing.
* AWS Lock-In - DynamoDB is proprietary to AWS, so organizations using it may face vendor lock-in. Migrating to another database system can be complex and costly, making it challenging to leave the AWS ecosystem.
* Data Size Limitations - The maximum size limit for each object in DynamoDB is 400 KB

### Mongo DB
#### Pros
* Efficient Memory Utilization - MongoDB uses internal memory for data storage. So, it accesses the data very fast and enhances the overall performance
* Replication and Workload Distribution - By making copies of data and spreading the work across different parts, MongoDB ensures that the information is always available and the system works really fast
* JSON-Like Document Storage - MongoDB’s JSON-like document structure is intuitive for developers, especially those familiar with JavaScript and front-end web development.

#### Cons
* Document Size Limit - MongoDB imposes a maximum document size limit of 16 MB
* Limited Consistency Guarantees -  MongoDB’s eventual consistency model can lead to potential data inconsistencies in sharded or distributed environments
* Lack of Support for ACID Transactions - MongoDB’s ACID compliance is limited to single-document transactions
  
### MySQL
#### Pros
* High Performance – MySQL can handle large amounts of data and traffic without slowing down
* User-Friendly - MySQL is known for being relatively easy to install, set up, and manage, especially for new users
* Strong Security Features – MySQL offers strong security features, including user authentication, encryption, and access control


#### Cons
* Poor Performance in High Loads -  for such high volumes of data MySQL does not provide adequate support for reading/write operations
* Single Point of Failure - MySQL uses a master-slave replication model by default, where all writes go to a single master server. This can create a bottleneck and limit scalability, as the master server can become a single point of failure.
* Data Consistency - Replication Lags in master-slave setups, leading to delays in data consistency across instances, especially under heavy load.

## Decision Outcome

* ##### Chosen option: MongoDB with Four Databases

* Reasoning - MongoDB was selected for its ability to meet scalability and availability requirements while providing a developer-friendly, JSON-like document model. By utilizing four separate MongoDB databases, we can achieve:

    - Efficient Data Partitioning: Workloads can be distributed across databases for optimized performance.

    - Scalability: MongoDB’s horizontal scaling and sharding capabilities allow us to handle anticipated growth efficiently.

    - High Availability: Built-in replication and workload distribution ensure system uptime and resilience.

    - Ease of Development: The JSON-like document structure aligns well with our development practices, improving productivity.

Although DynamoDB offers robust scalability and low-latency performance, its AWS lock-in and limited querying capabilities posed significant constraints. MySQL was less suitable due to its performance challenges with high volumes of data and single-point failure risks.

### Confirmation

* Check github repository, database will be in database.py file using the pymongo library 

### Consequences
*   Cost Implications: While MongoDB is cost-effective compared to DynamoDB, scaling across multiple databases will require infrastructure and resource planning.
*   Operational Complexity: Managing four databases may introduce complexity in terms of setup, monitoring, and maintenance
*   Data Model Flexibility: The schema-less nature of MongoDB allows for rapid iteration but can lead to unstructured or inconsistent data if not managed properly.

### References
* Advantages and Disadvantages of MongoDB (https://www.geeksforgeeks.org/mongodb-advantages-disadvantages/)
* Why MySQL is Not Scalable (https://feeddi.com/why-is-mysql-not-scalable)
* DynamoDB Overview and Limitations (https://docs.aws.amazon.com/dynamodb/)
* Challenges of Using NoSQL Databases (https://thinkcloudly.com/blogs/aws/advantages-disadvantages-aws-dynamodb/)
