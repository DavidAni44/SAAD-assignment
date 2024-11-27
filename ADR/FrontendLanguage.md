---
status: "proposed"
date: {2024-04-11}
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

* HTML/CSS & JavaScript
* React

## Pros and Cons of the Options

### HTML/CSS & JavaScript

* Good as the developers are familiar with HTML/CSS, and have some experience with JavaScript, which will make development faster and less complex
* Good as it is easily compatible with the Flask framework
* Good as it improves SEO effeciency
* Bad as simplicity may lead to more advanced features not being able to be implemented

### React

* Good as it uses a more structure and component based approach
* Good as it allows for more a dynamic UI
* Bad as developers aren't familiar with the language which would increase development time
* Bad as it has slower loading times

## Decision Outcome

Chosen option: HTML/CSS & JavaScript, due to developer familiarity

### Consequences

* Good, because it will allow development to go more smoothly as developers don't need to spend time learning new technologies
* Good, because it is widely used and will have a variety of features available to create the AML
* Bad, because simplicity may lead to certain desired features being unavailable

### Confirmation

* Github repistory should show that all front-end features are created in HTML/CSS & JavaScript
* Inspect code when running, should be able to see the script and html tags

### References
* GeeksforGeeks. (2024, September 25). HTML vs. React: What Every Web Developer Needs to Know. GeeksforGeeks. https://www.geeksforgeeks.org/html-vs-react/ 
* Jomagene. (2024, June 29). Comparing Frontend Technologies: ReactJS vs. Pure HTML, CSS, and JavaScript. DEV Community. https://dev.to/jomagene/comparing-frontend-technologies-reactjs-vs-pure-html-css-and-javascript-3ofb
* 