# What It Does

This script is designed to make regularizing strings from data relatively painless. It uses fuzzy matching to compare a string with every other string in the data, retrieving the best match either from items that have already been regularized (preferentially) or from strings that have not yet had a similar comparison run.

# Running the Script

When you run the script, it will produce output like the below:

```
Processing possible misspellings. You may hit ctrl+C at any point to exit, or enter `e` at the prompt. Progress will be saved.

1/265
Matching Institute for Health Metrics and Evaluation:
Choose the best version:
[0] Institute for Health Metrics and Evaluation
[1] Institute of Health Metrics and Evaluation
[2] Institute for Health Metric and Evaluation

[r] Remove one or more matches
[c] Enter a better version of all
[e] Save and exit
Selection:
```

Remove any values that aren't actually "the same" from this list, then either select or enter the "correct" version. Ideally this will be the organization's name in the [Reasearch Organization Registry](https://ror.org/).

```
Institute of Health Metrics and Evaluation, Institute for Health Metric and Evaluation recorded as duplicates of Institute for Health Metrics and Evaluation
```

You can exit at any time using Ctrl + C to kill the script, or by entering `e` (really, anything but a valid selection) at the selection prompt.

The script then tries to get ROR organization IDs for each cleaned value and adds them to the final dataframe, if available. This will perform the matching on the list of ROR names, if
the current cleaned name is not found in that list. This can take a while, because the list is long and fuzzy matching is expensive. Use `--skip-rematch-for-ror` to skip this matching attempt.

Finally, you'll get the truncated, sorted counts of each organization out. The full dataframe will be saved to `cleaned_organizations.csv` in the `data` folder.

## Options

Run `python -m process_data -h` to see a list of options.

### Adjusting the Match Sensitivity

I believe the default sensitivity is set reasonably well. However, if you'd like to make matching more or less sensitive, pass the argument `--match-score` to the command. The default value is 90. This is approximately a percentage; adjust accordingly. For example, to make strings match only if they're already almost perfect, run `python -m process_data --match-score 99`. On the other hand, to make some pretty bad matches appear, run `python -m process_data --match-score 80`.

### Rescanning previously-unmatched strings

If you'd like to go over strings that were previously thought to be unique with a lower match sensitivity or new data, pass `--rescan-non-dupes`. Because this set gets smaller each time you find a match, processing over lower and lower `match-score`s seems likely to be a useful strategy, though you'll reach a point of diminishing returns where most matches are just noise (at which point, congrats, I guess it's done!).

# Manual Checks

If you'd like to double-check the items that have been marked as duplicates, or marked as non-duplicates, you can look at the JSON files in the `data` folder. These are always in alphabetical order. Additionally, the ROR data is available in alphabetical order, if you think an item without a ROR ID should have one and the matching isn't finding it.

# Updating the ROR Data

A utility for updating the ROR data is provided. Update the path to the raw JSON data (from https://zenodo.org/records/10278793) and run the script.
