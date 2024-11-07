---
status: "proposed"
date: {2024-10-10 when the decision was last updated}
decision-makers: {Waris Ali, Connor Wright, David Ani}
---

# Choice of Front-End Language used for the System

## Context and Problem Statement

What language will be used to create the front-end of the system that users interact with? This includes the styling elements
and the page layouts

## Decision Drivers

* Developer Profeciency, the more experienced the developers are with the language the less time is spent on learning and implementing the required features
* Scalability, as the system grows to handle more users/take on more inputs it needs to be able to handle this
* Backend integration, the langauge chosen needs to be compatible with the backend language

## Considered Options

* HTML/CSS
* JavaScript
* React

## Pros and Cons of the Options

### HTML/CSS

* Good as developer familiarity will make development less complex and faster
* Good as it is commonly used and therefore resources are plentiful and easy to access
* Bad as it is simple and may lack some more advanced desired features 

### JavaScript

* Good as it can handle both styling and interactive elements
* Good as it can be used with other languages
* Bad as it can increase development complexity and time

### React

* Good as it uses a more structure and component based approach
* Bad as developers aren't familiar with the language which would increase development time

## Decision Outcome

Chosen option: HTML/CSS, due to developer familiarity

### Consequences

* Good, because it will allow development to go more smoothly as developers don't need to spend time learning new technologies
* Good, because HTML/CSS is widely used and will have a variety of features available to create the AML
* Bad, because simplicity may lead to certain desired features being unavailable

### Confirmation

* Github repistory should show that all front-end features are created in HTML/CSS
* ADR to be reviewed as more detailed functions are developed - may choose to work with other languages as well
