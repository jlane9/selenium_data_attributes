Selenium Data Attributes
========================

Introduction
------------
Python wrapper for the selenium framework. This library makes use of custom data attributes released in HTML5 to place design of the web testing mostly in the hands of those developing the source code. 
Developers will add the attribute "data-qa-id" to the pieces of code they want tests to interact with. 




Web Developer Guidelines
------------------------

- For all elements place the data attribute tag directly on the element that will be interacted with. **This is especially important for elements that are interactive such as inputs or buttons.**
```html
// Example
<a href="#" data-qa-id="hello-world">Hello world</a>
```
- For containers that contain repeating elements (List, Table, etc.) use square brackets at the end of the nested elements' id.
```html
// Example
<ol>
    <li>
        <a href="/to/some/where" data-qa-id="link[0]">I'm feeling lucky</a>
    </li>
    <li>
        <a href="/this/leads/no/where" data-qa-id="link[1]">Claim your prize</a>
    </li>
    <li>
        <a href="/im/lost" data-qa-id="link[2]">Need help?</a>
    </li>
</ol>
```
- Certain elements will have special identifiers that should not be used elsewhere:
    1. Forms elements may contain:
        1. **submit** if the element is the submission button for that form
        2. **cancel** if the element is the cancel button for that form
    2. Modal elements may contain:
        1. **submit** if the element is the submission button for that modal
        2. **cancel** if the element is the cancel button for that modal
        3. **close** if the element is the close button for that modal
        
    3. Search elements may contain:
        1. **clear** if the element is the clear button for that search field
        
    4. Table headers may contain elements that contain:
        1. **asc** or **desc** ties to the sort order icon


Tester Guidelines
-----------------
