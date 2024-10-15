---
# These are optional metadata elements. Feel free to remove any of them.
status: "proposed"
date: {2024-15-10}
decision-makers: {Connor Wright, Waris Ali, David Ani}
---

# How will communication between branches be acheived 

## Context and Problem Statement

How will branches communicate with each other to effeciently share resources?
Will this be done in system or externally?


## Decision Drivers

* Resource/Management sharing is a key objective of the system so it needs to be a robust solution
* Communication should be instant, and if not verbal/written should only contain relevant information that is easy to read

## Considered Options

* External Systems (e.g. phone calls)
* In-System Messaging Functionality
* Request System (see more details in More Information tab)

## Pros and Cons of the Options

### External Systems (e.g. phone calls)

* Good as it won't require any development effort
* Bad as it isn't a scalable solution
* Bad as it can lead to human error

### In-System Messaging Functionality

* Good as it would make communication easier and be more accessible
* Bad as it would be a large feature to develop

### Request System 

* Good as it would allow branches to work seamlessly together
* Good as it wouldn't require any major updates from one branch to work with another
* Good as it handles both sharing and informing others
* Bad as it may not be as detailed

## Decision Outcome

Chosen option: Request System 

### Confirmation

* Ensure a feature is developed that displays a branches inventory and managerial information, and that from here requests can be made to borrow

### Consequences

* Branches can borrow staff and inventory from each other
* Branches can see what is available in other areas
* Branches can keep up to date with new stock

### More Information

* The Request System would work as follows: The user can select a branch, and select whether they want to see their staff or their inventory. The selected data is then displayed, and from here a request can be made to borrow. This request is then sent to an Admin at the relevant branch who can approve it, and the system updates both branches. 