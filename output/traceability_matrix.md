**Traceability Matrix**
=======================

| **Requirement ID** | **Requirement Description** | **Test Case ID** | **Test Case Title** | **Priority** | **Preconditions** | **Steps** | **Expected Result** | **Test Sign Off Criteria** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| REQ-001 | Authenticate Customer Service Agents via SSO and validate ROLE_FAULT_WRITE permission for fault ticket submission. | TC-001 | SSO Authentication and ROLE_FAULT_WRITE Permission | High | Customer Service Agent has valid SSO credentials and ROLE_FAULT_WRITE permission | Login with SSO credentials, Verify ROLE_FAULT_WRITE permission | Successful authentication and permission validation | 1. Test case executed successfully 2. Expected result matches actual result 3. No errors or warnings encountered |
| REQ-002 | Accept fault creation requests via POST /api/v1/faults/raise and respond with HTTP 202 Accepted and a Ticket Reference ID within sub-second latency. | TC-002 | Fault Creation via API | High | Valid request payload and authenticated user | Send POST request to /api/v1/faults/raise, Verify HTTP 202 Accepted response | Ticket Reference ID received within sub-second latency | 1. Test case executed successfully 2. Expected result matches actual result 3. No errors or warnings encountered |
| REQ-003 | Validate request payload, perform idempotency checks, and publish a FaultCreatedEvent to Kafka topic jiotel.fibre.faults.v1. | TC-005 | Request Payload Validation | Low | Invalid request payload sent to /api/v1/faults/raise | Send invalid POST request to /api/v1/faults/raise, Verify validation error response | Validation error response received | 1. Test case executed successfully 2. Expected result matches actual result 3. No errors or warnings encountered |
| REQ-004 | Ensure fault submission is idempotent to prevent duplicate tickets on double submission. | TC-003 | Idempotent Fault Submission | Medium | Valid request payload and authenticated user | Send duplicate POST requests to /api/v1/faults/raise, Verify only one ticket is created | No duplicate tickets created | 1. Test case executed successfully 2. Expected result matches actual result 3. No errors or warnings encountered |
| REQ-005 | Process FaultCreatedEvent in parallel consumer groups for ticketing, workforce reservation, and notification, isolating failures between consumers. | TC-004 | FaultCreatedEvent Processing | Medium | Valid FaultCreatedEvent published to Kafka topic | Verify event is processed by parallel consumer groups, Verify failures are isolated between consumers | Successful event processing and isolation of failures | 1. Test case executed successfully 2. Expected result matches actual result 3. No errors or warnings encountered |

**Summary**

* **High Priority Test Cases**: 2 (TC-001, TC-002)
* **Medium Priority Test Cases**: 2 (TC-003, TC-004)
* **Low Priority Test Cases**: 1 (TC-005)
* **Total Test Cases**: 5
* **Test Sign Off Criteria**: 1. Test case executed successfully 2. Expected result matches actual result 3. No errors or warnings encountered