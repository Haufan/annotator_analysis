# annotator_analysis_from_rs3.py
This Python script processes .rs3 files, which are XML files used in the context of text segmentation and relation analysis, and generates detailed analyses of the tree structures and relations contained within the files.

## Features
Parse RS3 files: Extracts segments, groups, relations, and other relevant information from .rs3 files.
Tree Structure Construction: Builds a hierarchical tree from the extracted segments and groups.
Relation Analysis: Analyzes the relations between nodes in the tree and provides a breakdown of their occurrence and position (top, middle, bottom).
Command-line Interface (CLI): Allows processing of .rs3 files from a specified directory.

## Requirements
Python 3.x
Dependencies:
xml.etree.ElementTree (Part of Python's standard library)
collections (Part of Python's standard library)
No external dependencies are required beyond the Python standard library.

## Usage
Command-line Usage
To run the script, use the following command in your terminal:

`python annotator_analysis_from_rs3.py <directory_path>`

Where <directory_path> is the full path to the directory containing the .rs3 files you want to process.





