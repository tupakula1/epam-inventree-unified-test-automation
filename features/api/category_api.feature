@api @category @crud @bdd
Feature: Category API CRUD and validation
  As an API consumer
  I want to manage part categories through the REST API
  So that parts can be organized correctly

  @positive @smoke
  Scenario: Create a minimal category
    Given a unique minimal category payload
    When I create the category via API
    Then the category API response status should be 201
    And the created category response should include the request name

  @positive
  Scenario: Create a child category
    Given an existing parent category via API
    When I create a child category for that parent
    Then the category API response status should be 201
    And the created category parent id should match the parent category id

  @positive
  Scenario: Update a category name
    Given an existing category via API
    When I update the category name to "BDD Updated Category"
    Then the category API response status should be 200
    And the category API response name should be "BDD Updated Category"

  @positive @smoke
  Scenario: Delete a category
    Given an existing category via API
    When I delete the category
    Then the category API response status should be 204
    And fetching the deleted category by id should return 404

  @negative
  Scenario: Reject category creation without required name
    Given a category payload missing the required name
    When I create the category via API
    Then the category API response status should be 400
    And the category API error should contain field "name"
