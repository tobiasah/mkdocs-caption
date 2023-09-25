# Referencing Figures And Tables

Referencing elements in markdown is pretty straight forward. Since this plugin
adds a default id to all figures and tables created these ids can be used to 
reference the element. The following example shows how to reference a figure.

=== "Markdown"

    ```Markdown
    ![Caption text](assets/demo.png)

    See [Figure](#_figure-1) above for more details.
    ```

=== "HTML"

    ```html
    <figure id=_figure-1>
        <img src="assets/demo.png" alt="This uses the alt as caption" />
        <figcaption>Figure 1. Caption</figcaption>
    </figure>
    <p>See the <a href="#_figure-1">Figure</a> above for more details.</p>
    ```

!!! warning
    Although a default id is added to each figure/table it is not recommended 
    use it as a reference. The reason is that the order of the figures/tables
    might change. This will result in the wrong figure/table being referenced.
    Instead it is recommended to assign a custom id to the figure/table.

## Automatic Link Text Generation

Often one would like the link text to look something like `Figure 1` or `Table 1`.
Sure this can be done manually, but it is tedious and error prone. This plugin
can automatically generate the link text for you. This done by referencing the
figure/table id and not specifying a link text.

=== "Markdown"

    ```Markdown
    ![Caption text](assets/demo.png)

    See [](#_figure-1) above for more details.
    ```

=== "HTML"

    ```html
    <figure id=_figure-1>
        <img src="assets/demo.png" alt="This uses the alt as caption" />
        <figcaption>Figure 1. Caption</figcaption>
    </figure>
    <p>See <a href="#_figure-1">Figure 1</a> above for more details.</p>
    ```

!!! note
    The link text can be customized by using the `reference_text` option in the
    configuration. See the [config chapter](#config.md) for more details.