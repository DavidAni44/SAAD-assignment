---
# These are optional metadata elements. Feel free to remove any of them.
status: "proposed"
date: {2024-10-10}
decision-makers: {Connor Wright, Waris Ali, David Ani}
---

# Choice of Backend Language

## Context and Problem Statement

What language will be used to code the backend of the solution in?
What language will be the most optimum for the requirements of the system? 
This is the main bulk of the code that will perform the various functions of the AML

## Decision Drivers

* Scalability, the system will need to be able to handle it if the demand grows
* Developer Profeciency, as this will affect not only the quality of code written but also the speed at which the system can be developed
* Integration, the chosen language needs to interact well both with the Architectural Style chosen as well as the front-end/database systems being used
* Performance, the chosen language should be ideal for large amounts of processing

## Considered Options

* C#
* PHP
* Python/Flask

## Pros and Cons of the Options

### C-Sharp

* Good as it can be used with the MVC Framework for web applications, which makes development more structured and is used in a wide array of web applications
* Good as documentation is easily avaialble
* Bad as development will be slower with unfamiliar developers

### PHP

* Good as it is specifically designed for web applications
* Good as developers are all already familiar with the language
* Bad as it is less effecient for heavy processing tasks
* Bad as PHP has security vulnerabilities

### Python/Flask

* Good as the framework is designed for web development
* Good as developers have familiarity with the language
* Good as Python is portable and can be run on on many different types of systems, allowing for easier development as we have developers on both Windows and Mac
* Bad due to reliance on external libraries


## Decision Outcome

Chosen option: Python/Flask due to the choice to make a Web App and its expanded functionality

### Confirmation

* Check github repository, backend files should all be written in python/Flask

### Consequences

* Good, because it will allow the solution to be coded faster due to developer pre-knowledge
* Good as it will avoid the security issues in PHP
* Good as it will be able to perform more complex tasks
* Bad, because of reliance on libraries in Python

### References
* GeeksforGeeks. (2024a, August 8). Top 7 programming languages for Backend Web Development. GeeksforGeeks. https://www.geeksforgeeks.org/top-7-programming-languages-for-backend-web-development/ 
* Saini, H. (2022, November 29). Top backend technologies and their pros and cons. What should you use for your next project. Medium. https://medium.com/@hs913271/top-backend-technologies-and-their-pros-and-cons-what-should-you-use-for-your-next-project-3ac920509ff5 
* Tarif, Z. (2024, April 18). Backend Programming Languages in 2024 | Which is the best? Back4App Blog. https://blog.back4app.com/backend-programming-languages/ 