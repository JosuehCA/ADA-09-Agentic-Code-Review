# AI Usage Log

### Entry 01 - Requirements Redefiniton
- **Stage**: Requirements.
- **Prompt/goal**: Redefine system's FR and NFR, looking for ambiguities.
- **AI Contribution**: 

      Suggested: 
        1. For FR-02, specifying whether a partial search is done over the whole full name and not just "the name".
        2. For FR-04, changing the word "tilde" to "diacritic", since a tilde in English is a different character from the Spanish tilde.
        3. For FR-06, proposing using a creation ID instead of date/time data to not have to rely on extra functionality.
        4. For NFR-02, stating that protection from injection attacks is out of scope (no in memory database).
- **Student Decision**: Accepted all observations except the third one, since that's part of the SPEC.md file. Still used that observation to change it to a more general phrasing. Refined requirements to be more accurate.
- **Impact**: REQUIREMENTS.md updated.

### Entry 02 - Specification Drafting
- **Stage**: Specification.
- **Prompt/goal**: Help define the SPEC.md contents based on the REQUIREMENTS.md file.
- **AI Contribution**: Provided a draft SPEC.md, cross referencing the REQUIREMENTS.md file and using a best practices context file as base of knowledge.
- **Student Decision**: Accepted. Stripped away samples from bullet points and changed some text formatting to match the desired view.
- **Impact**: SPEC.md updated.

### Entry 03 - Architecture Building
- **Stage**: Architecture.
- **Prompt/goal**: Build the architecture file and compare it against the SPEC.md file.
- **AI Contribution**: Provided a draft ARCHITECTURE.md, based on the SPEC.md file, and using a best practices context file as base of knowledge. Then suggested additional changes and the addition of a mermaid diagram.
- **Student Decision**: Accepted.
- **Impact**: ARCHITECTURE.md updated.

### Entry 04 - Tasks Definition
- **Stage**: Tasks.
- **Prompt/goal**: Build the unit tasks from the base of knowledge comprising REQUIREMENTS.md, SPEC.md, and ARCHITECTURE.md.
- **AI Contribution**: Provided the definition of 6 tasks regarding project setup -> domain model -> search logic -> validation and errors -> tests -> documentation.
- **Student Decision**: Accepted. Added README definition to T-06, and mock data definition for testing to T-05.
- **Impact**: TASKS.md updated.

<!-- Stages: Requirements, Specification, Architecture, Tasks, Implementation, Testing, Review  -->