# Deep Dive into data.json

## What is `data.json`?

`data.json` is a JSON file that contains all the information about you that will be used to generate the resume. The JSON file follows a custom schema. You can find the schema & the details about the fields in this page.

Please find the schema for the `data.json` file below.

??? Schema

    The json schema for the `metadata.json` file is as follows:
    ```{ .json title="schema" .copy .select}
      --8<-- "docs/assets/json/rahul-resume-schema.json"
    ```

## Fields

### Basic Details

=== ":fontawesome-solid-f: First Name"

    ```{ .json .copy .select .annotate hl_lines="2"}
    {
      "firstName": "Rahul" // (1)
    }
    ```

    1. :warning: Required.

=== ":fontawesome-solid-m: Middle Name (Optional)"

    ```{ .json .copy .select .annotate hl_lines="3"}
    {
      "firstName": "Rahul",
      "middleName": ""  // (1)
    }
    ```

    1. :material-help-circle: Optional.

=== ":fontawesome-solid-l: Last Name"

    ```{ .json .copy .select .annotate hl_lines="4"}
    {
      "firstName": "Rahul",
      "middleName": "",
      "lastName": "Agarwal"  // (1)
    }
    ```

    1. :warning: Required.

=== ":material-link-variant-plus: Links (Optional)"

    ```{ .json .copy .select .annotate hl_lines="5-25"}
    {
      "firstName": "Rahul",
      "middleName": "",
      "lastName": "Agarwal",
      "links": [
          {
            "text": "git://ragarwalll", // (1)
            "href": "https://github.com/ragarwalll" // (2)
          },
          {
            "text": "linkedin://ragarwalll",
            "href": "https://www.linkedin.com/in/ragarwalll/",
            "column": 1 // (3)
          },
          {
            "text": "contact@therahulagarwal.com",
            "href": "mailto:contact@therahulagarwal.com",
            "column": 2 // (4)
          },
          {
            "text": "orcid://0009-0005-8806-1557",
            "href": "https://orcid.org/0009-0005-8806-1557",
            "column": 2
          }
      ],
    }
    ```

    1. :warning: Required. Defines the text that will be displayed for the link.
    2. :warning: Required. Defines the URL that the link will redirect to.
    3. :material-help-circle: Optional. Defines the column in which the link will be displayed. Default is `1`.
    4. :material-help-circle: Optionally define that the link will be displayed in the `second column`.

`Visual Specifics`

=== ":material-theme-light-dark: Preset"

    ```{ .json .copy .select .annotate hl_lines="3"}
    {
      "firstName": "Rahul",
      "preset": "deedy-inspired-open-fonts" // (1)
    }
    ```

    1. :material-help-circle: Optional. Defines the preset that will be used to generate the resume. Default is `deedy-inspired-open-fonts`.

    !!! information "Note"
        The preset is a combination of the theme, font, and the layout. Following are the available presets.

        - `deedy-inspired-open-fonts`: Default preset.
        - `deedy-inspired`: It uses the helvetica font. Can be used only in local development.
        - `carlito`
        - `montserrat`

=== ":material-format-paragraph-spacing: Spacing"

    ```{ .json .copy .select .annotate hl_lines="4"}
    {
      "firstName": "Rahul",
      "preset": "deedy-inspired-open-fonts",
      "spacing": "ultra" // (1)
    }
    ```

    1. :material-help-circle: Optional. Defines the spacing between the sections. Default is `ultra`.

    !!! information "Note"
        Following are the available spacings.

        - `tight`
        - `ultra`
        - `maximum`
        - `high_dense`
        - `pro_dense`
        - `semi_dense`
        - `light_dense`
        - `compact`
        - `normal`
        - `cozy`
        - `airy`
        - `minimal`
        - `spacious`

    !!! information "Suggestion"

          If you have a lot of content, it is advisable to use `ultra` or `tight` spacing.

### Sections

`key: resume.sections[]`

Sections are the main content of the resume. Each section can have multiple subsections. The subsections can have multiple fields.
Let's talk about each field in the sections.

=== ":octicons-heading-16: Heading"

    ```{ .json .copy .select .annotate hl_lines="6-12"}
    {
      "firstName": "Rahul",
      "middleName": "",
      "lastName": "Agarwal",
      "links": [],
      "resume": {
        "sections": [
          {
            "heading": "Experience" // (1)
          }
        ]
      }
    }
    ```

    1. :warning: Required. Defines the heading of the section.

=== ":material-format-section: Subsections"

    ```{ .json .copy .select .annotate hl_lines="10"}
    {
      "firstName": "Rahul",
      "middleName": "",
      "lastName": "Agarwal",
      "links": [],
      "resume": {
        "sections": [
          {
            "heading": "Experience",
            "subsections": [] // (1)
          }
        ]
      }
    }
    ```

    1. :warning: Required. Defines the subsections of the section. Refer to the [subsections section](#subsections) for more details.

    Please refer to the [subsections section](#subsections) for more details.

=== ":material-table-of-contents: Contents (Optional)"

    ```{ .json .copy .select .annotate hl_lines="11"}
    {
      "firstName": "Rahul",
      "middleName": "",
      "lastName": "Agarwal",
      "links": [],
      "resume": {
        "sections": [
          {
            "heading": "Experience",
            "subsections": [],
            "content": {} // (1)
          }
        ]
      }
    }
    ```

    1. :warning: Required. Defines the content of the section. Refer to the [content section](#content) for more details.

    !!! information "Note"
        Sometimes, you might not need subsections. In that case, you can directly define the content in a section itself.

    Please refer to the [content section](#content) for more details.

`Visual Specifics`

=== "::octicons-columns-16: Column Identifier"

    ```{ .json .copy .select .annotate hl_lines="10"}
    {
      "firstName": "Rahul",
      "middleName": "",
      "lastName": "Agarwal",
      "links": [],
      "resume": {
        "sections": [
          {
            "heading": "Experience",
            "column": 2 // (1)
          }
        ]
      }
    }
    ```

    1. :material-help-circle: Optional. Defines the column in which the section will be displayed. Default is `1`.

    !!! warning "Note"
        Currently only one & two columns are supported. More columns will be added in the future. So, for now, you can use `1` or `2`.

=== ":material-view-column: Subsections Columns"

    ```{ .json .copy .select .annotate hl_lines="10"}
    {
      "firstName": "Rahul",
      "middleName": "",
      "lastName": "Agarwal",
      "links": [],
      "resume": {
        "sections": [
          {
            "heading": "Experience",
            "column": 2,
            "columnSettings": 2 // (1)
          }
        ]
      }
    }
    ```

    1. :material-help-circle: Optional. Defines the number of columns for the subsections. Default is `1`.

    !!! information "Note"
        `columnSettings` basically means if the subsections should be displayed in multiple columns. If you have a lot of subsections, you can use this to display them in multiple columns.

    !!! information "Suggestion"

          Ideally, to imporve readability, you can use `columnSettings` with `2` if you have more than 4 subsections.

### Subsections

`key: resume.sections[].subsections[]`

Subsections are the sub-content of the sections. Each subsection can have multiple fields. Let's talk about each field in the subsections.

=== ":octicons-heading-16: Subsection Heading"

    ```{ .json .copy .select .annotate hl_lines="11"}
    {
      "firstName": "Rahul",
      "middleName": "",
      "lastName": "Agarwal",
      "links": [],
      "resume": {
        "sections": [
          {
            "heading": "Experience",
            "subsections": [{
              "heading": "SAP Labs India" // (1)
            }]
          }
        ]
      }
    }
    ```

    1. :warning: Required. Defines the heading of the section.

=== ":material-axis-arrow-info: Info"

    ```{ .json .copy .select .annotate hl_lines="12-15"}
    {
      "firstName": "Rahul",
      "middleName": "",
      "lastName": "Agarwal",
      "links": [],
      "resume": {
        "sections": [
          {
            "heading": "Experience",
            "subsections": [{
              "heading": "SAP Labs India",
              "info": {
                "title": "Software Engineer", // (1)
                "sameLine": true // (2)
              }
            }]
          }
        ]
      }
    }
    ```

    1. :warning: Required. You can use it to define anything, mostly you current role(s) is advisable.
    2. :material-help-circle: Optional. Defines if the title should be displayed in the same line as the subsection heading. Default is `false`.

    !!! information "Note"
        The name `info` might be misleading but you can consider it as the subtitle of the subsection.

=== ":fontawesome-solid-location-arrow: Metadata"

    ```{ .json .copy .select .annotate hl_lines="16-19"}
    {
      "firstName": "Rahul",
      "middleName": "",
      "lastName": "Agarwal",
      "links": [],
      "resume": {
        "sections": [
          {
            "heading": "Experience",
            "subsections": [{
              "heading": "SAP Labs India",
              "info": {
                "title": "Software Engineer",
                "sameLine": true
              },
              "metadata": {
                "duration": "July 2019 - Present", // (1)
                "location": "Bangalore, India" // (2)
              }
            }]
          }
        ]
      }
    }
    ```

    1. :material-help-circle: Optional. You can use it to define anything, mostly the duration is advisable.
    2. :material-help-circle: Optional. You can use it to define anything, mostly the location is advisable.

    !!! information "Note"
        The name `metadata` might be misleading but you can consider it as the extra information about the subsection.

=== ":material-table-of-contents: Content"

    ```{ .json .copy .select .annotate hl_lines="20"}
    {
      "firstName": "Rahul",
      "middleName": "",
      "lastName": "Agarwal",
      "links": [],
      "resume": {
        "sections": [
          {
            "heading": "Experience",
            "subsections": [{
              "heading": "SAP Labs India",
              "info": {
                "title": "Software Engineer",
                "sameLine": true
              },
              "metadata": {
                "duration": "July 2019 - Present",
                "location": "Bangalore, India"
              },
              "content": {} // (1)
            }]
          }
        ]
      }
    }
    ```

    1. :warning: Required. Defines the content of the subsection. Refer to the [content section](#content) for more details.

    Please refer to the [content section](#content) for more details.

### Content

`key: resume.sections[].subsections[].content`

`key: resume.sections[].content`

As the name suggests, it is the content of the subsection. You can define the type of content you want to display. Let's talk about each field in the content.

!!! information "Note"

      Content can be part of each `subsection` or the `section` itself.

=== ":material-layers-triple: Type"

    ```{ .json .copy .select .annotate hl_lines="21"}
    {
      "firstName": "Rahul",
      "middleName": "",
      "lastName": "Agarwal",
      "links": [],
      "resume": {
        "sections": [
          {
            "heading": "Experience",
            "subsections": [{
              "heading": "SAP Labs India",
              "info": {
                "title": "Software Engineer",
                "sameLine": true
              },
              "metadata": {
                "duration": "July 2019 - Present",
                "location": "Bangalore, India"
              },
              "content": {
                "type": "list|paragraph|table" // (1)
              }
            }]
          }
        ]
      }
    }
    ```

    1. :warning: Required. Defines the type of content you want to display in the subsection.

=== ":material-border-style: Style"

    ```{ .json .copy .select .annotate hl_lines="22-25"}
    {
      "firstName": "Rahul",
      "middleName": "",
      "lastName": "Agarwal",
      "links": [],
      "resume": {
        "sections": [
          {
            "heading": "Experience",
            "subsections": [{
              "heading": "SAP Labs India",
              "info": {
                "title": "Software Engineer",
                "sameLine": true
              },
              "metadata": {
                "duration": "July 2019 - Present",
                "location": "Bangalore, India"
              },
              "content": {
                "type": "list|paragraph|table",
                "style": {
                  "showBullet": true, // (1)
                }
              }
            }]
          }
        ]
      }
    }
    ```

    1. :material-help-circle: Optional. Defines if the bullet should be displayed in the list. Default is `true`.

    Currently, only `showBullet` is supported. More styles will be added in the future.

#### List

`Use Case 1`

Let's say you wanna simply display two points in the list. Something like this.

> 1. Developed and implemented a Visual Studio Code extension that streamlined project onboarding processes, reducing setup time by 60% and enhancing productivity for 1,500+ developers across multiple product teams.
> 2. Developed a centralized onboarding platform that consolidated all pre-joining requirements for scholar programs, establishing a single source of truth that processes 150+ new graduates annually and reducing onboarding complexity by eliminating multiple touchpoints.

The json would look something like this.

```{ .json .copy .select .annotate hl_lines="20-41"}
{
  "firstName": "Rahul",
  "middleName": "",
  "lastName": "Agarwal",
  "links": [],
  "resume": {
    "sections": [
      {
        "heading": "Experience",
        "subsections": [{
          "heading": "SAP Labs India",
          "info": {
            "title": "Software Engineer",
            "sameLine": true
          },
          "metadata": {
            "duration": "July 2019 - Present",
            "location": "Bangalore, India"
          },
          "content": {
            "type": "list",
            "style": {
              "showBullet": true
            },
            "items": [
              {
                "segments": [
                  {
                    "text": "Developed and implemented a Visual Studio Code extension that streamlined project onboarding processes, reducing setup time by 60% and enhancing productivity for 1,500+ developers across multiple product teams."
                  }
                ]
              },
              {
                "segments": [
                  {
                    "text": "Developed a centralized onboarding platform that consolidated all pre-joining requirements for scholar programs, establishing a single source of truth that processes 150+ new graduates annually and reducing onboarding complexity by eliminating multiple touchpoints."
                  }
                ]
              }
            ]
          }
        }]
      }
    ]
  }
}
```

`Use Case 2`

Now let say you wanna underline some parts of the text & make some text bold. Something like this.

> 1. Developed and implemented a {==<b>Visual Studio Code extension</b>==} that streamlined project onboarding processes, reducing setup time by 60% and {==^^enhancing productivity for 1,500+ developers(underline)^^==} across multiple product teams.

The json would look something like this.

```{ .json .copy .select .annotate hl_lines="20-59"}
{
  "firstName": "Rahul",
  "middleName": "",
  "lastName": "Agarwal",
  "links": [],
  "resume": {
    "sections": [
      {
        "heading": "Experience",
        "subsections": [{
          "heading": "SAP Labs India",
          "info": {
            "title": "Software Engineer",
            "sameLine": true
          },
          "metadata": {
            "duration": "July 2019 - Present",
            "location": "Bangalore, India"
          },
          "content": {
            "type": "list",
            "style": {
              "showBullet": true
            },
            "items": [
              {
                "segments": [
                  {
                    "text": "Developed and implemented a"
                  },
                  {
                    "text": "Visual Studio Code extension",
                    "style": {
                      "bold": true // (1)
                    }
                  },
                  {
                    "text": "that streamlined project onboarding processes, reducing setup time by 60% and"
                  },
                  {
                    "text": "enhancing productivity for 1,500+ developers",
                    "style": {
                      "underline": true // (2)
                    }
                  },
                  {
                    "text": "across multiple product teams."
                  }
                ]
              },
              {
                "segments": [
                  {
                    "text": "Developed a centralized onboarding platform that consolidated all pre-joining requirements for scholar programs, establishing a single source of truth that processes 150+ new graduates annually and reducing onboarding complexity by eliminating multiple touchpoints."
                  }
                ]
              }
            ]
          }
        }]
      }
    ]
  }
}
```

1. :material-help-circle: Optional. Defines if the text should be displayed in bold. Default is `false`.
2. :material-help-circle: Optional. Defines if the text should be displayed in underline. Default is `false`.

Following are the supported styles.

```{ .json .copy .select}
{
  "bold": true|false,
  "italic": true|false,
  "underline": true|false,
}
```

#### Inline List

Let's say you wanna display a list without new lines. Something like this.

> Over 6000 lines:<br />
> Java • JS • PHP • LaTeX<br />
> Over 1000 lines:<br />
> C • C++ • GO <br />
> Familiar:<br />
> Swift • Ruby<br />

The json would look something like this.

```{ .json .copy .select .annotate hl_lines="20-72"}
{
  "firstName": "Rahul",
  "middleName": "",
  "lastName": "Agarwal",
  "links": [],
  "resume": {
    "sections": [
      {
        "heading": "Experience",
        "subsections": [{
          "heading": "SAP Labs India",
          "info": {
            "title": "Software Engineer",
            "sameLine": true
          },
          "metadata": {
            "duration": "July 2019 - Present",
            "location": "Bangalore, India"
          },
          "content": {
            "type": "list",
            "style": {
              "showBullet": false
            },
            "items": [
              {
                "segments": [
                  {
                    "text": "Over 6000 lines:"
                  },
                  "inlineList": { // (1)
                    "separator": "•",
                    "items": [
                      "Java",
                      "JS",
                      "PHP",
                      "LaTeX"
                    ]
                  }
                ]
              },
              {
                "segments": [
                  {
                    "text": "Over 1000 lines:"
                  },
                  "inlineList": {
                    "separator": "•",
                    "items": [
                      "C",
                      "C++",
                      "GO"
                    ]
                  }
                ]
              },
              {
                "segments": [
                  {
                    "text": "Familiar:"
                  },
                  "inlineList": {
                    "separator": "•",
                    "items": [
                      "Swift",
                      "Ruby"
                    ]
                  }
                ]
              },
            ]
          }
        }]
      }
    ]
  }
}
```

1. :material-help-circle: Optional. Defines the inline list, which means list without new lines. You can define the separator and the items.

#### Paragraph

Take an example where you wanna display a paragraph. Something like this.

> Developed and implemented a Visual Studio Code extension that streamlined project onboarding processes, reducing setup time by 60% and enhancing productivity for 1,500+ developers across multiple product teams.

> Developed a centralized onboarding platform that consolidated all pre-joining requirements for scholar programs, establishing a single source of truth that processes 150+ new graduates annually and reducing onboarding complexity by eliminating multiple touchpoints.

The json would look something like this.

```{ .json .copy .select .annotate hl_lines="20-38"}
{
  "firstName": "Rahul",
  "middleName": "",
  "lastName": "Agarwal",
  "links": [],
  "resume": {
    "sections": [
      {
        "heading": "Experience",
        "subsections": [{
          "heading": "SAP Labs India",
          "info": {
            "title": "Software Engineer",
            "sameLine": true
          },
          "metadata": {
            "duration": "July 2019 - Present",
            "location": "Bangalore, India"
          },
          "content": {
            "type": "paragraph",
            "items": [
              {
                "segments": [
                  {
                    "text": "Developed and implemented a Visual Studio Code extension that streamlined project onboarding processes, reducing setup time by 60% and enhancing productivity for 1,500+ developers across multiple product teams."
                  }
                ]
              },
              {
                "segments": [
                  {
                    "text": "Developed a centralized onboarding platform that consolidated all pre-joining requirements for scholar programs, establishing a single source of truth that processes 150+ new graduates annually and reducing onboarding complexity by eliminating multiple touchpoints."
                  }
                ]
              }
            ]
          }
        }]
      }
    ]
  }
}
```

#### Table

Let's say you have an awards section where you wanna display the awards in a table. Something like this.

> |      |         |
> | ---- | ------- |
> | 2021 | Award 1 |
> | 2022 | Award 2 |

!!! warning "Note"

      Ignore the weird table header formatting. It's just for the sake of understanding.

The json would look something like this.

```{ .json .copy .select .annotate hl_lines="20-26"}
{
  "firstName": "Rahul",
  "middleName": "",
  "lastName": "Agarwal",
  "links": [],
  "resume": {
    "sections": [
      {
        "heading": "Experience",
        "subsections": [{
          "heading": "SAP Labs India",
          "info": {
            "title": "Software Engineer",
            "sameLine": true
          },
          "metadata": {
            "duration": "July 2019 - Present",
            "location": "Bangalore, India"
          },
          "content": {
            "type": "table",
            "rows": [
              ["2021", "Award 1"],
              ["2022", "Award 2"]
            ]
          }
        }]
      }
    ]
  }
}
```

!!! warning "Note"

      The table is a simple table with rows only. More complex tables will be supported in the future.

#### Additional: Links

Let's say you wanna add links to the list or paragraph. Something like this.

> 1. You can connect me on {==[LinkedIn](https://www.linkedin.com/in/ragarwalll/).==}
> 2. Here is my {==[Github](https://www.github.com/ragarwalll)==} profile.

The json would look something like this.

```{ .json .copy .select .annotate hl_lines="20-52"}
{
  "firstName": "Rahul",
  "middleName": "",
  "lastName": "Agarwal",
  "links": [],
  "resume": {
    "sections": [
      {
        "heading": "Experience",
        "subsections": [{
          "heading": "SAP Labs India",
          "info": {
            "title": "Software Engineer",
            "sameLine": true
          },
          "metadata": {
            "duration": "July 2019 - Present",
            "location": "Bangalore, India"
          },
          "content": {
            "type": "list|paragraph",
            "items": [
              {
                "segments": [
                  {
                    "text": "You can connect me on"
                  },
                  {
                    "text": "LinkedIn",
                    "href": "https://www.linkedin.com/in/ragarwalll/",
                    "style": {
                      "bold": true
                    }
                  }
                ]
              },
              {
                "segments": [
                  {
                    "text": "Here is my"
                  },
                  {
                    "text": "Github",
                    "href": "https://www.github.com/ragarwalll"
                  },
                  {
                    "text": "profile.",
                  }
                ]
              }
            ]
          }
        }]
      }
    ]
  }
}
```
