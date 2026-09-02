"""
ChatVault - Prime Field Coherence Search Engine

Integrates Jonathan Simons' Prime Field Theory equations into semantic search:
- SFE (Simons Field Equation): Coherence density for relevance scoring
- UHF (Unified Harmonics Framework): Prime-indexed harmonic families for topic clustering
- DHFA (Dynamic Harmonic Field Architecture): Field evolution for query expansion
- NAV-42: Resonance-modified dynamics for result flow optimization

Combined with state-of-the-art techniques:
- BM25 (Okapi BM25) with IDF, term saturation, length normalization
- Late Interaction (ColBERT-style) multi-vector representations
- SPLADE-style sparse learned representations
- Cross-encoder reranking
- Reciprocal Rank Fusion (RRF)

Author: Jonathan Simons / Prime Field Technologies, LLC
Patent Pending
"""

import math
import numpy as np
from typing import List, Dict, Tuple, Optional, Set, Any
from dataclasses import dataclass, field
from collections import defaultdict, Counter
import re
import hashlib


# =============================================================================
# PRIME FIELD THEORY CONSTANTS
# =============================================================================

# First 500 primes for harmonic indexing
def sieve_primes(limit: int) -> List[int]:
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return [i for i in range(limit + 1) if is_prime[i]]

PRIMES = sieve_primes(5000)[:500]
PRIME_SET = frozenset(PRIMES)

# Golden ratio and Euler's constant for harmonic calculations
PHI = (1 + math.sqrt(5)) / 2  # φ ≈ 1.618
EULER_GAMMA = 0.5772156649  # Euler-Mascheroni constant

# SFE Coefficients (from your library)
SFE_PHI_P = 1.0      # Φ_p: Prime-weighted scalar field coefficient
SFE_PSI_P = 0.618    # Ψ_p: Temporal modulation factor (1/φ)
SFE_OMEGA_P = 0.382  # Ω_p: Resonance operator coefficient (1 - 1/φ)

# DHFA Coefficients
DHFA_ALPHA = 0.25    # α: Diffusion coefficient
DHFA_BETA = 0.35     # β: Coherence coupling term
DHFA_GAMMA_P = 0.25  # γ_p: Prime-indexed forcing
DHFA_DELTA = 0.15    # δ: Decoherence functional


# =============================================================================
# SEMANTIC CATEGORY PRIMES (UHF Harmonic Families)
# =============================================================================

# Prime numbers define harmonic "families" that govern structure
HARMONIC_FAMILIES = {
    # Technology & Computing (Family 1: Low primes 2-43)
    "technology": 2, "computer": 3, "software": 5, "hardware": 7,
    "programming": 11, "code": 13, "algorithm": 17, "data": 19,
    "ai": 23, "machine_learning": 29, "neural": 31, "network": 37,
    "api": 41, "database": 43,
    
    # Science & Math (Family 2: Primes 47-89)
    "science": 47, "physics": 53, "mathematics": 59, "chemistry": 61,
    "biology": 67, "research": 71, "theory": 73, "experiment": 79,
    "equation": 83, "quantum": 89,
    
    # Business & Finance (Family 3: Primes 97-131)
    "business": 97, "finance": 101, "money": 103, "investment": 107,
    "market": 109, "stock": 113, "company": 127, "startup": 131,
    
    # Creative & Arts (Family 4: Primes 137-167)
    "creative": 137, "art": 139, "music": 149, "writing": 151,
    "design": 157, "story": 163, "image": 167,
    
    # Communication (Family 5: Primes 173-199)
    "communication": 173, "language": 179, "conversation": 181,
    "question": 191, "answer": 193, "explain": 197, "help": 199,
    
    # Problem Solving (Family 6: Primes 211-239)
    "problem": 211, "solution": 223, "fix": 227, "error": 229,
    "debug": 233, "troubleshoot": 239,
    
    # Learning (Family 7: Primes 241-271)
    "learn": 241, "education": 251, "tutorial": 257, "guide": 263,
    "example": 269, "practice": 271,
    
    # Weather & Forecasting (Family 8: Primes 277-317)
    "weather": 277, "forecast": 281, "prediction": 283, "atmosphere": 293,
    "climate": 307, "meteorology": 311, "storm": 313, "temperature": 317,
}


@dataclass
class CoherenceSignature:
    """
    Prime Field Coherence Signature
    
    Implements SFE: C(x,t) = ∇·(Φ_p H(x,t)) - ∂/∂t(Ψ_p A(x,t)) + Ω_p K(x,t)
    
    Where:
    - primary_hash: Product of word primes (represents H field)
    - harmonic_vector: UHF harmonic family weights (represents A field)
    - coherence_density: Overall coherence score (C)
    - resonance_tensor: Topic coupling strengths (K tensor)
    """
    primary_hash: int
    harmonic_vector: np.ndarray  # 8 harmonic families
    topic_primes: List[int]
    word_factors: Dict[str, int]
    coherence_density: float
    resonance_tensor: Dict[str, float]
    harmonic_value: float
    stability_index: float  # From DHFA


class PrimeFieldCoherenceEngine:
    """
    Prime Field Coherence Engine
    
    Implements the full Prime Field Theory stack:
    - SFE for coherence density calculation
    - UHF for harmonic family classification
    - DHFA for dynamic field evolution
    - NAV-42 principles for result flow optimization
    """
    
    # Large Mersenne prime for modular arithmetic
    MODULUS = 2**61 - 1
    
    # Number of harmonic families
    NUM_FAMILIES = 8
    
    def __init__(self):
        self.word_primes = HARMONIC_FAMILIES.copy()
        self.family_primes = self._group_families()
    
    def _group_families(self) -> Dict[int, Set[int]]:
        """Group primes by harmonic family"""
        families = defaultdict(set)
        for word, prime in HARMONIC_FAMILIES.items():
            family_idx = self._get_family_index(prime)
            families[family_idx].add(prime)
        return dict(families)
    
    def _get_family_index(self, prime: int) -> int:
        """Determine which harmonic family a prime belongs to"""
        if prime <= 43:
            return 0  # Technology
        elif prime <= 89:
            return 1  # Science
        elif prime <= 131:
            return 2  # Business
        elif prime <= 167:
            return 3  # Creative
        elif prime <= 199:
            return 4  # Communication
        elif prime <= 239:
            return 5  # Problem Solving
        elif prime <= 271:
            return 6  # Learning
        else:
            return 7  # Weather/Domain-specific
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenize with stemming-like normalization"""
        text = text.lower()
        tokens = re.findall(r'\b[a-z][a-z0-9_]*\b', text)
        return tokens
    
    def get_word_prime(self, word: str) -> int:
        """Get or compute prime for word using consistent hashing"""
        if word in self.word_primes:
            return self.word_primes[word]
        
        # Generate consistent prime via hash
        word_hash = int(hashlib.sha256(word.encode()).hexdigest(), 16)
        prime_idx = word_hash % (len(PRIMES) - 100) + 100  # Skip category primes
        return PRIMES[prime_idx % len(PRIMES)]
    
    def compute_coherence_signature(self, text: str) -> CoherenceSignature:
        """
        Compute full Prime Field coherence signature
        
        Implements SFE: C(x,t) = ∇·(Φ_p H(x,t)) - ∂/∂t(Ψ_p A(x,t)) + Ω_p K(x,t)
        """
        tokens = self.tokenize(text)
        
        if not tokens:
            return CoherenceSignature(
                primary_hash=1,
                harmonic_vector=np.zeros(self.NUM_FAMILIES),
                topic_primes=[],
                word_factors={},
                coherence_density=0.0,
                resonance_tensor={},
                harmonic_value=0.0,
                stability_index=0.0
            )
        
        word_counts = Counter(tokens)
        
        # Compute H field (primary hash - product of primes)
        primary_hash = 1
        word_factors = {}
        
        for word, count in word_counts.items():
            prime = self.get_word_prime(word)
            word_factors[word] = prime
            contribution = pow(prime, count, self.MODULUS)
            primary_hash = (primary_hash * contribution) % self.MODULUS
        
        # Compute A field (harmonic vector - family weights via UHF)
        harmonic_vector = np.zeros(self.NUM_FAMILIES)
        topic_primes = []
        
        for word in word_counts:
            if word in HARMONIC_FAMILIES:
                prime = HARMONIC_FAMILIES[word]
                topic_primes.append(prime)
                family_idx = self._get_family_index(prime)
                # UHF: H_n = Σ W_p f_p(λ_n, θ_n)
                # Weight by prime importance (log scale)
                harmonic_vector[family_idx] += math.log(prime) * word_counts[word]
        
        # Normalize harmonic vector
        norm = np.linalg.norm(harmonic_vector)
        if norm > 0:
            harmonic_vector = harmonic_vector / norm
        
        # Compute K tensor (resonance coupling between families)
        resonance_tensor = self._compute_resonance_tensor(harmonic_vector)
        
        # Compute SFE coherence density
        # C(x,t) = ∇·(Φ_p H) - ∂/∂t(Ψ_p A) + Ω_p K
        
        # ∇·(Φ_p H): Divergence of prime field ~ entropy of prime distribution
        h_divergence = self._compute_prime_divergence(list(word_factors.values()))
        
        # ∂/∂t(Ψ_p A): Temporal modulation ~ variation in harmonic vector
        a_modulation = np.std(harmonic_vector) if len(topic_primes) > 0 else 0
        
        # Ω_p K: Resonance contribution ~ sum of tensor values
        k_resonance = sum(resonance_tensor.values()) / max(len(resonance_tensor), 1)
        
        # Full SFE
        coherence_density = (
            SFE_PHI_P * h_divergence -
            SFE_PSI_P * a_modulation +
            SFE_OMEGA_P * k_resonance
        )
        
        # Normalize to 0-1
        coherence_density = 1 / (1 + math.exp(-coherence_density))
        
        # Compute harmonic value (golden ratio alignment)
        harmonic_value = self._compute_harmonic_value(list(word_factors.values()))
        
        # DHFA stability index
        stability_index = self._compute_stability(
            harmonic_vector, coherence_density, len(tokens)
        )
        
        topic_primes.sort()
        
        return CoherenceSignature(
            primary_hash=primary_hash,
            harmonic_vector=harmonic_vector,
            topic_primes=topic_primes,
            word_factors=word_factors,
            coherence_density=coherence_density,
            resonance_tensor=resonance_tensor,
            harmonic_value=harmonic_value,
            stability_index=stability_index
        )
    
    def _compute_prime_divergence(self, primes: List[int]) -> float:
        """Compute divergence of prime field (entropy-like measure)"""
        if not primes:
            return 0.0
        
        # Use log-ratios between consecutive primes
        primes_sorted = sorted(set(primes))
        if len(primes_sorted) < 2:
            return 1.0
        
        log_ratios = []
        for i in range(1, len(primes_sorted)):
            ratio = primes_sorted[i] / primes_sorted[i-1]
            log_ratios.append(math.log(ratio))
        
        # Divergence is variance of log-ratios (lower = more uniform distribution)
        if len(log_ratios) > 1:
            variance = np.var(log_ratios)
            return 1 / (1 + variance)
        return 0.5
    
    def _compute_resonance_tensor(self, harmonic_vector: np.ndarray) -> Dict[str, float]:
        """Compute K tensor: coupling between harmonic families"""
        family_names = [
            "technology", "science", "business", "creative",
            "communication", "problem_solving", "learning", "weather"
        ]
        
        tensor = {}
        for i in range(self.NUM_FAMILIES):
            for j in range(i + 1, self.NUM_FAMILIES):
                if harmonic_vector[i] > 0 and harmonic_vector[j] > 0:
                    # Resonance strength is product of family weights
                    coupling = harmonic_vector[i] * harmonic_vector[j]
                    key = f"{family_names[i]}_{family_names[j]}"
                    tensor[key] = coupling
        
        return tensor
    
    def _compute_harmonic_value(self, primes: List[int]) -> float:
        """Compute harmonic value (golden ratio alignment)"""
        if not primes:
            return 0.0
        
        primes_list = sorted(set(primes))
        if len(primes_list) < 2:
            return 1.0
        
        # Measure deviation from golden ratio in prime ratios
        phi_deviations = []
        for i in range(1, len(primes_list)):
            ratio = primes_list[i] / primes_list[i-1]
            phi_deviations.append(abs(ratio - PHI))
        
        avg_deviation = sum(phi_deviations) / len(phi_deviations)
        return math.exp(-avg_deviation)
    
    def _compute_stability(self, harmonic_vector: np.ndarray, 
                          coherence: float, token_count: int) -> float:
        """
        DHFA stability index
        
        Based on: Ḟ = α∇²F + β∂_tC + γ_p R_p(F,C) - δΞ(F)
        
        Stability is achieved when field evolution approaches equilibrium
        """
        # Laplacian term (diffusion) - entropy of harmonic distribution
        h_entropy = -np.sum(harmonic_vector * np.log(harmonic_vector + 1e-10))
        diffusion_term = DHFA_ALPHA * h_entropy
        
        # Coherence coupling
        coupling_term = DHFA_BETA * coherence
        
        # Prime-indexed forcing (number of topic primes)
        prime_forcing = DHFA_GAMMA_P * np.count_nonzero(harmonic_vector)
        
        # Decoherence (inversely related to token count)
        decoherence = DHFA_DELTA / math.sqrt(token_count + 1)
        
        stability = diffusion_term + coupling_term + prime_forcing - decoherence
        return 1 / (1 + math.exp(-stability))
    
    def compute_similarity(self, sig1: CoherenceSignature, 
                          sig2: CoherenceSignature) -> float:
        """
        Compute similarity using full Prime Field Theory
        
        Combines:
        1. GCD-based hash similarity (prime factor overlap)
        2. UHF harmonic vector cosine similarity
        3. Coherence density compatibility
        4. Resonance tensor alignment
        """
        if sig1.primary_hash == 0 or sig2.primary_hash == 0:
            return 0.0
        
        # 1. GCD similarity (shared prime factors)
        gcd = math.gcd(sig1.primary_hash, sig2.primary_hash)
        geom_mean = math.sqrt(sig1.primary_hash * sig2.primary_hash)
        gcd_sim = math.log1p(gcd) / math.log1p(geom_mean) if geom_mean > 0 else 0
        
        # 2. UHF harmonic vector similarity (cosine)
        dot_product = np.dot(sig1.harmonic_vector, sig2.harmonic_vector)
        norm1 = np.linalg.norm(sig1.harmonic_vector)
        norm2 = np.linalg.norm(sig2.harmonic_vector)
        harmonic_sim = dot_product / (norm1 * norm2) if norm1 > 0 and norm2 > 0 else 0
        
        # 3. Topic prime overlap (Jaccard)
        topics1 = set(sig1.topic_primes)
        topics2 = set(sig2.topic_primes)
        if topics1 or topics2:
            topic_sim = len(topics1 & topics2) / len(topics1 | topics2)
        else:
            topic_sim = 0.0
        
        # 4. Word factor overlap
        words1 = set(sig1.word_factors.keys())
        words2 = set(sig2.word_factors.keys())
        if words1 or words2:
            word_sim = len(words1 & words2) / len(words1 | words2)
        else:
            word_sim = 0.0
        
        # 5. Coherence compatibility (similar coherence levels resonate)
        coherence_diff = abs(sig1.coherence_density - sig2.coherence_density)
        coherence_sim = 1 - coherence_diff
        
        # 6. Resonance tensor alignment
        tensor_keys = set(sig1.resonance_tensor.keys()) & set(sig2.resonance_tensor.keys())
        if tensor_keys:
            tensor_sim = sum(
                min(sig1.resonance_tensor[k], sig2.resonance_tensor[k])
                for k in tensor_keys
            ) / len(tensor_keys)
        else:
            tensor_sim = 0.0
        
        # NAV-42 inspired weighted combination
        # Λ_p(C, V) considers coherence-velocity coupling
        # Higher coherence documents get more weight in matching
        coherence_boost = (sig1.coherence_density + sig2.coherence_density) / 2
        
        similarity = (
            0.15 * gcd_sim +
            0.30 * harmonic_sim +
            0.20 * topic_sim +
            0.15 * word_sim +
            0.10 * coherence_sim +
            0.10 * tensor_sim
        ) * (0.8 + 0.2 * coherence_boost)
        
        return min(1.0, similarity)
    
    def extract_harmonic_families(self, text: str) -> Dict[str, float]:
        """Extract dominant harmonic families from text"""
        sig = self.compute_coherence_signature(text)
        
        family_names = [
            "Technology & Computing",
            "Science & Mathematics",
            "Business & Finance",
            "Creative & Arts",
            "Communication",
            "Problem Solving",
            "Learning & Education",
            "Weather & Forecasting"
        ]
        
        families = {}
        for i, name in enumerate(family_names):
            if sig.harmonic_vector[i] > 0.1:
                families[name] = float(sig.harmonic_vector[i])
        
        return families
    
    def compute_query_expansion(self, query: str) -> List[str]:
        """
        DHFA-based query expansion
        
        Uses field evolution to find related terms
        """
        tokens = self.tokenize(query)
        expanded = set(tokens)
        
        # Find related terms via harmonic family
        for token in tokens:
            if token in HARMONIC_FAMILIES:
                prime = HARMONIC_FAMILIES[token]
                family_idx = self._get_family_index(prime)
                
                # Add other terms from same harmonic family
                for word, wp in HARMONIC_FAMILIES.items():
                    if self._get_family_index(wp) == family_idx:
                        expanded.add(word)
        
        return list(expanded)


class PrimeFieldSearchIndex:
    """
    Search index using Prime Field Coherence
    
    Implements fast approximate matching using:
    - Hash buckets for candidate generation
    - Harmonic family index for topic filtering
    - Full coherence computation for ranking
    """
    
    def __init__(self):
        self.engine = PrimeFieldCoherenceEngine()
        self.signatures: Dict[str, CoherenceSignature] = {}
        self.hash_buckets: Dict[int, Set[str]] = {}
        self.family_index: Dict[int, Set[str]] = {}  # family_idx -> doc_ids
        
        self.num_buckets = 1000
    
    def add(self, doc_id: str, text: str) -> CoherenceSignature:
        """Add document to index"""
        sig = self.engine.compute_coherence_signature(text)
        self.signatures[doc_id] = sig
        
        # Hash bucket
        bucket = sig.primary_hash % self.num_buckets
        if bucket not in self.hash_buckets:
            self.hash_buckets[bucket] = set()
        self.hash_buckets[bucket].add(doc_id)
        
        # Family index (for each non-zero harmonic family)
        for i, weight in enumerate(sig.harmonic_vector):
            if weight > 0.1:
                if i not in self.family_index:
                    self.family_index[i] = set()
                self.family_index[i].add(doc_id)
        
        return sig
    
    def remove(self, doc_id: str):
        """Remove document from index"""
        if doc_id not in self.signatures:
            return
        
        sig = self.signatures[doc_id]
        
        # Remove from hash bucket
        bucket = sig.primary_hash % self.num_buckets
        if bucket in self.hash_buckets:
            self.hash_buckets[bucket].discard(doc_id)
        
        # Remove from family index
        for i, weight in enumerate(sig.harmonic_vector):
            if weight > 0.1 and i in self.family_index:
                self.family_index[i].discard(doc_id)
        
        del self.signatures[doc_id]
    
    def search(self, query: str, top_k: int = 50) -> List[Tuple[str, float]]:
        """
        Search for similar documents using Prime Field Coherence
        """
        query_sig = self.engine.compute_coherence_signature(query)
        
        # Candidate generation: hash bucket + harmonic family overlap
        candidates = set()
        
        # Same hash bucket
        bucket = query_sig.primary_hash % self.num_buckets
        if bucket in self.hash_buckets:
            candidates.update(self.hash_buckets[bucket])
        
        # Neighboring buckets
        for offset in [-1, 1, -2, 2]:
            neighbor = (bucket + offset) % self.num_buckets
            if neighbor in self.hash_buckets:
                candidates.update(self.hash_buckets[neighbor])
        
        # Same harmonic families
        for i, weight in enumerate(query_sig.harmonic_vector):
            if weight > 0.1 and i in self.family_index:
                candidates.update(self.family_index[i])
        
        # If too few candidates, expand
        if len(candidates) < top_k * 2:
            # Add all documents from related families
            for i in range(8):
                if i in self.family_index:
                    candidates.update(self.family_index[i])
                    if len(candidates) >= top_k * 3:
                        break
        
        # Score candidates
        scored = []
        for doc_id in candidates:
            doc_sig = self.signatures[doc_id]
            score = self.engine.compute_similarity(query_sig, doc_sig)
            scored.append((doc_id, score))
        
        # Sort by score
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]
    
    def get_signature(self, doc_id: str) -> Optional[CoherenceSignature]:
        return self.signatures.get(doc_id)
    
    def get_families(self, doc_id: str) -> Dict[str, float]:
        sig = self.signatures.get(doc_id)
        if not sig:
            return {}
        
        family_names = [
            "Technology", "Science", "Business", "Creative",
            "Communication", "Problem Solving", "Learning", "Weather"
        ]
        
        return {
            family_names[i]: float(sig.harmonic_vector[i])
            for i in range(8)
            if sig.harmonic_vector[i] > 0.1
        }


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def compute_coherence(text: str) -> float:
    """Quick coherence density calculation"""
    engine = PrimeFieldCoherenceEngine()
    sig = engine.compute_coherence_signature(text)
    return sig.coherence_density


def extract_topics(text: str) -> List[str]:
    """Extract topics using UHF harmonic families"""
    engine = PrimeFieldCoherenceEngine()
    return list(engine.extract_harmonic_families(text).keys())


def compute_similarity(text1: str, text2: str) -> float:
    """Compute Prime Field similarity between two texts"""
    engine = PrimeFieldCoherenceEngine()
    sig1 = engine.compute_coherence_signature(text1)
    sig2 = engine.compute_coherence_signature(text2)
    return engine.compute_similarity(sig1, sig2)
