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

* ##### Chosen option: Dynamo DB

* Reasoning - The data model for ALM is simple and DynamoDB suits simple data models because it’s optimized for quick, predictable access via primary keys. It also meets the non functional requirmenets for scalability as DynamoDB uses automatic partitioning for massive workloads, flexible capacity modes for predictable or spiky traffic, and multi-region replication via Global Tables for global low-latency access. DynamoDB also uses automatic scaling and serverless architecture meeting the fuctional requirements set out by the end users. DymnamoDB also has multi-region replication with global tables meaning real time notifications can be sent to users.
### Confirmation

* Check github repository, database will be in DynamoDB

### Consequences
*  Tt may lead to high costs for applications with unpredictable or extremely high traffic however ALM doesnt mention any cost contraints with regards to the new system and traffic volumes dont seem like they would majorily spike at any point. Also as a  AWS service, using DynamoDB may lead to vendor lock-in, making it challenging to migrate to other database systems or platforms in the future.

### References
* https://feeddi.com/why-is-mysql-not-scalable
* https://aspiringyouths.com/advantages-disadvantages/mysql/#google_vignette
* https://www.geeksforgeeks.org/mongodb-advantages-disadvantages/
* https://thinkcloudly.com/blogs/aws/advantages-disadvantages-aws-dynamodb/?v=7885444af42e
* https://docs.aws.amazon.com/dynamodb/
