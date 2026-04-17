```python
class ProfileHMM:
    def __init__(self, length, alphabet="ACDEFGHIKLMNPQRSTVWY"):
        """Initialize pHMM with L match states and supporting I/D states."""
        self.L = length
        self.alphabet = alphabet
        self.states = self._build_states()
        self.emit_probs = {}      # {state: {residue: prob}}
        self.trans_probs = {}     # {state: {next_state: prob}}
        self.begin_probs = {}     # {state: prob}
```
**State Architecture**
* Fixed topology
* The state diagram has a left-to-right topology.
```
    def _build_states(self):
        """Create state topology: M0, M1..ML, I0..IL, D1..DL, End."""
        
        # Hard-code state creation and allowable transitions.
        states = ["Begin", "I0"]
        for i in range(1, self.L + 1):
            states += [f"M{i}", f"I{i}", f"D{i}"]
        
        # Generate topology from length parameter 
        states.append(f"End")
        return states
```
**Parameter Estimation from MSA**
* Instead of baum-welch on raw, unlabeled sequences, use pre-aligned MSA (labeled data) to estimate emission and transition probs
* Note: Since MSA is pre-aligned and labeled, each residue is a match, and if it is an insertion it will be lowercased
```
    def init_from_msa(self, msa, pseudocount=1e-100):
        """Initialize parameters from labeled multiple sequence alignment.
        
        Args:
            msa: list of aligned sequences (gaps = '-')
            pseudocount: small value to avoid zero probabilities
        """
        self._estimate_emissions_from_msa(msa, pseudocount)
        self._estimate_transitions_from_msa(msa, pseudocount)
```

**Emission Probabilities**
* Match Cases: Position-specific distributions (Count residues at each position for each sequence in msa)
* Insertion Cases: Compute global aa freq from all training sequences and use background distribution for all $I_i$ states
* Deletion Cases: No emission
* Pseudocounts are applied to avoid zeroes
```
    def _estimate_emissions_from_msa(self, msa, pseudocount):
        """Count residues at each position → emission probabilities."""
        for pos in range(1, self.L + 1):
            counts = {aa: pseudocount for aa in self.alphabet}
            for seq in msa:
                if seq[pos-1] != '-':
                    counts[seq[pos-1]] += 1
            total = sum(counts.values())
            self.emit_probs[f"M{pos}"] = {aa: counts[aa]/total 
                                           for aa in self.alphabet}

        bg_counts = {aa: pseudocount for aa in self.alphabet}
        for seq in msa:
            for aa in seq:
                if aa != '-':
                    bg_counts[aa] += 1
        total_bg = sum(bg_counts.values())
        bg_dist = {aa: bg_counts[aa]/total_bg for aa in self.alphabet}
        for i in range(self.L + 1):
            self.emit_probs[f"I{i}"] = bg_dist.copy()

        for i in range(1, self.L + 1):
            self.emit_probs[f"D{i}"] = {}  # Empty = silent
```

* Counts observed state transitions to get transition probabilities
* Applies pseudocounts to avoid zeroes

```
    def _can_transition(self, state, next_state):
        """Transition Rules"""
        if state == "Begin":
            return next_state in ["M1", "I0", "D1"]
         
        if state == "End":
            return False
        
        # Get the number for the state
        n = int(state[1:])
        
        if state.startswith("M"):
            return next_state in [f"M{n+1}", f"I{n}", f"D{n}"]
        if state.startswith("I"):
            return next_state in [f"I{n}", f"M{n+1}"]
        if state.startswith("D"):
            return next_state in [f"M{n+1}", f"I[n]", f"D{n+1}", "End"]
        
        return False    
```

```
    def _build_transition_skeleton(self):
        """Build the transition count skeleton"""
        transition_counts = {}
        for state in self.states:
            for next_state in self.states:
                if(_can_transition(state, next_state)):
                    transition_counts[(state, next_state)] = 0
        return transition_counts
```
```
    def _count_transitions_from_msa(self, msa):
        """Counts state transitions from alignment"""
          for i in range(0, self.+1, 2)
            for sequence in msa:
                if sequence[i] == '-':
                    state = f"D{i+1}
                
                
        

```
```
    def _estimate_transitions_from_msa(self, msa, pseudocount):
        """ Normalize transition counts to transition probabilities."""
        trans_counts = self._count_transitions_from_msa(msa) # This is not present in example
        
        # 
        for state in self.states:
            self.trans_probs[state] = {}
            
            outgoing = {s: trans_counts.get((state, s), 0) + pseudocount 
                       for s in self.states 
                       if (state, s) in trans_counts or self._can_transition(state, s)}
            if outgoing:
                total = sum(outgoing.values())
                for next_state, count in outgoing.items():
                    self.trans_probs[state][next_state] = count / total
```
    def forward(self, sequence):
        """Compute P(sequence | HMM) via forward algorithm."""
        n = len(sequence)
        F = [[{} for _ in range(len(self.states))] for _ in range(n + 1)]
        
        F[0]["Begin"] = 0.0  # log(1)
        
        for i in range(1, n + 1):
            for state in self.states:
                if state == "Begin":
                    continue
                incoming = sum(
                    F[i-1][prev_state] + log(self.trans_probs[prev_state][state])
                    for prev_state in self.states
                    if prev_state in self.trans_probs and state in self.trans_probs[prev_state]
                )
                if state.startswith('D'):
                    F[i][state] = incoming  # Silent: no emission
                else:
                    emit_logprob = log(self.emit_probs[state].get(sequence[i-1], 1e-100))
                    F[i][state] = incoming + emit_logprob
        
        total_logprob = sum(F[n][s] + log(self.trans_probs.get(s, {}).get("End", 1e-100))
                           for s in self.states if s != "Begin")
        return exp(total_logprob)

    def viterbi(self, sequence):
        """Find most probable hidden state path via Viterbi algorithm."""
        n = len(sequence)
        V = [[{} for _ in range(len(self.states))] for _ in range(n + 1)]
        
        V[0]["Begin"] = (0.0, None)
        
        for i in range(1, n + 1):
            for state in self.states:
                if state == "Begin":
                    continue
                best_logprob = -inf
                best_prev = None
                for prev_state in self.states:
                    if prev_state in V[i-1]:
                        prev_logprob, _ = V[i-1][prev_state]
                        trans_logprob = log(self.trans_probs[prev_state].get(state, 1e-100))
                        total = prev_logprob + trans_logprob
                        if total > best_logprob:
                            best_logprob = total
                            best_prev = prev_state
                
                if not state.startswith('D'):
                    emit_logprob = log(self.emit_probs[state].get(sequence[i-1], 1e-100))
                    best_logprob += emit_logprob
                
                V[i][state] = (best_logprob, best_prev)
        
        path = []
        best_state = max(V[n], key=lambda s: V[n][s][0] if V[n][s] else -inf)
        for i in range(n, 0, -1):
            path.append(best_state)
            _, prev_state = V[i][best_state]
            best_state = prev_state
        
        return list(reversed(path))

    def baum_welch(self, sequences, max_iterations=100, convergence_threshold=1e-6):
        """Train pHMM using EM algorithm on unlabeled sequences."""
        prev_loglik = -inf
        
        for iteration in range(max_iterations):
            posteriors = []
            for seq in sequences:
                forward = self._forward_table(seq)
                backward = self._backward_table(seq)
                posterior = self._compute_posterior(forward, backward)
                posteriors.append(posterior)
            
            self._reestimate_emissions(posteriors, sequences)
            self._reestimate_transitions(posteriors, sequences)
            
            loglik = sum(self._log_likelihood(seq) for seq in sequences)
            if abs(loglik - prev_loglik) < convergence_threshold:
                return True
            prev_loglik = loglik
        
        return False

    def _forward_table(self, sequence):
        """Compute full forward table for later use."""
        pass

    def _backward_table(self, sequence):
        """Compute full backward table for later use."""
        pass

    def _compute_posterior(self, forward, backward):
        """Compute gamma (state posteriors) from forward-backward."""
        pass

    def _reestimate_emissions(self, posteriors, sequences):
        """Update emission probabilities based on expected counts."""
        pass

    def _reestimate_transitions(self, posteriors, sequences):
        """Update transition probabilities based on expected counts."""
        pass
    


```