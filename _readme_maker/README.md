# Readme maker

The script `make_readme` will
* Use `README.md.template` as a template
* Slurp the content from `history.txt` (markdown) and put it where the `{history.txt}` placeholder is. 
* Replace `{content}` with a list of directories and their content as processed by the script, in order to add links and directory size
* Automatically save the output in `../README.md`
