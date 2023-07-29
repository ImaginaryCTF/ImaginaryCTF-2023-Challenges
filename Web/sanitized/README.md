# sanitized
**Category:** Web
**Difficulty:** Hard
**Author:** maple3142

## Description

You are not going to find a DOMPurify 0day right?

## Distribution

- link

## Solution

- DOMPurify uses HTML parser by default, but XHTML parsing allows CDATA so it is possible to use a combination of `<style>` and CDATA to bypass it. Actual HTML payload should be encoded inside a HTML attribute.
- To bypass CSP, you need to abuse the **page not found** fallback route and use that to construct a valid js using url path.
- It is necessary to clobber `window.Page` to prevent the js from throwing error.
- To make a `<script>` tag load when inserted using `innerHTML`, the only way is to use `<iframe srcdoc="...">`. But you can't do that easily as XHTML does not allow `<` in attribute value, and you can't easily emit a `&lt;` token from HTML's attribute context.
- The trick is to inject a `<base href="...">` to change the base url, then the subsequent `report.js` script tag will use the new base url, which triggers the fallback route.
- `solve.js`
