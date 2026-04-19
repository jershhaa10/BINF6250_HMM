## Pseudocode for Step 2: Assign State to Columns
```
Input: List of Sequences
Return: List of State Types

# Initialization
* Empty List for State Type
* match_case = 0
* sequences_by_positions = Transpose sequences by positions using zip(*list)

# Iteration
Iterate through each position:
    initialize a gap count to 0
    for index in list of residues of position:
        Update count if position is gap ('-')
    Calculate percentage of gaps by dividing by number of sequences
    if gap_count <= 0.5:
        This is a match case
        append M{match_case+1} to state type list
        Add 1 to match_case
    else if gap_count > 0.5:
        This is an insertion case
        append I{match_case} to state type list
```

## Step 3: Label Each Sequence
```
Input: List of sequences, state_types
Return: List of Lists where each list is the labels of the residue for each position
# Initialization
* A list to hold labeled sequences

# Iteration
for each sequence:
    match_case = 0
    sequence_label = Initialize an empty list to hold each sequence by label
    for i, residue in enumerate(sequence):
        if residue is '-' and state_type[i] starts with 'M':
            # This represents a deletion
            Append to sequence_label D{match_case+1}
            match_case+= 1
        elif res is in alphabet and state_type[i] starts with 'M':
            # This is a match case
            Append to sequence_label M{match_case +1}
            match_case +=1
        elif res is in alphabet and state_type[i] starts with "I":
            # This is an insertion
            Append to sequence_label I{match_case}

    Append sequence_label to labeled sequences

```

