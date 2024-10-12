---
status: "proposed"
date: {2024-10-10 when the decision was last updated}
decision-makers: {Waris Ali, Connor Wright, David Ani}
---

# Choice of Front-End Language used for the System

## Context and Problem Statement

What language will be used to create the front-end of the system that users interact with? This includes the styling elements
and the page layouts

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

{Describe how the implementation of/compliance with the ADR can/will be confirmed. Is the chosen design and its implementation in line with the decision? E.g., a design/code review or a test with a library such as ArchUnit can help validate this. Note that although we classify this element as optional, it is included in many ADRs.}
