# Quick Start

The plugin can be configured in the MkDocs configuration file `mkdocs.yml`.
By default, the figure and table captions are enabled.

To enable the plugin, simply add the plugin to the `plugin` section of your configuration.

In `mkdocs.yml`: 

```yaml
...
plugins:
- caption
```

With the plugin enabled, one can now use an easy and descriptive syntax to add
captions to figures and tables. The captions are automatically numbered and
can be referenced in the text.


=== "Markdown"

    ```Markdown
    ![figure caption](img.jpg)

    Table: table caption {#my-table}

    | heading 1| heading 2 | 
    | - | - | 
    | content 1 | content 2 |
    | content 3 | content 4 |

    See [#my-table] for more details.
    ```

=== "HTML"

    ```html
    <p>
    <figure id=_figure-1>
        <img src="img.jpg" />
        <figcaption>Figure 1. figure caption</figcaption>
    </figure>
    </p>
    <p>
    <table id="my-table">
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
    <caption style="caption-side:bottom">Table 1: table caption</caption>
    </table>
    <p>
    See <a href="#my-table">Table 1</a> for more details.
    </p>
    ```
