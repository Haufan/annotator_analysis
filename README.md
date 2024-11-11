annotator_analysis_from_rs3.py
This Python script processes .rs3 files, which are XML files used in the context of text segmentation and relation analysis, and generates detailed analyses of the tree structures and relations contained within the files.

Features
Parse RS3 files: Extracts segments, groups, relations, and other relevant information from .rs3 files.
Tree Structure Construction: Builds a hierarchical tree from the extracted segments and groups.
Relation Analysis: Analyzes the relations between nodes in the tree and provides a breakdown of their occurrence and position (top, middle, bottom).
Command-line Interface (CLI): Allows processing of .rs3 files from a specified directory.
Requirements
Python 3.x
Dependencies:
xml.etree.ElementTree (Part of Python's standard library)
collections (Part of Python's standard library)
No external dependencies are required beyond the Python standard library.

Usage
Command-line Usage
To run the script, use the following command in your terminal:

bash
Copy code
python annotator_analysis_from_rs3.py <directory_path>
Where <directory_path> is the full path to the directory containing the .rs3 files you want to process.

For example:

bash
Copy code
python annotator_analysis_from_rs3.py "C:/Users/haufa/OneDrive/Desktop/hiwi/Annotationsvergleich/RST"
This command will:

Search the provided directory for all .rs3 files.
Process each .rs3 file found.
For each file, the script will:
Parse the RS3 data.
Build a hierarchical tree structure.
Perform an analysis of relations and their positions.
Write the output to a text file named <file_name>_analysis.txt.
Output
For each .rs3 file processed, the script creates a new text file with the following sections:

Tree Structure: A visual representation of the hierarchical structure of segments and groups in the file.
Analysis of Relations and Positions: A breakdown of the types of relations found, including how often each relation appears and its distribution across the tree (top, middle, bottom).
Example output file name: UP_academic_census-Dietrmar.rs3_analysis.txt

Example Output
For a file example.rs3, the output might look like:

yaml
Copy code
Tree Structure:
1: Die Kränzliner , Mankerer , Wustrauer , Walchower und Protzener fühlen sich ungerecht behandelt . (relname: reason-N)
├── 2: Segment text here (relname: result)
└── 3: Another segment (relname: reason-N)

Analysis of Relations and Positions:
reason-N: 2 times (top: 1 times, bottom: 1 times)
result: 1 times (middle: 1 times)
Functions
parse_rs3(file_path)
Parses the RS3 file at file_path, extracting segments, groups, and relation types. Returns dictionaries for segments and groups, a nested dictionary tracking relation counts and directions, and lists of 'rst' and 'multinuc' relation types.

build_tree(nodes_data, structure_data)
Constructs a hierarchical tree from node and structure data. Returns the root node of the tree.

print_tree(root)
Prints the tree structure rooted at root.

analyze_relations_and_positions(root)
Analyzes the relations and their positions in the tree structure. Outputs counts of each relation type and their distribution across top, middle, and bottom positions in the tree.

find_rs3_files(directory)
Finds all .rs3 files in the specified directory and its subdirectories.

process_rs3_file(file_path)
Processes a single .rs3 file, builds the tree, analyzes it, and writes the results to an output file.

Example Workflow
Prepare Your RS3 Files: Ensure your .rs3 files are located in a directory on your computer.
Run the Script: Use the command-line interface to point to the directory containing the .rs3 files.
Review Output: After processing, you will have a set of analysis files (<file_name>_analysis.txt) in the same directory.
Contributing
If you would like to contribute improvements to the script, feel free to open an issue or submit a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.

