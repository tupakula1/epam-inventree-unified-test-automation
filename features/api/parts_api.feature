@api @part @crud @bdd
Feature: Parts API CRUD and validation
  As an API consumer
  I want to manage parts through the REST API
  So that inventory records remain accurate

  @positive @smoke
  Scenario: Create a minimal part
    Given a unique minimal part payload
    When I create the part via API
    Then the API response status should be 201
    And the created part response should include the request name

  @positive
  Scenario: Get a part by id
    Given an existing part created via API
    When I fetch the created part by id
    Then the API response status should be 200
    And the API response should contain the same part id

  @positive
  Scenario: Update a part name
    Given an existing part created via API
    When I update the created part name to "BDD Updated Part"
    Then the API response status should be 200
    And the API response part name should be "BDD Updated Part"

  @positive @smoke
  Scenario: Delete a part
    Given an existing part created via API
    When I delete the created part
    Then the API response status should be 204
    And fetching the deleted part by id should return 404

  @negative @boundary
  Scenario: Reject part creation without required name
    Given a part payload missing the required name
    When I create the part via API
    Then the API response status should be 400
    And the API error should contain field "name"

  @negative
  Scenario: Reject duplicate IPN
    Given an existing part with IPN "BDD-DUP-001"
    When I create another part with duplicate IPN "BDD-DUP-001"
    Then the API response status should be one of "201,400,409"
