# Image Caption

By default, MkDocs does not wrap images in a `<figure>` tag. A markdown image
tag simply translates into an HTML `<img>` tag. This plugin enables the user
to wrap images in an HTML `<figure>` tag and specify a caption for the image.


## Adding a caption

There is more than one way to add a caption to an image. This page explains in
all options in detail.

!!! Important
    If none of the described options apply, the image remains untouched. Meaning
    that the image is not wrapped in a `<figure>` tag and no caption is added.


### Using the alt attribute as caption

The easiest way to add a caption to an image is to use define an alt text for 
the image. In markdown this is done by adding a text in the square brackets:

=== "Markdown"

    ```Markdown
    ![This uses the alt as caption](assets/demo.png)
    ```

=== "HTML"

    ```html
    <figure id=_figure-1>
        <img src="assets/demo.png" alt="This uses the alt as caption" />
        <figcaption>Figure 1. This uses the alt as caption</figcaption>
    </figure>
    ```

!!! note 
    By default, every figure is assigned a default id (`_figure-x`). This id
    can be used to reference the figure. It is however recommended to 
    assign a custom id to the image directly, or to the figure tag (see the
    [customization section](#customizing-the-figure-element) below). This will ensure that the 
    correct image is referenced even if the order of the images changes.

### Using the title attribute as caption

MkDocs by default is able to assign a title to an image. The `Caption` plugin
is able to use this title as a caption for the figure.

A title can be assigned to an image by adding a quoted text right after the 
image path:

=== "Markdown"

    ```Markdown
    ![](assets/demo.png "This uses the title as caption")
    ```

=== "HTML"

    ```html
    <figure id=_figure-1>
        <img src="assets/demo.png"/>
        <figcaption>Figure 1. This uses the title as caption</figcaption>
    </figure>
    ```

!!! note 
    By default, every figure is assigned a default id (`_figure-x`). This id
    can be used to reference the figure. It is however recommended to 
    assign a custom id to the image directly, or to the figure tag (see the
    [customization section](#customizing-the-figure-element) below). This will ensure that the 
    correct image is referenced even if the order of the images changes.

!!! note
    If both the `alt` and `title` attribute are present, the `title` attribute
    is used as caption. This allows the user to define both a caption and an
    alt text for the image.

### Using the Figure identifier as caption

The most flexible way to add a caption to an image is to use the Figure
identifier (by default `Figure:`) to define the caption.
This identifier is unique to the `Caption` plugin and is also used for the 
table and custom captioning. The identifier must be placed right before the 
image and has the following syntax:

=== "Markdown"

    ```Markdown
    Figure: This uses the identifier as caption

    ![](assets/demo.png)
    ```

=== "HTML"

    ```html
    <figure id=_figure-1>
        <img src="assets/demo.png"/>
        <figcaption>Figure 1. This uses the identifier as caption</figcaption>
    </figure>
    ```

!!! danger
    The caption can stretch over multiple lines. However it must end with a 
    blank line before the image. Otherwise the image will be interpreted as
    part of the caption.

!!! note 
    By default, every figure is assigned a default id (`_figure-x`). This id
    can be used to reference the figure. It is however recommended to 
    assign a custom id to the image directly, or to the figure tag (see the
    [customization section](#customizing-the-figure-element) below). This will ensure that the 
    correct image is referenced even if the order of the images changes.

!!! note
    This syntax is custom to the `Caption` plugin and is not supported by
    MkDocs natively. However, even if the plugin is not enabled (e.g. in the
    Github/text editor preview) the image will still be rendered correctly, and
    the caption will be displayed as normal text above the image. This helps
    the readability outside MkDocs.

!!! tip
    The identifier can be customized in the `mkdocs.yml` configuration file
    through the `caption_prefix`. See the [Config chapter](config.md) for more details.

## Customizing the Figure element

The plugin allows customizing the figure element. One way is through the 
`mkdocs.yml` configuration file (e.g. position of the caption relative to the
image). The other way is to add attributes to the caption. 

!!! Important
    Only when using the [`Figure:` identifier](#using-the-figure-identifier-as-caption),
    attributes can be added directly to `figure` element. If the `alt` or `title`
    attribute is used, attributes can only be added to the `img` element directly.

Attributes are added to the figure element by adding a curly bracket after the
figure identifier and specifying the attributes inside the curly brackets. This
is not unique to the `Caption` plugin, but is a general feature of the extended
Markdown syntax used by MkDocs.

!!! tip
    The class attribute can be assign with `.class_name`

!!! tip
    The id attribute can be assign with `#id_name` and overrides the default id.

=== "Markdown"

    ```Markdown
    Figure: Caption Text {.my_class #my_id any_attribute="value"}

    ![](assets/demo.png)
    ```

=== "HTML"

    ```html
    <figure id="my_id" class="my_class" any_attribute="value">
        <img src="assets/demo.png"/>
        <figcaption>Figure 1. Caption Text</figcaption>
    </figure>
    ```