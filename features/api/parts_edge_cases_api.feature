@api @part @bdd
Feature: Parts API edge and protocol behaviors
  As an API consumer
  I want authentication and protocol edge behaviors covered
  So that integration errors are detected early

  @negative
  Scenario: Unauthenticated request is rejected
    When I call parts list endpoint without authentication
    Then the edge API response status should be one of "401,403"

  @negative
  Scenario: Invalid token is rejected
    When I call parts list endpoint with invalid token
    Then the edge API response status should be one of "401,403"

  @negative
  Scenario: Invalid JSON payload is rejected
    Given a valid API token for edge scenario
    When I create part with invalid JSON body
    Then the edge API response status should be one of "400,415"

  @negative
  Scenario: Unsupported method on list endpoint returns 405
    Given a valid parts api client for edge scenario
    When I delete the parts list endpoint
    Then the edge API response status should be 405

  @positive @boundary
  Scenario: Single-character part name is accepted
    Given an edge payload with part name "X"
    When I create edge case part
    Then the edge API response status should be 201

  @positive @boundary
  Scenario: Maximum name length part is accepted
    Given an edge payload with max part name length 100
    When I create edge case part
    Then the edge API response status should be 201
