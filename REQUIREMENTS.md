# Requirements — Customer Search

## User Story
As a user, I want to search customers by name or email, so that I can quickly find the customer record I need.

## Functional Requirements
- **FR-01**: The system must allow to search for customer records across the fields: first name, last name, and email address.
- **FR-02**: The system must return customer records that contain partial matches in either the full name or email address. 
- **FR-03**: The system must reject search queries that do not contain a minimum of 3 inputted non-whitespace characters.
- **FR-04**: The system's matches must be case-insensitive, and diacritic-insensitive.
- **FR-05**: The system must return a user-friendly message in case no matches are found.
- **FR-06**: The system must sort resultant records ranked by exact matches first, partial matches second.

## Non-Functional Requirements
- **NFR-01**: Queries response time must not exceed 300ms.
- **NFR-02**: Queries must be protected against unathorized characters.
- **NFR-03**: The system must limit the resultant records from a query to a maximum of 20.

## Open Questions
- **Q-01**: When the user types multiple words, should the system search for matches independently? Or should it treat it as a unit?
- **Q-02**: What should the tie-braker be when two records have the same relevance?
- **Q-03**: What would happen if not enough characters are typed to make the search?
- **Q-04**: What attributes from a matching user should be displayed?

## Constraints / Assumptions
- **A-01**: Every customer record as a unique ID.
- **A-02**: Emails are unique across all records.
- **A-03**: Customer names and email address may only include Latin characters including accents.