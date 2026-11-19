import { MCQQuestion, CodingChallenge, InterviewQuestion } from '../types';

export const BENCHMARK_20_MCQS: MCQQuestion[] = [
  {
    id: "mcq_1",
    question: "What is the average-case time complexity of lookup, insertion, and deletion operations in a well-distributed Hash Table?",
    code_snippet: undefined,
    options: [
      { id: "A", text: "O(1)" },
      { id: "B", text: "O(log N)" },
      { id: "C", text: "O(N)" },
      { id: "D", text: "O(N log N)" }
    ],
    correct_option_id: "A",
    explanation: "A Hash Table provides amortized O(1) constant time complexity for insert, search, and delete operations when using an effective hash function with minimal collisions."
  },
  {
    id: "mcq_2",
    question: "In Python, what is the output of calling add_item(1) followed by add_item(2)?",
    code_snippet: "def add_item(val, lst=[]):\n    lst.append(val)\n    return lst\n\nprint(add_item(1))\nprint(add_item(2))",
    options: [
      { id: "A", text: "[1] and [2]" },
      { id: "B", text: "[1] and [1, 2]" },
      { id: "C", text: "[1] and [2, 1]" },
      { id: "D", text: "TypeError: mutable default argument" }
    ],
    correct_option_id: "B",
    explanation: "Default parameter values in Python are evaluated once when the function is defined, not each time the function is called. Hence, mutable default arguments like lists persist across function calls."
  },
  {
    id: "mcq_3",
    question: "Which of the following correctly describes the logical order of execution of SQL clauses?",
    code_snippet: undefined,
    options: [
      { id: "A", text: "SELECT -> FROM -> WHERE -> GROUP BY -> HAVING -> ORDER BY" },
      { id: "B", text: "FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY" },
      { id: "C", text: "FROM -> SELECT -> WHERE -> GROUP BY -> ORDER BY -> HAVING" },
      { id: "D", text: "WHERE -> FROM -> GROUP BY -> HAVING -> SELECT -> ORDER BY" }
    ],
    correct_option_id: "B",
    explanation: "SQL query execution begins at the data source (FROM/JOIN), filters rows (WHERE), groups them (GROUP BY), filters groups (HAVING), evaluates expressions (SELECT), and finally sorts (ORDER BY)."
  },
  {
    id: "mcq_4",
    question: "In RESTful API design, which HTTP method is required to be strictly idempotent according to RFC 7231?",
    code_snippet: undefined,
    options: [
      { id: "A", text: "POST" },
      { id: "B", text: "PATCH" },
      { id: "C", text: "PUT" },
      { id: "D", text: "CONNECT" }
    ],
    correct_option_id: "C",
    explanation: "PUT replaces the target resource entirely; repeating the same PUT request multiple times leaves the system in the identical state, satisfying the definition of idempotence."
  },
  {
    id: "mcq_5",
    question: "In relational database design, what does Third Normal Form (3NF) strictly require beyond 2NF?",
    code_snippet: undefined,
    options: [
      { id: "A", text: "All attributes must be atomic and non-repeating." },
      { id: "B", text: "Every non-key attribute must depend directly on the entire primary key, not a subset." },
      { id: "C", text: "There must be no transitive dependency for non-prime attributes on candidate keys." },
      { id: "D", text: "All foreign keys must have cascading deletion rules." }
    ],
    correct_option_id: "C",
    explanation: "3NF requires a relation to be in 2NF and have no transitive functional dependencies of non-prime attributes on any candidate key ('Every non-key attribute must provide a fact about the key, the whole key, and nothing but the key')."
  },
  {
    id: "mcq_6",
    question: "What is the worst-case time complexity of QuickSort when an unbalanced pivot (e.g., largest/smallest element) is selected at every partition step?",
    code_snippet: undefined,
    options: [
      { id: "A", text: "O(N log N)" },
      { id: "B", text: "O(N^2)" },
      { id: "C", text: "O(log N)" },
      { id: "D", text: "O(2^N)" }
    ],
    correct_option_id: "B",
    explanation: "If the pivot consistently splits an array of size N into 0 and N-1 elements, the recursion tree height degrades from log N to N, yielding O(N^2) total comparisons."
  },
  {
    id: "mcq_7",
    question: "In Git, what is the core behavioral difference between 'git merge' and 'git rebase'?",
    code_snippet: undefined,
    options: [
      { id: "A", text: "git merge deletes commit history; git rebase preserves it." },
      { id: "B", text: "git merge creates a 3-way merge commit; git rebase reapplies commits onto a new base commit linearly." },
      { id: "C", text: "git rebase can only be used on the remote origin branch." },
      { id: "D", text: "git merge converts all commits into a single squash commit." }
    ],
    correct_option_id: "B",
    explanation: "Merge preserves the exact historical timeline and creates a merge commit. Rebase moves or reapplies your commits atop the target tip, producing a clean linear history."
  },
  {
    id: "mcq_8",
    question: "What does the following JavaScript asynchronous code print to the console?",
    code_snippet: "console.log('1');\nsetTimeout(() => console.log('2'), 0);\nPromise.resolve().then(() => console.log('3'));\nconsole.log('4');",
    options: [
      { id: "A", text: "1, 2, 3, 4" },
      { id: "B", text: "1, 4, 2, 3" },
      { id: "C", text: "1, 4, 3, 2" },
      { id: "D", text: "1, 3, 4, 2" }
    ],
    correct_option_id: "C",
    explanation: "Synchronous code runs first (1, 4), then microtasks in the Promise queue are drained (3), and finally macrotasks like setTimeout run (2)."
  },
  {
    id: "mcq_9",
    question: "Which ACID property ensures that transactions execute concurrently without seeing intermediate, uncommitted states of other transactions?",
    code_snippet: undefined,
    options: [
      { id: "A", text: "Atomicity" },
      { id: "B", text: "Consistency" },
      { id: "C", text: "Isolation" },
      { id: "D", text: "Durability" }
    ],
    correct_option_id: "C",
    explanation: "Isolation determines how transaction integrity is visible to other concurrent users, preventing dirty reads and non-repeatable reads."
  },
  {
    id: "mcq_10",
    question: "In Redis, what is the default eviction behavior when maxmemory is reached and 'allkeys-lru' policy is set?",
    code_snippet: undefined,
    options: [
      { id: "A", text: "Throws an out-of-memory error on every write." },
      { id: "B", text: "Evicts the least recently used keys among all keys." },
      { id: "C", text: "Evicts keys with an explicit TTL expiration set only." },
      { id: "D", text: "Evicts keys randomly." }
    ],
    correct_option_id: "B",
    explanation: "The 'allkeys-lru' policy evicts the least recently used (LRU) keys across the entire keyspace regardless of whether a TTL expiration was configured."
  },
  {
    id: "mcq_11",
    question: "Which tree traversal algorithm yields keys in strictly non-decreasing ascending order for any valid Binary Search Tree (BST)?",
    code_snippet: undefined,
    options: [
      { id: "A", text: "Pre-order traversal (Root, Left, Right)" },
      { id: "B", text: "In-order traversal (Left, Root, Right)" },
      { id: "C", text: "Post-order traversal (Left, Right, Root)" },
      { id: "D", text: "Level-order traversal (BFS)" }
    ],
    correct_option_id: "B",
    explanation: "In a BST, all left descendants are smaller than the root, and all right descendants are larger. Traversing Left -> Root -> Right (In-order) visits nodes in sorted ascending sequence."
  },
  {
    id: "mcq_12",
    question: "What is the auxiliary space complexity of a recursive Depth-First Search (DFS) on a tree of height H?",
    code_snippet: undefined,
    options: [
      { id: "A", text: "O(1)" },
      { id: "B", text: "O(H)" },
      { id: "C", text: "O(N^2)" },
      { id: "D", text: "O(2^H)" }
    ],
    correct_option_id: "B",
    explanation: "Recursive DFS creates stack frames corresponding to the current traversal path from root to leaf, which is bounded by the height of the tree H."
  },
  {
    id: "mcq_13",
    question: "What is the semantic distinction between HTTP status code 401 Unauthorized and 403 Forbidden?",
    code_snippet: undefined,
    options: [
      { id: "A", text: "401 indicates server failure; 403 indicates invalid query parameters." },
      { id: "B", text: "401 indicates missing or invalid authentication credentials; 403 indicates authentication was recognized but authorization to access the resource is denied." },
      { id: "C", text: "401 is for GET requests; 403 is for POST and PUT requests." },
      { id: "D", text: "There is no difference; they are interchangeable in RFC 7231." }
    ],
    correct_option_id: "B",
    explanation: "401 signifies unauthenticated (client must authenticate first). 403 signifies forbidden (server understands who you are, but you do not possess permission for this operation)."
  },
  {
    id: "mcq_14",
    question: "Why are B+ Trees overwhelmingly preferred over B Trees for disk-based relational database indexes (like PostgreSQL and MySQL InnoDB)?",
    code_snippet: undefined,
    options: [
      { id: "A", text: "B+ Trees require zero memory locks during write operations." },
      { id: "B", text: "Leaves are linked sequentially for fast range scans and internal nodes store only keys maximizing fanout." },
      { id: "C", text: "B Trees do not support binary searching." },
      { id: "D", text: "B+ Trees have an average lookup time of O(1)." }
    ],
    correct_option_id: "B",
    explanation: "In B+ Trees, non-leaf nodes store only index keys (maximizing fanout per disk page), and all leaf nodes form a contiguous doubly-linked list enabling rapid sequential range scans."
  },
  {
    id: "mcq_15",
    question: "In distributed microservices, how does the Circuit Breaker pattern behave in the 'Half-Open' state?",
    code_snippet: undefined,
    options: [
      { id: "A", text: "All incoming requests are immediately dropped and routed to dead-letter queue." },
      { id: "B", text: "It permits a limited number of test requests through to evaluate whether the downstream service has recovered." },
      { id: "C", text: "It runs a full database backup before resuming operations." },
      { id: "D", text: "It duplicates all traffic across two independent data centers." }
    ],
    correct_option_id: "B",
    explanation: "After an open circuit timeout expires, the breaker transitions to Half-Open to allow a trial burst of requests. If they succeed, it closes the circuit; if they fail, it trips back to Open."
  },
  {
    id: "mcq_16",
    question: "According to the CAP Theorem, what fundamental trade-off must a distributed data store make during an unavoidable network partition (P)?",
    code_snippet: undefined,
    options: [
      { id: "A", text: "Between Performance and Security." },
      { id: "B", text: "Between Consistency (all nodes see latest data) and Availability (every request receives a non-error response)." },
      { id: "C", text: "Between Latency and Storage throughput." },
      { id: "D", text: "Between Compression ratio and Encryption depth." }
    ],
    correct_option_id: "B",
    explanation: "When a partition occurs, a distributed system must either reject writes to guarantee consistency across unreachable nodes (CP) or accept writes on available partitions at the expense of stale reads (AP)."
  },
  {
    id: "mcq_17",
    question: "What is an architectural security trade-off when using stateless JWT authentication compared to server-side session stores?",
    code_snippet: undefined,
    options: [
      { id: "A", text: "JWTs cannot be validated without continuous database roundtrips." },
      { id: "B", text: "JWTs cannot be revoked instantly prior to expiration without maintaining a distributed token revocation blacklist." },
      { id: "C", text: "JWTs can only be sent over unencrypted HTTP connections." },
      { id: "D", text: "JWTs do not support digital signatures." }
    ],
    correct_option_id: "B",
    explanation: "Because JWTs are self-contained and cryptographically verified statelessly, revoking a compromised token before its expiration requires introducing a centralized revocation list or Redis blacklist."
  },
  {
    id: "mcq_18",
    question: "What is the primary difference between dynamic programming Memoization (top-down) and Tabulation (bottom-up)?",
    code_snippet: undefined,
    options: [
      { id: "A", text: "Memoization avoids all recursion; Tabulation always uses recursion." },
      { id: "B", text: "Tabulation iteratively computes and fills a table from base cases up, eliminating recursive call stack overhead." },
      { id: "C", text: "Tabulation requires exponential memory space." },
      { id: "D", text: "Memoization is always O(1) time complexity." }
    ],
    correct_option_id: "B",
    explanation: "Memoization maintains recursion and caches results in a hash table or array. Tabulation avoids recursion stack overhead by filling subproblems systematically from base cases up."
  },
  {
    id: "mcq_19",
    question: "In Docker, why is multi-stage building considered an industry best practice for production images?",
    code_snippet: undefined,
    options: [
      { id: "A", text: "It forces containers to run in rootless mode by default." },
      { id: "B", text: "It separates build-time dependencies (compilers, SDKs) from runtime artifacts, producing minimal, secure production containers." },
      { id: "C", text: "It merges all Docker layers into a single uncompressed tarball." },
      { id: "D", text: "It eliminates the need for container port forwarding." }
    ],
    correct_option_id: "B",
    explanation: "Multi-stage builds leave heavyweight compilers and dev tools behind in temporary build stages, copying only the compiled executable or static assets into a slim final runtime base (like Alpine or distroless)."
  },
  {
    id: "mcq_20",
    question: "What is the time complexity of building a Binary Heap from an unordered array of N elements using the bottom-up 'heapify' algorithm?",
    code_snippet: undefined,
    options: [
      { id: "A", text: "O(N log N)" },
      { id: "B", text: "O(N)" },
      { id: "C", text: "O(N^2)" },
      { id: "D", text: "O(1)" }
    ],
    correct_option_id: "B",
    explanation: "Although inserting N elements one-by-one takes O(N log N), bottom-up heap construction (sifting down from the lowest parent nodes) mathematically converges to linear O(N) time."
  }
];

export const BENCHMARK_2_CHALLENGES: CodingChallenge[] = [
  {
    id: "code_01",
    title: "Two Sum (Sorted Array) - Two Pointer Scan",
    difficulty: "Medium",
    language: "python",
    problem_statement: "Given a 1-indexed sorted array of integers numbers and a target sum, find two distinct indices [i, j] such that numbers[i] + numbers[j] == target. Implement an optimal O(N) time and O(1) auxiliary space solution.",
    starter_code: "def two_sum_sorted(numbers: list[int], target: int) -> list[int]:\n    # Implement optimal two pointer scan\n    left = 0\n    right = len(numbers) - 1\n    while left < right:\n        current_sum = numbers[left] + numbers[right]\n        if current_sum == target:\n            return [left + 1, right + 1]\n        elif current_sum < target:\n            left += 1\n        else:\n            right -= 1\n    return []\n",
    sample_input: "numbers = [2, 7, 11, 15], target = 9",
    sample_output: "[1, 2]",
    test_cases: [
      { input: "[2, 7, 11, 15], target = 9", expected: "[1, 2]" },
      { input: "[2, 3, 4], target = 6", expected: "[1, 3]" }
    ]
  },
  {
    id: "code_02",
    title: "Valid Parentheses - Stack Balance Validator",
    difficulty: "Easy",
    language: "python",
    problem_statement: "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid. An input string is valid if open brackets are closed by the same type of brackets in the correct order. Implement in O(N) time and O(N) space using a Stack.",
    starter_code: "def is_valid_parentheses(s: str) -> bool:\n    # Implement stack validator\n    stack = []\n    mapping = {')': '(', '}': '{', ']': '['}\n    for char in s:\n        if char in mapping:\n            top_elem = stack.pop() if stack else '#'\n            if mapping[char] != top_elem:\n                return False\n        else:\n            stack.append(char)\n    return not stack\n",
    sample_input: "s = '()[]{}'",
    sample_output: "True",
    test_cases: [
      { input: "'()[]{}'", expected: "True" },
      { input: "'([)]'", expected: "False" }
    ]
  }
];

export const BENCHMARK_5_INTERVIEW_QUESTIONS: InterviewQuestion[] = [
  {
    id: "sam_q1",
    question_number: 1,
    total_questions: 5,
    question: "Hello Rakshita, welcome to your technical interview for the Cloud & DevOps Engineer role. To kick off: How do you choose between an SQL (Relational) database and a NoSQL document database when architecting a high-throughput backend?",
    rubric_tags: ["Core Concept Clarity", "Practical Trade-offs", "Real-World Application"]
  },
  {
    id: "sam_q2",
    question_number: 2,
    total_questions: 5,
    question: "When building REST APIs in production, what is the importance of idempotency, and which HTTP methods (GET, POST, PUT, DELETE) should be strictly idempotent?",
    rubric_tags: ["REST Standards", "Network Reliability", "System Integrity"]
  },
  {
    id: "sam_q3",
    question_number: 3,
    total_questions: 5,
    question: "Imagine an API endpoint is suddenly taking 2.5 seconds to respond under heavy user traffic. Walk me step-by-step through how you would diagnose the bottleneck.",
    rubric_tags: ["Debugging Strategy", "Database Indexing & Caching", "Observability"]
  },
  {
    id: "sam_q4",
    question_number: 4,
    total_questions: 5,
    question: "Tell me about a challenging bug or architecture issue you ran into during a project. How did you isolate the root cause and ensure it won't reoccur?",
    rubric_tags: ["STAR Method", "Root Cause Analysis", "Engineering Rigor"]
  },
  {
    id: "sam_q5",
    question_number: 5,
    total_questions: 5,
    question: "As user load and data volume explode, how would you decouple synchronous request-response bottlenecks using asynchronous message queues like Kafka, RabbitMQ, or Redis Streams?",
    rubric_tags: ["System Scalability", "Asynchronous Queuing", "Fault Tolerance & DLQ"]
  }
];
