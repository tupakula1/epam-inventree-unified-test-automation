@api @part @bdd
Feature: Parts API filtering and pagination
  As an API consumer
  I want to filter and page part results
  So that I can retrieve only relevant records

  @positive
  Scenario: Search parts by exact unique name
    Given an existing part with generated unique name
    When I search parts using the created part name
    Then the filter API response status should be 200
    And search results should contain the created part name

  @positive
  Scenario: Filter parts by active true
    When I list parts with active flag true
    Then the filter API response status should be 200
    And each listed part should have active true

  @positive
  Scenario: Filter parts by active false
    When I list parts with active flag false
    Then the filter API response status should be 200
    And each listed part should have active false

  @positive @boundary
  Scenario: Pagination limit returns at most requested rows
    When I list parts with pagination limit 5 and offset 0
    Then the filter API response status should be 200
    And the results length should be at most 5

  @positive
  Scenario: Pagination pages do not overlap
    When I list first and second pages with limit 5
    Then the first and second page part ids should not overlap

  @positive @boundary
  Scenario: Zero limit returns empty results
    When I list parts with pagination limit 0 and offset 0
    Then the filter API response status should be 200
    And the results length should be 0
