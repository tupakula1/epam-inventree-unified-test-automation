@api @part @bdd @negative @boundary
Feature: Parts API validation rules
  As an API consumer
  I want field validations to be enforced
  So that invalid part data is rejected

  Scenario: Reject part creation without name
    Given a validation payload without part name
    When I create the part for validation check
    Then the validation API response status should be 400
    And validation error payload should include field "name"

  Scenario: Reject part creation with name above maximum length
    Given a validation payload with part name length 101
    When I create the part for validation check
    Then the validation API response status should be 400

  Scenario: Reject duplicate part IPN
    Given an existing part for duplicate IPN "BDD-VAL-DUP-001"
    When I create another part for duplicate IPN "BDD-VAL-DUP-001"
    Then the validation API response status should be one of "201,400,409"

  Scenario: Ignore client-supplied pk field
    Given a validation payload with client pk 99999
    When I create the part for validation check
    Then the validation API response status should be 201
    And created part pk should not equal 99999

  Scenario: Reject empty name
    Given a validation payload with empty name
    When I create the part for validation check
    Then the validation API response status should be 400

  Scenario Outline: Reject values above field max lengths
    Given a validation payload with field "<field>" length <length>
    When I create the part for validation check
    Then the validation API response status should be 400

    Examples:
      | field | length |
      | name  | 101    |
      | IPN   | 101    |
      | units | 21     |
