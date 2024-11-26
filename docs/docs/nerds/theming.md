# Theming

we have defined a set of variables that you can use to customize the look and feel. This basically consists of the following components:

- **Colors**: The color palette used in the theme.
- **Typography**: The font family and sizes used in the theme.
- **Spacing**: The spacing used in the theme.
- **Presets**: The default theme options.

!!! warning

    This is only applicable when you want to use & customize the default theme in local

## Colors

Let's get a little technical here. We have 4 customizations for colors:

- `datecolor`
- `primarycolor`
- `headingscolor`
- `subheadingscolor`

To customize the colors, you can create a new file in this path [`theme/colors`](https://github.com/ragarwalll/rahul-resume/tree/main/theme/colors) and add the following code:

```tex
% theme/colors/deedy-inspired.tex - Deedy-inspired color definitions

\def\datecolor{666666}
\def\primarycolor{2b2b2b}
\def\headingscolor{6A6A6A}
\def\subheadingscolor{333333}
```

## Typography

We have define all the font family along with each font family LaTeX options.

- `thinfont`
- `extralightfont`
- `lightfont`
- `defaultfont`
- `mediumfont`
- `boldfont`
- `extraboldfont`

We also have some custom font defined for resume specific.

- `firstnamefont`
- `lastnamefont`
- `profilelinksfont`
- `lastupdatedfont`
- `sectionfont`
- `subsectionfont`
- `infofont`
- `additionalinfofont`

Similarly, if you want to define some options for the font, use the `{font-type}options`. Please find all the available options [here](https://github.com/ragarwalll/rahul-resume/blob/main/theme/presets/default.tex)

Similarly, you can customize the typography by creating a new file in this path [`theme/fonts`](https://github.com/ragarwalll/rahul-resume/tree/main/theme/fonts). The idea here is to have file for each font family.

```tex
% theme/fonts/deedy-inspired.tex - Deedy-inspired fonts

\def\thinfont{Lato-Hai}
\def\extralightfont{Lato-Hai}
\def\lightfont{Lato-Lig}
\def\defaultfont{Lato-Reg}
\def\mediumfont{Lato-Reg}
\def\semiboldfont{Lato-Bol}
\def\boldfont{Lato-Bol}
\def\extraboldfont{Lato-Bla}
%
\def\fontpath{fonts/lato/}
%
%
\def\mainfontoptions{BoldItalicFont=Lato-RegIta,BoldFont=Lato-Reg,ItalicFont=Lato-LigIta}%
```

## Spacing

Spacing basicaly define the font size and line height. Currently, we use the `goldern-ratio` for the line height. Following variables are available for customization:

- `tinyfontsize`
- `scriptfontsize`
- `footnotefontsize`
- `smallfontsize`
- `normalfontsize`
- `largefontsize`
- `largerfontsize`
- `largestfontsize`
- `hugefontsize`
- `hugestfontsize`

We can also override the line height for each font size using the following variables:

- `tinyfontheight`
- `scriptfontheight`
- `footnotefontheight`
- `smallfontheight`
- `normalfontheight`
- `largefontheight`
- `largerfontheight`
- `largestfontheight`
- `hugefontheight`
- `hugestfontheight`

We also have some custom spacing defined for resume specific.

- `infofontsize`
- `additionalinfofontsize`
- `infofontheight`
- `additionalinfofontheight`

Similarly, you can customize the spacing by creating a new file in this path [`theme/sizes`](https://github.com/ragarwalll/rahul-resume/tree/main/theme/sizes)

```tex
% theme/sizes/golden-ration.tex - sizes for the PDF%
%
% Base fontsize and ratio%
\def\normalfontsizepoint{12}%
\def\goldenratio{1.618}%
%
% Define all font fontsizes and line fontheights%
\def\tinyfontsize{\fpeval{\normalfontsizepoint/(\goldenratio*\goldenratio*\goldenratio)}pt}%
\def\tinyfontheight{\fpeval{(\normalfontsizepoint/(\goldenratio*\goldenratio*\goldenratio))*\goldenratio*\spacingscale}pt}%
%
\def\scriptfontsize{\fpeval{\normalfontsizepoint/(\goldenratio*\goldenratio)}pt}%
\def\scriptfontheight{\fpeval{(\normalfontsizepoint/(\goldenratio*\goldenratio))*\goldenratio*\spacingscale}pt}%
%
\def\footnotefontsize{\fpeval{\normalfontsizepoint/(\goldenratio*1.2)}pt}%
\def\footnotefontheight{\fpeval{(\normalfontsizepoint/(\goldenratio*1.2))*\goldenratio*\spacingscale}pt}%
%
\def\smallfontsize{\fpeval{\normalfontsizepoint/\goldenratio}pt}%
\def\smallfontheight{\fpeval{(\normalfontsizepoint/\goldenratio)*\goldenratio*\spacingscale}pt}%
%
\def\normalfontsize{\normalfontsizepoint pt}%
\def\normalfontheight{\fpeval{\normalfontsizepoint*\goldenratio*\spacingscale}pt}%
%
\def\largefontsize{\fpeval{\normalfontsizepoint*\goldenratio}pt}%
\def\largefontheight{\fpeval{\normalfontsizepoint*\goldenratio*\goldenratio*\spacingscale}pt}%
%
\def\largerfontsize{\fpeval{\normalfontsizepoint*\goldenratio*1.2}pt}%
\def\largerfontheight{\fpeval{\normalfontsizepoint*\goldenratio*1.2*\goldenratio*\spacingscale}pt}%
%
\def\largestfontsize{\fpeval{\normalfontsizepoint*\goldenratio*\goldenratio}pt}%
\def\largestfontheight{\fpeval{\normalfontsizepoint*\goldenratio*\goldenratio*\goldenratio*\spacingscale}pt}%
%
\def\hugefontsize{\fpeval{\normalfontsizepoint*\goldenratio*\goldenratio*1.2}pt}%
\def\hugefontheight{\fpeval{\normalfontsizepoint*\goldenratio*\goldenratio*1.2*\goldenratio*\spacingscale}pt}%
%
\def\hugestfontsize{\fpeval{\normalfontsizepoint*\goldenratio*\goldenratio*\goldenratio}pt}%
\def\hugestfontheight{\fpeval{\normalfontsizepoint*\goldenratio*\goldenratio*\goldenratio*\goldenratio*\spacingscale}pt}%
%
\def\infofontsize{\fpeval{\normalfontsizepoint-1}pt}%
\def\infofontheight{\fpeval{(\normalfontsizepoint-1)*\goldenratio*\spacingscale}pt}%
%
\def\additionalinfofontsize{\fpeval{\normalfontsizepoint-2}pt}%
\def\additionalinfofontheight{\fpeval{(\normalfontsizepoint-2)*\goldenratio*\spacingscale}pt}%
```

## Presets

Now that we have defined all the colors, typography and spacing, we can define the default theme options. You can create a new file in this path [`theme/presets`](https://github.com/ragarwalll/rahul-resume/tree/main/theme/presets)

This basically means, we can have hybrid fonts, color etc.

```tex
% theme/predefined/deedy-inspired-open-fonts.tex -  theme for the PDF
%
% loads colors%
\input{theme/colors/deedy-inspired.tex}%
%
% XeLaTeX specifc fonts%
\input{theme/fonts/lato.tex}%
\let\mainfont\lightfont%
\let\sectionfont\lightfont%
\let\subsectionfont\boldfont%
\let\firstnamefont\thinfont%
\let\lastnamefont\lightfont%
%
%
\let\mainfontpath\fontpath%
\let\sectionfontpath\fontpath%
\let\subsectionfontpath\fontpath%
\let\firstnamefontpath\fontpath%
\let\lastnamefontpath\fontpath%
%
%
\input{theme/fonts/raleway.tex}%
\let\sansfont\extralightfont%
\let\lastupdatedfont\extralightfont%
\let\profilelinksfont\mediumfont%
\let\infofont\mediumfont%
\let\additionalinfofont\mediumfont%
```
