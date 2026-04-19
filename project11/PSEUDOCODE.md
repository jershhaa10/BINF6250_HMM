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
    sequence_label = Initialize "Begin" to hold each sequence by label
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
    sequence_label.append("End")
    Append sequence_label to labeled sequences

```



## Step 4: Estimate Initial Emissions Count
Rules:
* Match Cases: Position-specific distributions (Count residues at each position for each sequence in msa)
  * This is a consensus column
* Insertion Cases: Compute global aa freq from all training sequences and use background distribution for all $I_i$ states
  * This is extra residues in between consensus columns
* Deletion Cases: No emission
  * This is silence between consensus columns
* Pseudocounts are applied to avoid zeroes

```
Input
* sequences_by_positions
* state_type

* Return an emissions probability dictionary

# Initialization
* emit_probs = {}
* pseudocount = 0.01

# Iteration
for position in len(state_types):
    Initialize a counts dictionary with amino acids labels as keys and pseudocounts as values
    # Match Cases
    if state_type[pos].startswith("M"):
        Get position residues = sequences_by_positions[pos]
        for res in position residues:
            if res not in ['-', "Begin", "End"]:
                counts dictionary[res] +=1
        Calculate total across values in count dictionary
        emit_probs[state_type[pos]] = {amino acids: count dictionary[amino acids] / total for specific amino acid in alphabet}

    # Insertion case
    if state_type_pos.startswith("I"):
        Initialize a background counts dictionary with amino acids labels as keys and pseudocounts as values
        Iterate through each sequence
            for each residue in sequence
                if res not in ['-', "Begin", "End"]:
                    Add count to amino acid in background count dictionary
        Calculate total across values in background count dictionary
        emit_probs[state_type[pos]] = {amino acids: background count dictionary[amino acids] / total for specific amino acid in alphabet}
```

## Step 5: Estimate Initial Transitions Count
**Pre Step: Build list of states (once we figure out state types (Step 1))**
```
*Input: Consensus length
*Output: List of states
states = ["Begin", "I0"]
for index, range(1, Consensus length + 1):
  states += [f"M{i}", f"I{i}", f"D{i}"]
states.append("End")
```

**Step A: Define Transition Rules**
```
* Input: State, Next State (Example: M1, M2 or M1, D2), Consensus Length
* Returns Boolean which confirms if current state can transition to next_state

if state == "Begin":
    return True if next_state is in ["M1", "I0", "D1"]
if state == "End":
    return False since pHMM are directed graphs flowing from left to right

n = Get the number for the state  (Example: If M3, n=3)

if state starts with "M" # Match
    if n == consensus length:
            return next_state in ["End"]
    else return True if next_state is in [M[n+1], I[[n], D[n+1]]
if state starts with "I" # Insertion
    if n == consensus length:
        return next_state in ["End"]
    else return True if next_state is in [I[n], M[n+1]]
if state starts with "D" # Deletion
    if n == length:
            return next_state in ["End"]
    return True if next_state is in [M[n+1], D[n+1], End]
    
Else return False
```

**Step B: Build Transition Skeleton**
```
Input: states, pseudocounts = 0.01
Return: Dictionary transition_counts skeleton with tuples defining valid transitions (prev_state, next_state) as keys and pseudocounts as values 

transition_counts = {}
for prev_state in states:
    for next_state in states:
        if Transition_Rules(prev_state, next_state) returns True as valid transition states
            transition_counts(state, next_state) = pseudocount
return  transition_counts   
```

**Step C: Compute Transition Counts**
```
Input 
* Consensus Length, labeled sequences (msa)
Return
* Dictionary transition_counts with tuples defining valid transitions (prev_state, next_state) as keys and actual counts as values
 
states = build_states(consensus length)
Initialize transition counts with transition skeleton
for seqs in labeled sequences:
  Index through labeled sequences:
    transition_counts[(seq[i], seq[i+1] += 1
```

**Step D: Normalize to Transition Probabilities**
```
Input
* labeled sequences (msa)
* states
Return
* Dictionary of dictionaries transition probs where outer key == prev_state and inner keys are outgoing states, values are transition probs of prev_state -> outgoing state

Get Trans counts dictionary inputting labeled sequences in function
trans_probs = {}

for state in states
  if state != 'End'
    outgoing = {k[1]: v for k, v in trans_counts.items() if k[0] == state}
  if outgoing: 
    total = Calculate the total across values for specific state
    for next_state, count in outgoing.items()
      trans_probs[state][next_state] = count / total 
```
