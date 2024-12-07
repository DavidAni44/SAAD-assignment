---
# These are optional metadata elements. Feel free to remove any of them.
status: "proposed"
date: {2024-15-10}
decision-makers: {Connor Wright, Waris Ali, David Ani}
---

# How will the various items in the inventory be catogorised and split into their atomic values

## Context and Problem Statement

The system can store multiple types of media (books, CD's, DVD's, etc). How will break down the information so that it can be properly stored?

## Decision Drivers

* Performance, we need to choose the option that provides optimimum performance as the size of the inventory will start off large and only continue to grow
* Readability, the information needs to be stored in a way that is easy to understand for anyone viewing it in its raw form 
* Speed of input, we want adding new media to be a relatively quick process

## Considered Options

* Manual Entry
* External System to retrieve relevant data (using ISBN number lookups)


## Pros and Cons of the Options

### Manual Entry

* Good as we have control over the data being stored and then displayed
* Good as its not reliant on external factors
* Bad as it's not as scalable
* Bad as it would take up more storage
* Bad as it would require more effort to store, especially on large orders

### External System retrieves relevant data (using ISBN number lookups)

* Good as it will save time when ordering stock
* Good as it would be less constrained by large orders
* Bad as using API calls could become costly


## Decision Outcome

Chosen option: External System retrieves relevant data (using ISBN number lookups)

### Confirmation

* Ensure that a feature is developed that when given an ISBN (or equivalent) can extract the relevant information and store it in our database
* Ensure the database is structured properly and the information stored is both relevant and easy to read

### Consequences

* Large orders will be able to be added to the inventory quicker, as less inputs are required from the user. This in turn will make the system more scalable
* It will make storing media much easier 
* An API will most likely be used to acheive this, and a cost analysis will need to be performed to ensure it isn't making costs rise too much
