@ui @docs @regression
Feature: Part Documentation Table Of Contents Validation
  As a documentation user
  I want part documentation TOC links to resolve correctly
  So that each listed docs page remains navigable and relevant

  Scenario Outline: Validate page TOC subpages with text assertion
    Given I open the docs part page path "<path>"
    Then the docs part page request should be successful
    And all table of contents links should resolve with relevant text

    Examples:
      | path          |
      | /             |
      | create/       |
      | virtual/      |
      | views/        |
      | trackable/    |
      | revision/     |
      | template/     |
      | test/         |
      | pricing/      |
      | stocktake/    |
      | notification/ |
