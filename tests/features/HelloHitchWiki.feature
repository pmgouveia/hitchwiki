Feature:
    In order to keep my product stable
    As a developer or product manager
    I want to make sure that everything works as expected

Scenario: Check title of website after search
    Given I open the url "http://hitchwiki.coletivos.org"
    When I click on the element "#n-Map" 
    Then I expect that the title is "Hitchwiki Map - Hitchwiki"