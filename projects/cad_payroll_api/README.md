# Canadian Payroll API
(few sentences about the project)

(option to skip directly to the features section or go through the spiel below)

# Context

## Motivation
In a previous job, I was part of a project to build a payroll system for a client. While the initial goals of the project were to build a basic payroll system that would suit most people's needs on a limited budget, it quickly spiraled into a system with the intent to rival Ceridian and Quickbooks. This led to many setbacks and change requests to fulfill the new client expectations. While a product was delivered, it was far from the initial goal and possibly may not have suitable for the client long term.

## Idea
Throughout the project, I felt that a better opportunity presented itself which my company could take advantage of. Before presenting the idea, let me provide some context to help convey the conclusion I arrived at.

### Market
Ceridian, Quickbooks and ADP are some of the big names when it comes to payroll processing. These are systems with many features to match the many unique cases that arises from handling payroll. Almost all company sizes can go with any one of these solutions, and some (ex. Quickbooks) have features/pricing for small businesses. Any company looking for a payroll solution will inveitably look through these big name products before making a decision. 

### Company Resources
The company I was working for was a small company of < 25 people with only a handful of developers. There are a few systems being maintained, so there is limited capacity to maintain an additional system and build out future enhancements. 

### My Own Coding Abilities
Personally, I'm not very good at front end development. It is something that I've played around with and CSS still stumps me to this day. Eventually, I will revisit it, but at that time I only had some level of confidence in Python. I'm not a developer by any means, but I had some idea of how to break down requirements to basic steps that could eventually be translated into code.

### Thoughts
1. Here I will introduce a term (that may already exist) called "micro-company" which is a company with < 25 employees. I felt that for a micro-company, there would be a demand for an alternative option to the big payroll names. While their do provide features that these companies need, a lot of it will be unnecessary because these micro-companies don't operate with the most basic payroll scenarios. Hence, they will be paying for a set of features tailored to small business but only using a subset of them. This implies that a subset of the subscription cost is wasted.
2. For any future system that my company would own, it would need to be simple to maintain and build on top of. It would be critical to differentiate between "must have" features and "nice to haves". One question that comes to mind here is "how can we target the most amount of customers while putting the least amount of strain on development resources?"
3. I would eventually need to pitch this idea to my peers at the company, so I should be able to build some working version. What's the easiest thing I can develop to showcase this?

### Idea
The idea is to "create a payroll system that can charge $5 per month and can let customers run payroll in 5 minutes". Of course, probably not the best marketing statement as I am not in marketing, but it provides motivation for the solution which would be realized in two stages:
1. Build a "Payroll API" that would handle the most basic payroll tasks such as
   1. Manage company information
   2. Manage employee information
   3. Process payroll for a particular pay period
   4. Generate pay slips
   5. Generate end of year statements
2. Build a "Payroll Front-End Template" that would go along with the first stage to help market it to customers

### Opportunity
With this, the company could offer the following services:
1. Hook up directly to the API - (add explanation here)
2. Provide the standard front-end template as a SaaS - (add explanation here)
3. Custom development projects - (add explanation here)

### Considerations and Competition


# Features