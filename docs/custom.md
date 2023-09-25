# Custom Caption

What makes this plugin so unique is the ability to add a caption to any element.
This is done through the custom caption identifier and wrapping the element
in a figure. 

By default, there is no custom caption identifier defined. This means that the plugin
will not add a caption to any element. The user can define a custom caption identifier
in the `mkdocs.yml` configuration file. The configuration accepts a list of identifiers
so even multiple identifiers can be defined.

The following example shows how to define two custom caption `List` and `Example`
as identifiers:

```yaml
...
plugins:
  - caption:
    additional_identifier: ["List", "Example"]
...
```

!!! warning
    The identifier is case-sensitive.


## Adding a caption

A custom caption, unlike the image and table caption, can be added to any 
element. This is done be adding a defined identifier right before of the target 
element.

!!! note
    This example assumes that both `List` and `Example` are defined as custom
    caption identifiers.

=== "Markdown"

    ````Markdown
    List: This is a list

    * item 1
    * item 2
    * item 3

    Example: This is an example

    ```python
    print("Hello World")
    ```
    ````

=== "HTML"

    ```html
    <figure id="_list-1">
    <ul>
    <li>item 1</li>
    <li>item 2</li>
    <li>item 3</li>
    </ul>
    <figcaption>List 1: This is a list</figcaption>
    </figure>
    <figure id="_example-1">
    <div class="highlight">
    ... code block rendering ...
    </div>
    <figcaption>Example 1: This is an example</figcaption></figure>
    ```

!!! danger
    The caption can stretch over multiple lines. However it must end with a 
    blank line before the target. Otherwise the target will be interpreted as
    part of the caption.

!!! note 
    By default, every created figure is assigned a default id (`_list-x`). This id
    can be used to reference the figure. It is however recommended to 
    assign a custom id to the figure when referencing (see the
    [customization section](#customizing-the-custom-element) below). This will ensure that the 
    correct figure is referenced even if the order of the tables changes.

!!! note
    This syntax is custom to the `Caption` plugin and is not supported by
    MkDocs natively. However, even if the plugin is not enabled (e.g. in the
    Github/text editor preview) the target element will still be rendered correctly, and
    the caption will be displayed as normal text above the element. This helps
    the readability outside MkDocs.

!!! tip
    The numbering is unique to every identifier. This means that the numbering
    for `List` and `Example` are independent of each other.

## Customizing the Caption element

The plugin allows customizing the figure element. One way is through the 
`mkdocs.yml` configuration file (e.g. position of the caption relative to the
target element). The other way is to add attributes to the caption. 

!!! warning
    The configuration in the `mkdocs.yml` file is applied to all custom identifiers.
    It is not possible to customize the figure element for a specific identifier only.
    However most of the attributes allow the usage of a placeholder (`{identifier}`
    and `{Indentifier}`) which will be replaced with the identifier during 
    the build step.

Attributes are added by adding a curly bracket after the
caption and specifying the attributes inside the curly brackets. This
is not unique to the `Caption` plugin, but is a general feature of the extended
Markdown syntax used by MkDocs.

!!! tip
    The class attribute can be assign with `.class_name`

!!! tip
    The id attribute can be assign with `#id_name` and overrides the default id.

=== "Markdown"

    ```Markdown
    List: This is a list {.my_class #my_id any_attribute="value"}

    * item 1
    * item 2
    * item 3
    ```

=== "HTML"

    ```html
    <figure id="my_id" class="my_class" any_attribute="value">
    <ul>
    <li>item 1</li>
    <li>item 2</li>
    <li>item 3</li>
    </ul>
    <figcaption>List 1: This is a list</figcaption>
    </figure>
    ```