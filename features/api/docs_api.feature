@api @docs @bdd @smoke
Feature: Documentation API endpoint availability
  As a test engineer
  I want docs API endpoint health checks
  So that documentation links remain reachable

  Scenario: Docs API page is reachable
    When I request the docs API URL
    Then docs API response status should be 200
    And docs API response content type should include "text/html"
