# Table Caption

MkDocs supports the use of the simplified Markdown syntax for tables. However,
this syntax does not support captions for tables. The alternative to use HTML
tables is not ideal either, as it is not as readable as the Markdown syntax.
The `Caption` plugin solves this problem by adding support for table captions
to MkDocs.

## Adding a caption

A caption can be added to a table by using the Table identifier. This identifier
must be placed right before the table and has the following syntax:

=== "Markdown"

    ```Markdown
    Table: Caption for the following table

    ![](assets/demo.png)

    | heading 1| heading 2 | 
    | - | - | 
    | content 1 | content 2 |
    | content 3 | content 4 |
    ```

=== "HTML"

    ```html
    <table id="_table-1">
    <thead>
        <tr>
        <th>heading 1</th>
        <th>heading 2</th>
        </tr>
    </thead>
    <tbody>
        <tr>
        <td>content 1</td>
        <td>content 2</td>
        </tr>
        <tr>
        <td>content 3</td>
        <td>content 4</td>
        </tr>
    </tbody>
    <caption style="caption-side:bottom">Table 1: Caption for the following table</caption>
    </table>
    ```

!!! danger
    The caption can stretch over multiple lines. However it must end with a 
    blank line before the table. Otherwise the table will be interpreted as
    part of the caption.

!!! danger
    By default the caption is added to the bottom of the table. This can be
    changed by changing the `position` config element.
    See the [Config chapter](config.md) for more details.

!!! note 
    By default, every table is assigned a default id (`_table-x`). This id
    can be used to reference the table. It is however recommended to 
    assign a custom id to the table when referencing (see the
    [customization section](#customizing-the-table-element) below). This will ensure that the 
    correct table is referenced even if the order of the tables changes.

!!! note
    This syntax is custom to the `Caption` plugin and is not supported by
    MkDocs natively. However, even if the plugin is not enabled (e.g. in the
    Github/text editor preview) the table will still be rendered correctly, and
    the caption will be displayed as normal text above the table. This helps
    the readability outside MkDocs.

!!! tip
    The identifier can be customized in the `mkdocs.yml` configuration file
    through the `caption_prefix`. See the [Config chapter](config.md) for more details.

## Customizing the Caption element

The plugin allows customizing the table element. One way is through the 
`mkdocs.yml` configuration file (e.g. position of the caption relative to the
table). The other way is to add attributes to the caption. 

Attributes are added to the table element by adding a curly bracket after the
table identifier and specifying the attributes inside the curly brackets. This
is not unique to the `Caption` plugin, but is a general feature of the extended
Markdown syntax used by MkDocs.

!!! tip
    The class attribute can be assign with `.class_name`

!!! tip
    The id attribute can be assign with `#id_name` and overrides the default id.

=== "Markdown"

    ```Markdown
    Table: Caption {.my_class #my_id any_attribute="value"}

    ![](assets/demo.png)

    | heading 1| heading 2 | 
    | - | - | 
    | content 1 | content 2 |
    | content 3 | content 4 |
    ```

=== "HTML"

    ```html
    <table  id="my_id" class="my_class" any_attribute="value">
    <thead>
        <tr>
        <th>heading 1</th>
        <th>heading 2</th>
        </tr>
    </thead>
    <tbody>
        <tr>
        <td>content 1</td>
        <td>content 2</td>
        </tr>
        <tr>
        <td>content 3</td>
        <td>content 4</td>
        </tr>
    </tbody>
    <caption style="caption-side:bottom">Table 1: Caption</caption>
    </table>
    ```