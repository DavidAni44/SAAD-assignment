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

## Decision Outcome

Chosen option: Web Based Application

### Consequences

* Good because it will allow the solution to be more portable
* Good because it will be more available
* Bad because scalability may be an issue

<!-- This is an optional element. Feel free to remove. -->
### Confirmation

{Describe how the implementation of/compliance with the ADR can/will be confirmed. Is the chosen design and its implementation in line with the decision? E.g., a design/code review or a test with a library such as ArchUnit can help validate this. Note that although we classify this element as optional, it is included in many ADRs.}

<!-- This is an optional element. Feel free to remove. -->
## Pros and Cons of the Options

### Desktop/Database Application

<!-- This is an optional element. Feel free to remove. -->
{example | description | pointer to more information | …}

* Good, because this will be less vulnerable than a web app 
* Good, because this can be tailored to the AML 
* Good, most features can work without internet access
<!-- use "neutral" if the given argument weights neither for good nor bad -->
* Neutral, the system 
* Bad, because working with external systems (e.g. stock procurement) will require more effort

### Web Application

{example | description | pointer to more information | …}

* Good, it will allow the solution to be more portable and make availability easier
* Good, developers are familiar with web dev skills, making development faster and allowing more features to be implemented within the deadline
* Good, database can be updated in real time
* Bad, as scalability may be a concern
* Bad, internet access will always be needed to use it


