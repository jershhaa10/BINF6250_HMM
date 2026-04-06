def forward_matrix(self, observations):
        prob_matrix = np.zeros((len(self.states), len(observations)), dtype = float)

        ####### Iteration ########
        for i, observation in enumerate(observations):
            for j, state in enumerate(self.states):
                # Get initial and emission probabilities for current state
                state_init_probs = self.initial_probs[state]
                state_emit_probs = self.get_emission_probs(state)

                # calculate probabilities
                # Remember log(x*y) = log(x) + log(y)
                # first column
                if i == 0:
                    state_prob = np.log(state_init_probs) + np.log(state_emit_probs[observation])
                    prob_matrix[j][i] = state_prob

                else:
                    joint_probs = [prob_matrix[k][i-1] +
                                   np.log(self.get_transition_probs(prev_state)[state]) +
                                   np.log(state_emit_probs[observation])
                                   for k, prev_state in enumerate(self.states)]

                    sum_prob = np.logaddexp.reduce(joint_probs)
                    prob_matrix[j][i] = sum_prob

        final_col_prob = np.logaddexp.reduce(prob_matrix[:, -1])
        #print(f'Obs prob is {final_col_prob}')
        return prob_matrix, final_col_prob

    def backward_matrix(self, observations):
        prob_matrix = np.zeros((len(self.states), len(observations)), dtype = float)
        observations = observations[::-1]

        for i, observation in enumerate(observations):
            for j, state in enumerate(self.states):
                joint_probs = [prob_matrix[k][i-1] +
                           np.log(self.get_transition_probs(state)[next_state]) +
                           np.log(self.get_emission_probs(next_state)[observation])
                           for k, next_state in enumerate(self.states)]

                prob_matrix[j][i] = np.logaddexp.reduce(joint_probs)

        final_col_prob = np.logaddexp.reduce(prob_matrix[:, -1])
        return prob_matrix, final_col_prob
