---
workflowType: 'prd'
---

# Product Requirements Document - bmadv6-nextjs-test01

**Author:** Gabe
**Date:** 2025-04-03

## Functional Requirements

This section is the capability contract for all downstream work (UX, architecture, epics). Each FR is testable and implementation-agnostic.

**FR1:** The home page show a round clock.

**FR2:** Add Timezone picker

**FR2.1:** Save the selected Timezone to the in-memory User Profile

**FR3:** Retrieve a user from the `https://randomuser.me/api/?results=1` and display the name on the home page.

**FR3.1:** Save the user info to the in-memory User Profile to prevent API call on page reload

**FR3.2:** Make it easy to swap the API where the user is retrieved from.

**FR3.3:** Add a "Reset" button on the home page for clearing the in-memory User Profile, and load the page like the first loading. 