---
# These are optional metadata elements. Feel free to remove any of them.
status: "proposed"
date: {2024-20-10}
decision-makers: {Connor Wright, Waris Ali, David Ani}
---

# Will Payments be handled internally or externally?

## Context and Problem Statement
Will we create our own system to handle the payment methods for the various transactions of the system, or will we use a pre-existing external system/API?


## Decision Drivers

* Scalability - The chosen approach needs to be able to handle AML's expected growth of 10% per anum
* Performance - The approach should be able to take payments quickly, with minimum waiting/loading time
* Security - The approach must keep all payment details secure and not subject to any risks in order to ensure legal regulations are followed

## Considered Options

* Creating an internal system (Direct Debit)
* Using an external API (e.g Stripe)

## Pros and Cons of the Options

### Creating an internal system (Direct Debit)
#### Pros

* Control over the feature - We wouldn't have to rely on external services that could be subject to its own issues that would require waiting to resolve
* Cost - Not paying to use an external service could save money in the long run

#### Cons

* Development Time - Would be increased heavily due to complexity
* Security - A known and tested external service would have more security features and would be less subject to risk
* Scaling - Would be less scalable than an external service

### Using an external API (e.g Stripe)
#### Pros

* Ease of implementation - Using an external service would require less development time and in turn
* Security - An external service would already have robust features to ensure security laws are met
* Scalable - An external service will be much more suited to handling the increase of users per anum

#### Cons

* Cost - May be more expensive over time to pay for the service
* Dependency - Would be reliant on said external service, and could be left in the dark should something happen on their side

## Decision Outcome

Chosen option: Using an external API (e.g Stripe)

### Confirmation

* Ensure that the relevant API is documented alongside the others

### Consequences

* Using an external service will help speed up development, as well as allow the system to be more secure and scalable. Reliance on this service is a concern, however this is a worse case scenario and therefore this choice makes the most sense with AML's concerns and goals.

### References
* Payment gateway benefits for businesses | Stripe. (2023, August 31). https://stripe.com/gb/resources/more/five-key-benefits-of-payment-gateways-for-businesses
* GoCardless. (2023, March 30). How to create a payment gateway. GoCardless. https://gocardless.com/guides/posts/how-to-create-a-payment-gateway
* Payment APIs: What are they and how do they work? (n.d.). StaxPayments. https://staxpayments.com/blog/payment-apis-how-they-work/
* Chetu. (n.d.). Build Your Own Payment Gateway (The Pros + Cons). https://www.chetu.com/blogs/finance-2/why-you-should-create-your-own-payment-gateway.php