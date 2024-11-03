% chktex-file 44
% chktex-file 27

% resume.cls - A class file for LaTeX to create a resume    
% @author: ragarwalll
% @inspired by: deedy
% @date: 2024/11/02
% @version: 1.0
% @license: Apache License 2.0

% The format of this file is LaTeX2e.
% You can use it as a template for your own resume by replacing the text with your own information.
% You will need to have LaTeX installed on your computer to compile it.  
% If you don't have LaTeX installed, you can use an online LaTeX editor such as Overleaf.
\NeedsTeXFormat{LaTeX2e}

% This is resume.cls
% It is a class file for LaTeX that defines the formatting for a resume
\ProvidesClass{resume}[2024/11/02 Resume Class]

% This command declares an optional setting for the class that handles print formatting:
% If the print option is used, the class will use a different color scheme that is more suitable for printing.
\DeclareOption{print}{\def\@cv@print{}}

% This is a command that handles any options that weren't specifically declared in your class:
% What it does:
% \DeclareOption* catches all options that weren't explicitly defined
% \PassOptionsToClass forwards these options to the 'article' class
% \CurrentOption represents whatever option was passed
\DeclareOption*{
  \PassOptionsToClass{\CurrentOption}{article}%
}

% This command processes the options that were declared in the class file:
\ProcessOptions\relax

% This command loads the 'article' class with the options that were passed to the 'ragarwall-resume' class:
\LoadClass{article}

% This command loads the 'geometry' package with the specified options
\usepackage[hmargin=1.25cm, vmargin=0.7cm]{geometry}

% This command loads the 'xcolor' package with the specified options
\usepackage[usenames,dvipsnames]{xcolor}

% Load the 'hyperref' package with normal looking text as the link
\usepackage[hidelinks]{hyperref}

% This command loads the 'titlesec' package with the custom formatting for the sections
\usepackage{titlesec}

% This command loads the 'textpos' package which will allow text to be positioned at an absolute position on the page
\usepackage[absolute]{textpos}

% This command loads the 'babel' package with formatting for UK English
\usepackage[UKenglish]{babel}

% This command loads the 'isodate' package with formatting for UK English dates
\usepackage[UKenglish]{isodate}

% enable the following
% system fonts (TTF/OTF)
% Extra features for XeLaTeX
% Provides Unicode support
\usepackage{fontspec,xltxtra,xunicode}

% This command loads the 'xfp' package which provides floating point operations
\RequirePackage{xfp}

% Command to apply all settings
\newcommand{\applysettings}{

  % Apply the default modifers
  \input{modifiers/default.tex}

  % Apply the custom modifiers
  \input{modifiers/colors.tex}
  \input{modifiers/fonts.tex}
  \input{modifiers/sections.tex}
  \input{modifiers/sub-sections.tex}

  % load the custom commands
  \input{cmd/last-updated.tex}
  \input{cmd/name-section.tex}
  \input{cmd/each-sub-section.tex}
  \input{cmd/descriptor.tex}
  \input{cmd/location.tex}

}

% Command to load present
\newcommand{\loadpresent}[1]{
  % Always load defaults first
  \input{theme/presets/default.tex}
  % Then load specific preset if provided
  \IfFileExists{theme/presets/#1.tex}{
    \input{theme/presets/#1.tex}
  }{}

  \input{modifiers/default-fonts.tex}
  \input{cmd/debug.tex}
  \applysettings{}

}

% Command to override specific settings
\newcommand{\overridesetting}[2]{
  \expandafter\def\csname @#1\endcsname{#2}
}