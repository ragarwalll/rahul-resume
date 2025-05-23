# LaTeX Engine

In simple terms, the LaTeX engine is responsible for generating the resume from the LaTeX file generated by the python pre-processor. The LaTeX engine uses the [XeLaTeX](https://www.overleaf.com/learn/latex/XeLaTeX) compiler to generate the PDF file.

We have a LaTeX Class file that defines the structure of the resume. The class file is used to generate the resume from the LaTeX file generated by the python pre-processor.

Find the class file for the LaTeX template [here.](https://github.com/ragarwalll/rahul-resume/blob/main/resume.cls)

## Components in the LaTeX Engine

```mermaid
classDiagram
    class ResumeClass {
        +\NeedsTeXFormat()
        +\ProvidesClass()
        +\DeclareOption()
        +\ProcessOptions()
        +\LoadClass()
    }

    class RequiredPackages {
        +geometry
        +xcolor
        +hyperref
        +titlesec
        +textpos
        +babel
        +isodate
        +setspace
        +enumitem
        +paracol
        +ulem
        +fontspec
        +xltxtra
        +xunicode
        +xfp
        +multicol
    }

    class Commands {
        +\applysettings()
        +\loadpresent()
        +\overridesetting()
    }

    class Modifiers {
        +scaling-factor
        +default
        +colors
        +fonts
        +sections
        +sub-sections
        +tightemize
        +tightnopoints
    }

    class CustomCommands {
        +last-updated
        +name-section
        +alt-sub-section
        +section-seperator
        +info
        +additional-info
        +json-processor
        +trim-spaces
    }

    ResumeClass --> RequiredPackages
    ResumeClass --> Commands
    Commands --> Modifiers
    Commands --> CustomCommands
```

## How does it work?

```mermaid
sequenceDiagram
    participant User
    participant ResumeClass
    participant Settings
    participant Modifiers
    participant Commands

    User->>ResumeClass: Load Class
    activate ResumeClass
    ResumeClass->>ResumeClass: Process Options
    ResumeClass->>ResumeClass: Load Required Packages
    ResumeClass->>Settings: Load Default Settings
    activate Settings
    Settings->>Modifiers: Apply Default Modifiers
    activate Modifiers
    Modifiers->>Modifiers: Load Colors
    Modifiers->>Modifiers: Load Fonts
    Modifiers->>Modifiers: Load Sections
    Modifiers->>Modifiers: Load Sub-sections
    deactivate Modifiers
    Settings->>Commands: Load Custom Commands
    activate Commands
    Commands->>Commands: Register Commands
    deactivate Commands
    deactivate Settings
    ResumeClass->>User: Ready for Content
    deactivate ResumeClass
```
