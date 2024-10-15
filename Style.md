---
status: "proposed"
date: {2024-10-10}
decision-makers: {Waris Ali, David  Ani, Connor Wright}
---

# Choice of Architectural Style used for the AML

## Context and Problem Statement

What architectural style will be used to create the framework for the AML?

## Considered Options

* Desktop/Database Application
* Web Based Application
* Three Tier Architecture

## Decision Drivers

* Scalability, the style chosen should be suitable for a growing system
* Ease of updates, if changes need to be made to the system then the architectural style chosen should be one that makes updating the system as simple as possible
* Development Time, the style that allows the system to be developed in the shortest time frame

## Pros and Cons of the Options

### Desktop/Database Application

* Good, because this will be less vulnerable than a web app 
* Good, because this can be tailored to the AML 
* Good, most features can work without internet access
* Bad, because working with external systems (e.g. stock procurement) will require more effort
* Bad as it isn't portable and makes accessibility harder

### Web Application

* Good, it will allow the solution to be more portable and make availability easier
* Good, developers are familiar with web dev skills, making development faster and allowing more features to be implemented within the deadline
* Good, database can be updated in real time
* Bad, as scalability may be a concern
* Bad, internet access will always be needed to use it

### Three Tier Architecture

* Good as security can be tighter, with each layer having its own defences
* Good as this style tends to be more suited for large scale databases
* Bad as it can be much more costly both to create and mantain
* Bad as it will increase development time and complexity


## Decision Outcome

Chosen option: Web Based Application

### Consequences

* Good because it will allow the solution to be more portable. It can be accessed anywhere with a stable internet connection which in turn makes it more accessible.
* Good because it is a more cost effective option and doesn't require any specailist hardware
* Good because it will be easier to make updates in real time
* Bad because it is dependent upon a stable internet connection
* Bad because security will need to be a special consideration 


