# golden_globes

To start developing, make sure you activate the virtual environment. Make sure pip and Python are version 3.
	
	* python -m venv env 
	* source env/bin/activate
	* pip install -r requirements.txt

When done, you can leave the virtual environment with:
	
	* deactivate



## Testing

To use the autograder, first run `golden_globes.py 2013` from the command line, replacing 2013 with the desired year. The script assumes there is a JSON file called `gg2013.json` in the `/data` folder (or for target year).

After the script has been run, cd into `/autograder` and run `autograder.py 2013`, or with whichever year you've generated results for. 

## Grading
When using the autograder as 'python autograder.py {year}', ensure that the relevant data file for {year} is in data folder
