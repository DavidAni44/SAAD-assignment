---
status: "proposed"
date: {2024-21-11}
decision-makers: {Waris Ali, David  Ani, Connor Wright}
---

# Storage of user data

## Context and Problem Statement

How will we securely store user data so that it is properly encrypted

## Considered Options

* Symmetric Encryption
* Hashing


## Decision Drivers

* Scalability, the approach taken should be able to handle an increase in users
* Security, the approach should be as secure as possible in order to meet regulations
* Performance, the effect of securing the data shouldn't affect system speed 
* Integration, the approach taken should work well with the chosen languages (Python)

## Pros and Cons of the Options

### Symmetric Encryption

* Good as it's faster than other methods
* Bad due to a relience on key secrecy, if the key is shared outside the system than outsiders can access the data
* Bad as it isn't a scalable approach due to it being unsuited for larger user bases

### Hashing

* Good as it is a one-way approach, making it more secure
* Good as the output is of a fixed length, reducing storage size concerns and increasing scalability 
* Good as Python has built in hashing functionality 
* Bad as hash collisions may cause issues

### Confirmation

* Any page that takes sensitive inputs should have a hashing method implemented, this should be visible in the Github repository 

## Decision Outcome

Chosen option: Hashing

### Consequences

* Good as this will allow the system to be more scalable due to the fixed length of the data produced as well as needed less keys
* Good as it will be more secure than Symmetric Encryption
* Bad as it may be more complex to implement

### References

*  González, J. A. (n.d.). A Deep Dive into Encryption Types. Sealpath. https://www.sealpath.com/blog/types-of-encryption-guide/ 
* GeeksforGeeks. (n.d.). Difference between Hashing and Encryption. GeeksforGeeks. https://www.geeksforgeeks.org/difference-between-hashing-and-encryption/ 
* Pillsbury, D. (n.d.). Python Secure Password Management: Hashing and Encryption #️⃣🔐✨. DEV Community. https://dev.to/dpills/python-secure-password-management-hashing-and-encryption--1246 