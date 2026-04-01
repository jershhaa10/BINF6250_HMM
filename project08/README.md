# Introduction
Description of the project

# Pseudocode
Put pseudocode in this box:

```

# Viterbi:

probability matrix, traceback matrix = len(states) * len(observation)

for each i, observation
    for each j, state
        if observation [0]:
            prob = current state initial prob * current emission prob 
            prob_matrix[j][i] = log(prob)
        else # calculate all probs possible for this box
            possible_probs =
                for all previous states: [ prev state prob * previous state to current state transition prob * current state emission prob ]
            max_prob = max(possible_probs)
            prob_matrix[j][i] = log(max_prob)

            #fill traceback
            prev_coords = argmax(possible_probs)
            traceback_matrix[j][i] = prev_coords

# Traceback:

end_state = argmax(prob_matrix[:,-1]
predictions = end_state
for i in len(observation) backwards:
    predictions.append (trace_matrix[end_state][i])
reverse predictions

for observation in predictions:
    states_final.append(states[observation])
    
```

# Successes
Description of the team's learning points

# Struggles
Description of the stumbling blocks the team experienced

# Personal Reflections
## Victoria Van Berlo
This project required an approach I'm not used to. This project required us to keep the class object implementation in the back of our minds, so that the functions would suit the class setup and the class methods and variables would suit the functions. It was also an interesting challenge to create such a generalized implementation to suit any number of states and observations that were fed into it.

## Other member
Other members' reflections on the project

## Other member
Other members' reflections on the project

# Generative AI Appendix
Generative AI was not used in this project.