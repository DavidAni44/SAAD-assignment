---
# These are optional metadata elements. Feel free to remove any of them.
status: "proposed"
date: {2024-10-10}
decision-makers: {Connor Wright, Waris Ali, David Ani}
---

# Choice of Backend Language

## Context and Problem Statement

What language will be used to code the backend of the solution in? This is the main bulk of the code that will perform the various functions of the AML

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
* Bad as security is a big concern with this language

### Python/Flask

* Good as the framework is designed for web development
* Good as developers have familiarity with the language
* Bad due to reliance on external libraries


## Decision Outcome

Chosen option: Python/Flask due to the choice of Architectural Style being a Web App

### Consequences

* Good, because it will allow the solution to be coded faster due to developer pre-knowledge
* Good as it will avoid the security issues in PHP
* Good as it will be able to perform more complex tasks
* Bad, because of reliance on libraries in Python