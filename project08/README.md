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
We had a solid game plan going in and did some solid peer programming. We kept in touch over the week and met several times and tried to make sure all our group members understood code as we went.

# Struggles
We all feel like we are a bit weaker on implementing custom class objects, so this was a good opportunity to learn but also meant we spent a lot of time figuring out how to configure everything.
Late on Tuesday we realized that we needed to move our functions inside the class object so we spent a lot of time updating that last minute.
We also got a tip about handling ties and felt like we didn't have enough time to implement that so we will try to get it in the next project.

# Personal Reflections
## Victoria Van Berlo
This project required an approach I'm not used to. This project required us to keep the class object implementation in the back of our minds, so that the functions would suit the class setup and the class methods and variables would suit the functions. It was also an interesting challenge to create such a generalized implementation to suit any number of states and observations that were fed into it.

## Other member
Other members' reflections on the project

## Other member
Other members' reflections on the project

# Generative AI Appendix
Generative AI was not used in this project.