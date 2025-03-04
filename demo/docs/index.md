# Welcome to the Demo of the MkDocs Caption plugin

For full documentation, visit [https://tobiasah.github.io/mkdocs-caption/](https://tobiasah.github.io/mkdocs-caption/).

![Image title](https://dummyimage.com/600x400/f5f5f5/aaaaaa#only-light){width=80% #fig-schematic}
![Image title](https://dummyimage.com/600x400/21222c/d5d7e2#only-dark){width=80% #fig-schematic}

## Images

![This uses the alt as caption](assets/demo.png){width="200"}

![](assets/demo.png "This uses the the title as caption"){width="200"}

Figure: This uses a Figure identifier as caption {.my_class #my_id}

![](assets/demo.png){width="200"}

Figure: This uses a Figure identifier as caption
and it goes on for multiple lines

![](assets/demo.png){width="200"}


!!! warning

    Figure: This uses a Figure identifier as caption and
    it goes on for multiple lines

    ![](assets/demo.png){width="200"}

Inline images should not be converted ![Hello](assets/demo.png){width="30"}, even if they have a alt text. :smile:

### Cross page reference

See local [](#my_id) or cross page [](second_page.md#my_id) in that page. The same with a text [Test](second_page.md#my_id)

## Tables

Table: Table **bold** caption

| My | Table |
| - | - |
| Has | A Caption |
| Which Makes | It Fancy |

Table: Control the col width through the caption {cols=2,5}

| My | Table |
| - | - |
| Has | A Caption |
| Which Makes | It Fancy |

## Custom

List: This wraps any element in a figure with the specified caption

1. item 1
2. item 2
3. item 3

Code: The index is unique for each identifier

```
git push --force
```
