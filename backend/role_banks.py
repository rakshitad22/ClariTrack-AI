from typing import List, Dict
from models import MCQQuestion, MCQOption, CodingChallenge

def get_role_mcqs(target_career: str = "Cloud & DevOps Engineer") -> List[MCQQuestion]:
    career = (target_career or "").lower()
    
    # 1. CLOUD & DEVOPS ENGINEER
    if "devops" in career or "cloud" in career or "infrastructure" in career:
        return [
            MCQQuestion(
                id="cdo_1",
                question="In Linux file permissions, what access level does the octal mode 'chmod 755 script.sh' grant?",
                options=[
                    MCQOption(id="A", text="Read, Write, Execute for Owner; Read & Execute for Group and Others"),
                    MCQOption(id="B", text="Full access for everyone"),
                    MCQOption(id="C", text="Read & Execute only for Owner; Read only for Others"),
                    MCQOption(id="D", text="Read & Write for Owner; No access for Others")
                ],
                correct_option_id="A",
                explanation="7 (4+2+1) grants rwx to owner; 5 (4+0+1) grants r-x to group and others."
            ),
            MCQQuestion(
                id="cdo_2",
                question="Why are Docker multi-stage builds recommended for production container images?",
                options=[
                    MCQOption(id="A", text="They automatically mount persistent host volumes"),
                    MCQOption(id="B", text="They separate heavy build toolchains (compilers, SDKs) from the final slim runtime container"),
                    MCQOption(id="C", text="They run containers as root by default"),
                    MCQOption(id="D", text="They bypass Docker layer caching completely")
                ],
                correct_option_id="B",
                explanation="Multi-stage builds leave compilers and dev dependencies in build stages, copying only compiled binaries or static assets into a lightweight runtime image."
            ),
            MCQQuestion(
                id="cdo_3",
                question="In Kubernetes, what is the default Service type if no 'type' field is specified?",
                options=[
                    MCQOption(id="A", text="NodePort"),
                    MCQOption(id="B", text="ClusterIP"),
                    MCQOption(id="C", text="LoadBalancer"),
                    MCQOption(id="D", text="ExternalName")
                ],
                correct_option_id="B",
                explanation="ClusterIP is the default Kubernetes Service type, exposing the service on an internal IP reachable only from within the cluster."
            ),
            MCQQuestion(
                id="cdo_4",
                question="Which Linux signal is sent by default when running 'kill <PID>' to request graceful process termination?",
                options=[
                    MCQOption(id="A", text="SIGKILL (9)"),
                    MCQOption(id="B", text="SIGTERM (15)"),
                    MCQOption(id="C", text="SIGSTOP (19)"),
                    MCQOption(id="D", text="SIGHUP (1)")
                ],
                correct_option_id="B",
                explanation="'kill <PID>' sends SIGTERM (15), allowing the target process to trap the signal, finish active requests, and shut down cleanly."
            ),
            MCQQuestion(
                id="cdo_5",
                question="In Kubernetes Deployments, what is the purpose of 'maxSurge' during a rolling update?",
                options=[
                    MCQOption(id="A", text="The maximum number of seconds to wait before forcing a pod termination"),
                    MCQOption(id="B", text="The maximum number of Pods that can be scheduled above the desired replica count during an update"),
                    MCQOption(id="C", text="The CPU throttling ceiling for container processes"),
                    MCQOption(id="D", text="The maximum number of ingress requests allowed per second")
                ],
                correct_option_id="B",
                explanation="maxSurge specifies the maximum number or percentage of extra Pods that can be created above the desired replica count during a rollout."
            ),
            MCQQuestion(
                id="cdo_6",
                question="In Terraform, why should state locking be enabled using a distributed lock like AWS DynamoDB?",
                options=[
                    MCQOption(id="A", text="To compress the state file before uploading to S3"),
                    MCQOption(id="B", text="To prevent concurrent 'terraform apply' runs from corrupting the remote state file"),
                    MCQOption(id="C", text="To encrypt sensitive variable inputs"),
                    MCQOption(id="D", text="To automate rollback on provisioning failure")
                ],
                correct_option_id="B",
                explanation="State locking ensures that multiple engineers or CI/CD pipelines cannot run concurrent operations that would race and corrupt infrastructure state."
            ),
            MCQQuestion(
                id="cdo_7",
                question="In Docker, what is the key behavioral difference between 'ENTRYPOINT' and 'CMD'?",
                options=[
                    MCQOption(id="A", text="CMD cannot take default arguments; ENTRYPOINT can"),
                    MCQOption(id="B", text="ENTRYPOINT defines the executable to run; CMD provides default arguments that can easily be overridden at docker run"),
                    MCQOption(id="C", text="ENTRYPOINT runs only during docker build; CMD runs at runtime"),
                    MCQOption(id="D", text="There is no difference in Linux containers")
                ],
                correct_option_id="B",
                explanation="ENTRYPOINT specifies the permanent fixed command, while CMD acts as default arguments that can be overridden by arguments passed to 'docker run'."
            ),
            MCQQuestion(
                id="cdo_8",
                question="Which Kubernetes probe is responsible for deciding whether a Pod should receive user traffic from a Service?",
                options=[
                    MCQOption(id="A", text="Liveness Probe"),
                    MCQOption(id="B", text="Readiness Probe"),
                    MCQOption(id="C", text="Startup Probe"),
                    MCQOption(id="D", text="Security Probe")
                ],
                correct_option_id="B",
                explanation="Readiness probes determine when a Pod is ready to accept traffic. If it fails, endpoints controller removes the Pod from Service routing."
            ),
            MCQQuestion(
                id="cdo_9",
                question="In CI/CD with GitHub Actions, which keyword ensures that a step runs even if previous steps failed?",
                options=[
                    MCQOption(id="A", text="if: always()"),
                    MCQOption(id="B", text="retry: 3"),
                    MCQOption(id="C", text="ignore-errors: true"),
                    MCQOption(id="D", text="run-anyway: true")
                ],
                correct_option_id="A",
                explanation="Using 'if: always()' forces the step to execute regardless of whether earlier steps succeeded or failed (ideal for teardown/reporting)."
            ),
            MCQQuestion(
                id="cdo_10",
                question="What Prometheus metric type is most appropriate for counting cumulative HTTP request totals?",
                options=[
                    MCQOption(id="A", text="Gauge"),
                    MCQOption(id="B", text="Counter"),
                    MCQOption(id="C", text="Histogram"),
                    MCQOption(id="D", text="Summary")
                ],
                correct_option_id="B",
                explanation="A Counter is a monotonically increasing cumulative metric that only increases or resets to zero on restart, ideal for request counts and error totals."
            ),
            MCQQuestion(
                id="cdo_11",
                question="In Nginx reverse proxy configuration, which directive forwards the real client IP to the upstream server?",
                options=[
                    MCQOption(id="A", text="proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;"),
                    MCQOption(id="B", text="client_ip_forward on;"),
                    MCQOption(id="C", text="proxy_pass_real_ip true;"),
                    MCQOption(id="D", text="proxy_ssl_verify on;")
                ],
                correct_option_id="A",
                explanation="Setting X-Forwarded-For and X-Real-IP headers ensures the upstream backend perceives the original client IP rather than the Nginx proxy's internal IP."
            ),
            MCQQuestion(
                id="cdo_12",
                question="What does the Linux command 'lsof -i :8000' do?",
                options=[
                    MCQOption(id="A", text="Opens port 8000 on the firewall"),
                    MCQOption(id="B", text="Lists all processes listening on or communicating through port 8000"),
                    MCQOption(id="C", text="Logs network packets over port 8000 to disk"),
                    MCQOption(id="D", text="Terminates any process on port 8000")
                ],
                correct_option_id="B",
                explanation="'lsof -i :8000' lists open internet sockets and processes binding to port 8000."
            ),
            MCQQuestion(
                id="cdo_13",
                question="In Kubernetes, what happens to a PersistentVolume (PV) when its associated PVC is deleted if its reclaim policy is 'Retain'?",
                options=[
                    MCQOption(id="A", text="The PV is automatically deleted from cloud storage"),
                    MCQOption(id="B", text="The PV remains existing in 'Released' state and its physical storage is preserved"),
                    MCQOption(id="C", text="The PV is immediately reformatted and reassigned"),
                    MCQOption(id="D", text="The Kubernetes cluster triggers node cordon")
                ],
                correct_option_id="B",
                explanation="With 'Retain' policy, when the PVC is deleted, the PV is retained and transitions to Released state, preserving data until manual recovery."
            ),
            MCQQuestion(
                id="cdo_14",
                question="In AWS IAM, what principle dictates that a user or service should only receive the minimum permissions necessary?",
                options=[
                    MCQOption(id="A", text="Zero Trust Isolation"),
                    MCQOption(id="B", text="Principle of Least Privilege (PoLP)"),
                    MCQOption(id="C", text="Role Based Federation"),
                    MCQOption(id="D", text="Ephemeral Authorization")
                ],
                correct_option_id="B",
                explanation="Principle of Least Privilege ensures entities hold strictly the minimum required access rights to perform their assigned duty."
            ),
            MCQQuestion(
                id="cdo_15",
                question="What is the function of an Ingress Controller (like Nginx Ingress) in Kubernetes?",
                options=[
                    MCQOption(id="A", text="Allocating hardware GPUs to worker nodes"),
                    MCQOption(id="B", text="Managing external HTTP/HTTPS routing, host-based routing, and SSL termination into cluster services"),
                    MCQOption(id="C", text="Encrypting etcd database backups"),
                    MCQOption(id="D", text="Provisioning physical compute hardware")
                ],
                correct_option_id="B",
                explanation="Ingress Controllers fulfill Ingress resources by providing layer-7 routing rules, domain name mapping, and SSL termination."
            ),
            MCQQuestion(
                id="cdo_16",
                question="In Git, what does 'git stash pop' do?",
                options=[
                    MCQOption(id="A", text="Deletes all uncommitted changes permanently"),
                    MCQOption(id="B", text="Applies the most recently stashed changes and removes them from the stash list"),
                    MCQOption(id="C", text="Creates a new merge commit from stash"),
                    MCQOption(id="D", text="Pushes stashed commits to origin/main")
                ],
                correct_option_id="B",
                explanation="'git stash pop' re-applies the top stash entry onto the working directory and deletes it from stash history."
            ),
            MCQQuestion(
                id="cdo_17",
                question="In cloud networking, what is the role of a NAT Gateway in a private subnet?",
                options=[
                    MCQOption(id="A", text="Allowing instances in private subnets outbound internet access while blocking unsolicited inbound connections"),
                    MCQOption(id="B", text="Serving public web traffic to end users"),
                    MCQOption(id="C", text="Encrypting database connections"),
                    MCQOption(id="D", text="Accelerating DNS resolutions")
                ],
                correct_option_id="A",
                explanation="A NAT Gateway allows private subnet instances (like backend DBs) to download updates or reach external APIs without giving them public IP addresses."
            ),
            MCQQuestion(
                id="cdo_18",
                question="What does the command 'docker system prune -a' do?",
                options=[
                    MCQOption(id="A", text="Stops all running containers only"),
                    MCQOption(id="B", text="Removes all stopped containers, unused networks, and all images not referenced by running containers"),
                    MCQOption(id="C", text="Resets the Docker daemon config"),
                    MCQOption(id="D", text="Reinstalls the Docker engine")
                ],
                correct_option_id="B",
                explanation="'docker system prune -a' cleans up all unused containers, networks, and unreferenced images, freeing substantial disk space."
            ),
            MCQQuestion(
                id="cdo_19",
                question="In Kubernetes, what is the difference between a ConfigMap and a Secret?",
                options=[
                    MCQOption(id="A", text="ConfigMaps are for pods; Secrets are for nodes"),
                    MCQOption(id="B", text="ConfigMaps store non-confidential configuration data; Secrets store sensitive credentials (base64-encoded or KMS-encrypted)"),
                    MCQOption(id="C", text="Secrets cannot be mounted as files into pods"),
                    MCQOption(id="D", text="ConfigMaps are read-only; Secrets can be updated on the fly")
                ],
                correct_option_id="B",
                explanation="ConfigMaps hold plain text configuration settings, whereas Secrets hold sensitive tokens, passwords, and TLS certificates with dedicated access control."
            ),
            MCQQuestion(
                id="cdo_20",
                question="What is the default restart policy of a standalone Kubernetes Pod if left unspecified?",
                options=[
                    MCQOption(id="A", text="Never"),
                    MCQOption(id="B", text="Always"),
                    MCQOption(id="C", text="OnFailure"),
                    MCQOption(id="D", text="Conditional")
                ],
                correct_option_id="B",
                explanation="The default restartPolicy for Kubernetes Pods is 'Always', automatically restarting container processes that exit."
            )
        ]

    # 2. FULL-STACK DEVELOPER
    elif "full" in career or "frontend" in career or "web" in career:
        return [
            MCQQuestion(
                id="fsd_1",
                question="In React, why must you include a cleanup function in a useEffect hook that subscribes to an external event listener?",
                options=[
                    MCQOption(id="A", text="To force a component re-render on unmount"),
                    MCQOption(id="B", text="To prevent memory leaks and duplicate handler execution when the component unmounts or dependencies change"),
                    MCQOption(id="C", text="React throws a compiler error without it"),
                    MCQOption(id="D", text="To clear the Redux global store")
                ],
                correct_option_id="B",
                explanation="The cleanup function removes stale event listeners, timers, and active subscriptions, preventing zombie event handlers and memory leaks."
            ),
            MCQQuestion(
                id="fsd_2",
                question="What is the primary difference between 'useMemo' and 'useCallback' in React?",
                options=[
                    MCQOption(id="A", text="useMemo caches a computed value; useCallback caches a function definition between renders"),
                    MCQOption(id="B", text="useMemo is for class components; useCallback is for functional components"),
                    MCQOption(id="C", text="useCallback runs asynchronously in a web worker"),
                    MCQOption(id="D", text="There is no difference; they are aliases")
                ],
                correct_option_id="A",
                explanation="useMemo memoizes the result of invoking a calculation function; useCallback memoizes the function instance itself to prevent unnecessary child re-renders."
            ),
            MCQQuestion(
                id="fsd_3",
                question="In modern JavaScript, what is the order of execution between microtasks (Promises) and macrotasks (setTimeout)?",
                options=[
                    MCQOption(id="A", text="Macrotasks run before all microtasks"),
                    MCQOption(id="B", text="All pending microtasks in the queue are executed immediately after current call stack drains, before the next macrotask"),
                    MCQOption(id="C", text="They run strictly in alternating turns"),
                    MCQOption(id="D", text="Microtasks run only when browser is idle")
                ],
                correct_option_id="B",
                explanation="When the call stack empties, the JavaScript runtime drains the entire microtask queue (Promise callbacks) before picking up the next macrotask (setTimeout/setInterval)."
            ),
            MCQQuestion(
                id="fsd_4",
                question="What security vulnerability does setting the 'httpOnly' flag on session cookies prevent?",
                options=[
                    MCQOption(id="A", text="SQL Injection (SQLi)"),
                    MCQOption(id="B", text="Cross-Site Scripting (XSS) access to the cookie via document.cookie"),
                    MCQOption(id="C", text="Cross-Site Request Forgery (CSRF)"),
                    MCQOption(id="D", text="Distributed Denial of Service (DDoS)")
                ],
                correct_option_id="B",
                explanation="httpOnly prevents client-side JavaScript from accessing the cookie via document.cookie, mitigating session token theft through XSS exploits."
            ),
            MCQQuestion(
                id="fsd_5",
                question="In HTTP Cross-Origin Resource Sharing (CORS), when does the browser send an OPTIONS preflight request?",
                options=[
                    MCQOption(id="A", text="Only on GET requests with no parameters"),
                    MCQOption(id="B", text="When the request uses methods other than GET/POST/HEAD, or includes custom authorization headers"),
                    MCQOption(id="C", text="Only when communicating over HTTP instead of HTTPS"),
                    MCQOption(id="D", text="On every single fetch request without exception")
                ],
                correct_option_id="B",
                explanation="Preflight OPTIONS requests are triggered whenever requests are non-simple (e.g. methods like PUT/DELETE or custom headers like Authorization)."
            ),
            MCQQuestion(
                id="fsd_6",
                question="In TypeScript, what does the 'Partial<T>' utility type do?",
                options=[
                    MCQOption(id="A", text="Makes all properties in type T required"),
                    MCQOption(id="B", text="Constructs a type with all properties of T set to optional (?)"),
                    MCQOption(id="C", text="Excludes null and undefined from T"),
                    MCQOption(id="D", text="Picks a subset of keys from T")
                ],
                correct_option_id="B",
                explanation="Partial<T> transforms all properties of T into optional fields, enabling partial updates."
            ),
            MCQQuestion(
                id="fsd_7",
                question="What is the 'N+1 Query Problem' in ORM-based backend architectures?",
                options=[
                    MCQOption(id="A", text="Running 1 query for parent records followed by N individual queries for each child record instead of an eager JOIN"),
                    MCQOption(id="B", text="Database deadlock caused by N+1 concurrent transactions"),
                    MCQOption(id="C", text="Exceeding the maximum database connection pool limit"),
                    MCQOption(id="D", text="A query taking N+1 seconds to complete")
                ],
                correct_option_id="A",
                explanation="The N+1 problem occurs when fetching N parent items triggers N additional separate queries to load related child records rather than fetching them in a single batch JOIN."
            ),
            MCQQuestion(
                id="fsd_8",
                question="In Next.js, what is the primary benefit of Server-Side Rendering (SSR) compared to Client-Side Rendering (CSR)?",
                options=[
                    MCQOption(id="A", text="Eliminating all server hardware costs"),
                    MCQOption(id="B", text="Delivering pre-rendered HTML on each request for superior SEO indexation and faster First Contentful Paint"),
                    MCQOption(id="C", text="Allowing client browser to execute Node.js modules"),
                    MCQOption(id="D", text="Bypassing CORS checks completely")
                ],
                correct_option_id="B",
                explanation="SSR generates full HTML on the server per request, allowing web crawlers to index content easily and rendering UI without waiting for client bundles to download."
            ),
            MCQQuestion(
                id="fsd_9",
                question="Which CSS property creates a new stacking context without using 'position: relative'?",
                options=[
                    MCQOption(id="A", text="display: flex"),
                    MCQOption(id="B", text="opacity: 0.99 or transform: translateZ(0)"),
                    MCQOption(id="C", text="box-sizing: border-box"),
                    MCQOption(id="D", text="margin: auto")
                ],
                correct_option_id="B",
                explanation="Applying opacity < 1, transform, filter, or will-change creates a new stacking context in the CSS rendering tree."
            ),
            MCQQuestion(
                id="fsd_10",
                question="In RESTful APIs, which status code should be returned when a resource was successfully created via POST?",
                options=[
                    MCQOption(id="A", text="200 OK"),
                    MCQOption(id="B", text="201 Created"),
                    MCQOption(id="C", text="204 No Content"),
                    MCQOption(id="D", text="202 Accepted")
                ],
                correct_option_id="B",
                explanation="HTTP 201 Created confirms that the request succeeded and a new resource was created, typically returning the newly created entity in the response body."
            ),
            MCQQuestion(
                id="fsd_11",
                question="What is the difference between 'localStorage' and 'sessionStorage' in browser storage?",
                options=[
                    MCQOption(id="A", text="localStorage is encrypted automatically; sessionStorage is plain text"),
                    MCQOption(id="B", text="localStorage persists until cleared; sessionStorage clears automatically when the browser tab/session closes"),
                    MCQOption(id="C", text="sessionStorage can store up to 50MB; localStorage is capped at 1MB"),
                    MCQOption(id="D", text="localStorage sends data to server headers automatically")
                ],
                correct_option_id="B",
                explanation="sessionStorage is tied to the lifecycle of the browser tab and clears upon closing; localStorage persists indefinitely until explicitly cleared."
            ),
            MCQQuestion(
                id="fsd_12",
                question="In React, why should array indices NOT be used as keys when list items can be re-ordered or filtered?",
                options=[
                    MCQOption(id="A", text="React will throw a runtime syntax exception"),
                    MCQOption(id="B", text="It can cause component state bugs, incorrect input bindings, and degraded reconciliation diffing performance"),
                    MCQOption(id="C", text="Indices are not supported in React 18"),
                    MCQOption(id="D", text="It prevents Tailwind CSS from applying styles")
                ],
                correct_option_id="B",
                explanation="Using array index as key breaks React's reconciliation identity when items shift, causing inputs or component state to stick to the wrong item."
            ),
            MCQQuestion(
                id="fsd_13",
                question="In WebSocket communication, what HTTP status code confirms the initial handshake upgrade?",
                options=[
                    MCQOption(id="A", text="101 Switching Protocols"),
                    MCQOption(id="B", text="200 OK"),
                    MCQOption(id="C", text="301 Moved Permanently"),
                    MCQOption(id="D", text="206 Partial Content")
                ],
                correct_option_id="A",
                explanation="HTTP 101 Switching Protocols confirms that the server accepted the client's request to upgrade the connection from HTTP to bidirectional WebSocket."
            ),
            MCQQuestion(
                id="fsd_14",
                question="In modern CSS, what does 'box-sizing: border-box' change about element dimensions?",
                options=[
                    MCQOption(id="A", text="Padding and border are included within the specified width and height"),
                    MCQOption(id="B", text="Padding and border are added onto the width, expanding the element"),
                    MCQOption(id="C", text="Margins are merged with border width"),
                    MCQOption(id="D", text="It locks element aspect ratio")
                ],
                correct_option_id="A",
                explanation="'border-box' ensures padding and border widths are contained inside the element's declared width and height, preventing unexpected horizontal overflows."
            ),
            MCQQuestion(
                id="fsd_15",
                question="What is the purpose of the 'Content-Security-Policy' (CSP) HTTP response header?",
                options=[
                    MCQOption(id="A", text="To compress image assets using gzip"),
                    MCQOption(id="B", text="To restrict resources (scripts, styles, images) the browser is allowed to load, preventing XSS attacks"),
                    MCQOption(id="C", text="To enforce user authentication tokens"),
                    MCQOption(id="D", text="To enable HTTP/2 server push")
                ],
                correct_option_id="B",
                explanation="CSP restricts valid sources of executable scripts, stylesheets, and images, drastically mitigating cross-site scripting (XSS) and data injection."
            ),
            MCQQuestion(
                id="fsd_16",
                question="In JavaScript, what does 'Promise.allSettled()' do compared to 'Promise.all()'?",
                options=[
                    MCQOption(id="A", text="It rejects immediately if any single promise fails"),
                    MCQOption(id="B", text="It waits for all promises to either fulfill or reject, returning an array of outcome objects"),
                    MCQOption(id="C", text="It only executes the fastest promise"),
                    MCQOption(id="D", text="It cancels running promises after 5 seconds")
                ],
                correct_option_id="B",
                explanation="Promise.all() rejects as soon as one promise fails; Promise.allSettled() always waits for every promise to complete, returning status and value/reason for each."
            ),
            MCQQuestion(
                id="fsd_17",
                question="In SQL, what is the key difference between a clustered and non-clustered index?",
                options=[
                    MCQOption(id="A", text="A table can have multiple clustered indexes, but only one non-clustered index"),
                    MCQOption(id="B", text="A clustered index physically reorders table row storage on disk; non-clustered creates a separate lookup structure with pointers"),
                    MCQOption(id="C", text="Non-clustered indexes do not support B+ Trees"),
                    MCQOption(id="D", text="Clustered indexes only work with string columns")
                ],
                correct_option_id="B",
                explanation="Because physical records can only be stored in one physical order on disk, a table can possess only one clustered index (usually the Primary Key)."
            ),
            MCQQuestion(
                id="fsd_18",
                question="In web performance metrics, what does 'Largest Contentful Paint' (LCP) measure?",
                options=[
                    MCQOption(id="A", text="The time taken for the DNS lookup to finish"),
                    MCQOption(id="B", text="The render time of the largest image or text block visible within the viewport"),
                    MCQOption(id="C", text="The total size of the JavaScript bundle in megabytes"),
                    MCQOption(id="D", text="The delay before a button responds to user click")
                ],
                correct_option_id="B",
                explanation="LCP measures perceived load speed by timing when the main hero image or dominant content block has finished rendering on screen."
            ),
            MCQQuestion(
                id="fsd_19",
                question="In Node.js, why is 'fs.readFile' preferable to 'fs.readFileSync' in web server route handlers?",
                options=[
                    MCQOption(id="A", text="readFileSync uses more disk space"),
                    MCQOption(id="B", text="readFileSync blocks the single-threaded event loop, freezing all concurrent user requests until file reading finishes"),
                    MCQOption(id="C", text="readFile is only for JSON files"),
                    MCQOption(id="D", text="readFileSync cannot read files larger than 1MB")
                ],
                correct_option_id="B",
                explanation="Synchronous file I/O blocks Node.js's single main thread, causing severe latency spikes for all concurrent users connected to the server."
            ),
            MCQQuestion(
                id="fsd_20",
                question="In React 18, what is the role of the 'useTransition' hook?",
                options=[
                    MCQOption(id="A", text="To animate CSS opacity transitions automatically"),
                    MCQOption(id="B", text="To mark non-urgent state updates as interruptible transitions, keeping the UI responsive to user keystrokes"),
                    MCQOption(id="C", text="To migrate state from Redux to Context API"),
                    MCQOption(id="D", text="To switch router routes asynchronously")
                ],
                correct_option_id="B",
                explanation="useTransition allows marking heavy rendering updates (like large list filtering) as non-urgent transitions, prioritizing immediate user inputs."
            )
        ]

    # 3. AI / ML ENGINEER
    elif "ai" in career or "ml" in career or "machine" in career or "deep" in career:
        return [
            MCQQuestion(
                id="aiml_1",
                question="In linear algebra for deep learning, what condition must be met to compute the matrix product C = A @ B if A is of shape (M, K)?",
                options=[
                    MCQOption(id="A", text="B must have shape (K, N)"),
                    MCQOption(id="B", text="B must have shape (M, K)"),
                    MCQOption(id="C", text="B must be a square matrix (M, M)"),
                    MCQOption(id="D", text="Both matrices must have identical dimensions")
                ],
                correct_option_id="A",
                explanation="Matrix multiplication requires the inner dimensions to match: (M, K) multiplied by (K, N) yields resulting matrix (M, N)."
            ),
            MCQQuestion(
                id="aiml_2",
                question="In machine learning model evaluation, what does high variance (overfitting) typically manifest as?",
                options=[
                    MCQOption(id="A", text="High training error and high test error"),
                    MCQOption(id="B", text="Very low training error but high test error on unseen data"),
                    MCQOption(id="C", text="Zero gradient updates during backpropagation"),
                    MCQOption(id="D", text="Model predicting the mean value for every sample")
                ],
                correct_option_id="B",
                explanation="Overfitting (high variance) occurs when a model memorizes training noise, achieving near-perfect training loss but failing to generalize to validation/test sets."
            ),
            MCQQuestion(
                id="aiml_3",
                question="In neural network training, why is the ReLU activation function (f(x) = max(0, x)) preferred over Sigmoid in hidden layers?",
                options=[
                    MCQOption(id="A", text="It mitigates the vanishing gradient problem for positive inputs and is computationally fast"),
                    MCQOption(id="B", text="It squashes outputs between 0 and 1"),
                    MCQOption(id="C", text="It ensures gradients never exceed 0.5"),
                    MCQOption(id="D", text="It is differentiable at x = 0")
                ],
                correct_option_id="A",
                explanation="Sigmoid saturates at both tails with near-zero gradients (vanishing gradient); ReLU maintains a constant gradient of 1 for x > 0 and computes efficiently."
            ),
            MCQQuestion(
                id="aiml_4",
                question="In Transformer architectures, what is the core equation for Scaled Dot-Product Attention?",
                options=[
                    MCQOption(id="A", text="Attention(Q, K, V) = softmax(Q K^T / sqrt(d_k)) V"),
                    MCQOption(id="B", text="Attention(Q, K, V) = sigmoid(Q @ K) + V"),
                    MCQOption(id="C", text="Attention(Q, K, V) = tanh(W_q Q + W_k K) V"),
                    MCQOption(id="D", text="Attention(Q, K, V) = ReLU(Q @ V^T) K")
                ],
                correct_option_id="A",
                explanation="Scaled Dot-Product Attention computes query-key similarity scaled by sqrt(d_k) to prevent vanishing gradients in softmax, then weights the values V."
            ),
            MCQQuestion(
                id="aiml_5",
                question="In vector databases (like Qdrant or Pinecone), which approximate nearest neighbor (ANN) graph algorithm is widely considered state-of-the-art for fast vector retrieval?",
                options=[
                    MCQOption(id="A", text="HNSW (Hierarchical Navigable Small World)"),
                    MCQOption(id="B", text="Dijkstra's Algorithm"),
                    MCQOption(id="C", text="Bellman-Ford"),
                    MCQOption(id="D", text="K-Means Clustering only")
                ],
                correct_option_id="A",
                explanation="HNSW builds multi-layer hierarchical proximity graphs enabling logarithmic sub-linear vector search with high recall."
            ),
            MCQQuestion(
                id="aiml_6",
                question="What is the key mathematical difference between L1 (Lasso) and L2 (Ridge) weight regularization?",
                options=[
                    MCQOption(id="A", text="L1 adds the sum of absolute weights driving unneeded weights to exactly zero (sparsity); L2 adds squared weights shrinking them continuously"),
                    MCQOption(id="B", text="L2 creates sparse feature sets while L1 preserves all features"),
                    MCQOption(id="C", text="L1 can only be applied to classification problems"),
                    MCQOption(id="D", text="L2 eliminates the bias term entirely")
                ],
                correct_option_id="A",
                explanation="L1 penalty encourages sparsity by driving coefficients of uninformative features to zero, acting as automatic feature selection."
            ),
            MCQQuestion(
                id="aiml_7",
                question="In Retrieval-Augmented Generation (RAG), why are dense vector embeddings often combined with sparse keyword search (BM25)?",
                options=[
                    MCQOption(id="A", text="To double the storage space in PostgreSQL"),
                    MCQOption(id="B", text="Hybrid search balances semantic conceptual matching (dense) with exact keyword/code identifier retrieval (sparse)"),
                    MCQOption(id="C", text="Dense embeddings cannot process English text"),
                    MCQOption(id="D", text="BM25 is a deep neural network")
                ],
                correct_option_id="B",
                explanation="Hybrid search merges dense semantic comprehension with BM25's strength in retrieving exact domain tokens, part numbers, and code symbols."
            ),
            MCQQuestion(
                id="aiml_8",
                question="In PyTorch, what is the purpose of calling 'optimizer.zero_grad()' before 'loss.backward()' in the training loop?",
                options=[
                    MCQOption(id="A", text="To clear model parameter weights to zero"),
                    MCQOption(id="B", text="To reset accumulated parameter gradients, preventing gradient buildup across mini-batches"),
                    MCQOption(id="C", text="To reset the learning rate schedule"),
                    MCQOption(id="D", text="To allocate GPU VRAM")
                ],
                correct_option_id="B",
                explanation="PyTorch accumulates gradients on .backward() calls by default. zero_grad() clears stale gradients from prior batches."
            ),
            MCQQuestion(
                id="aiml_9",
                question="When evaluating an imbalanced binary classifier (e.g., 99% negative class, 1% positive fraud), why is accuracy a misleading metric?",
                options=[
                    MCQOption(id="A", text="Accuracy cannot be calculated on binary numbers"),
                    MCQOption(id="B", text="A naive model that predicts 'Negative' for every case achieves 99% accuracy while detecting zero true positives"),
                    MCQOption(id="C", text="Accuracy is always lower than ROC-AUC"),
                    MCQOption(id="D", text="Accuracy requires equal class variance")
                ],
                correct_option_id="B",
                explanation="In highly imbalanced datasets, accuracy fails to measure detection capability. Precision, Recall, PR-AUC, and F1-score are necessary."
            ),
            MCQQuestion(
                id="aiml_10",
                question="In generative LLMs, what does lowering the 'temperature' parameter (e.g., from 0.8 to 0.2) do?",
                options=[
                    MCQOption(id="A", text="Makes the model generate text twice as fast"),
                    MCQOption(id="B", text="Makes token sampling more deterministic and focused on top-probability tokens, reducing randomness"),
                    MCQOption(id="C", text="Expands the model's vocabulary size"),
                    MCQOption(id="D", text="Disables the model's safety filters")
                ],
                correct_option_id="B",
                explanation="Lowering temperature sharpens the softmax distribution over vocabulary tokens, favoring high-probability tokens for predictable, factual responses."
            ),
            MCQQuestion(
                id="aiml_11",
                question="In PyTorch, which context manager disables gradient computation during model inference to conserve memory?",
                options=[
                    MCQOption(id="A", text="with torch.no_grad():"),
                    MCQOption(id="B", text="with torch.eval():"),
                    MCQOption(id="C", text="with torch.freeze():"),
                    MCQOption(id="D", text="with torch.disable_autograd():")
                ],
                correct_option_id="A",
                explanation="'torch.no_grad()' deactivates autograd tape tracking, drastically reducing memory consumption and speeding up inference."
            ),
            MCQQuestion(
                id="aiml_12",
                question="In Natural Language Processing, what tokenization method is used by modern LLMs like GPT and Llama?",
                options=[
                    MCQOption(id="A", text="Word-level whitespace splitting"),
                    MCQOption(id="B", text="Byte-Pair Encoding (BPE) or WordPiece subword tokenization"),
                    MCQOption(id="C", text="Character-level ASCII only"),
                    MCQOption(id="D", text="Regex punctuation splitting")
                ],
                correct_option_id="B",
                explanation="Subword tokenizers like BPE decompose words into frequent subword fragments, handling out-of-vocabulary terms and rare words gracefully."
            ),
            MCQQuestion(
                id="aiml_13",
                question="What is the primary function of Batch Normalization in deep neural networks?",
                options=[
                    MCQOption(id="A", text="Normalizing layer inputs per mini-batch to stabilize internal covariate shift and enable higher learning rates"),
                    MCQOption(id="B", text="Compressing neural network weights into 8-bit integers"),
                    MCQOption(id="C", text="Eliminating all dropout layers"),
                    MCQOption(id="D", text="Converting tensors from CPU to GPU")
                ],
                correct_option_id="A",
                explanation="Batch Normalization normalizes activations across the mini-batch, smoothing the optimization landscape and speeding up convergence."
            ),
            MCQQuestion(
                id="aiml_14",
                question="In cosine similarity between two non-zero vectors A and B, what does a score of 1.0 indicate?",
                options=[
                    MCQOption(id="A", text="The vectors are orthogonal (90 degrees apart)"),
                    MCQOption(id="B", text="The vectors point in the exact same direction, indicating maximum semantic alignment"),
                    MCQOption(id="C", text="The vectors have opposite meanings (-180 degrees)"),
                    MCQOption(id="D", text="The vectors have identical Euclidean magnitude")
                ],
                correct_option_id="B",
                explanation="Cosine similarity computes cos(theta) = (A . B) / (||A|| ||B||). A score of 1.0 signifies theta = 0 degrees (collinear vectors)."
            ),
            MCQQuestion(
                id="aiml_15",
                question="In LLM fine-tuning, what is LoRA (Low-Rank Adaptation)?",
                options=[
                    MCQOption(id="A", text="Retraining all model weights from scratch with small learning rates"),
                    MCQOption(id="B", text="Freezing pre-trained model weights and injecting trainable rank decomposition matrices into Transformer attention layers"),
                    MCQOption(id="C", text="Quantizing models to 1-bit binary weights"),
                    MCQOption(id="D", text="Pruning 90% of model layers")
                ],
                correct_option_id="B",
                explanation="LoRA freezes base weights and decomposes the weight update delta into low-rank matrices (B @ A), reducing trainable parameters by 99%."
            ),
            MCQQuestion(
                id="aiml_16",
                question="What does the F1-score represent in statistical classification?",
                options=[
                    MCQOption(id="A", text="Arithmetic mean of Accuracy and Loss"),
                    MCQOption(id="B", text="Harmonic mean of Precision and Recall: 2 * (P * R) / (P + R)"),
                    MCQOption(id="C", text="Geometric mean of Sensitivity and Specificity"),
                    MCQOption(id="D", text="Area under the ROC curve")
                ],
                correct_option_id="B",
                explanation="F1-score is the harmonic mean of precision and recall, balancing false positives and false negatives."
            ),
            MCQQuestion(
                id="aiml_17",
                question="In supervised learning, what is Cross-Validation (e.g., 5-Fold CV) primarily used for?",
                options=[
                    MCQOption(id="A", text="Training 5 different architectures simultaneously"),
                    MCQOption(id="B", text="Assessing model generalization performance and mitigating dataset splitting bias across multiple folds"),
                    MCQOption(id="C", text="Cleaning duplicate dataset rows"),
                    MCQOption(id="D", text="Optimizing GPU kernel thread blocks")
                ],
                correct_option_id="B",
                explanation="K-fold cross-validation partitions data into K subsets, iteratively training on K-1 and testing on the remaining fold to ensure reliable generalization."
            ),
            MCQQuestion(
                id="aiml_18",
                question="In LLM inference, what is the purpose of KV Caching (Key-Value Caching)?",
                options=[
                    MCQOption(id="A", text="Saving prompt prompts to a Redis server"),
                    MCQOption(id="B", text="Storing past keys and values of previous tokens in attention layers to avoid redundant recalculation on each generated token"),
                    MCQOption(id="C", text="Caching SQL queries in PostgreSQL"),
                    MCQOption(id="D", text="Compressing embedding vectors into 4-bit floats")
                ],
                correct_option_id="B",
                explanation="Autoregressive generation recalculates attention on prior tokens. KV caching stores prior key/value vectors, transforming generation from O(N^2) to O(N)."
            ),
            MCQQuestion(
                id="aiml_19",
                question="In gradient descent, how does the Adam optimizer improve over standard Stochastic Gradient Descent (SGD)?",
                options=[
                    MCQOption(id="A", text="It eliminates the backpropagation step"),
                    MCQOption(id="B", text="It computes individual adaptive learning rates for parameters using exponentially decaying moving averages of past gradients and squared gradients"),
                    MCQOption(id="C", text="It only updates weights on alternate epochs"),
                    MCQOption(id="D", text="It restricts loss values to positive integers")
                ],
                correct_option_id="B",
                explanation="Adam combines Momentum (first moment of gradients) with RMSProp (second moment of squared gradients) for robust adaptive learning rates."
            ),
            MCQQuestion(
                id="aiml_20",
                question="In RAG evaluation, what does the 'Hallucination' metric assess?",
                options=[
                    MCQOption(id="A", text="Whether the LLM response is factually grounded in the retrieved reference context rather than fabricated"),
                    MCQOption(id="B", text="Whether the retrieved chunks contain spelling errors"),
                    MCQOption(id="C", text="The latency of vector database indexing"),
                    MCQOption(id="D", text="The size of the context window")
                ],
                correct_option_id="A",
                explanation="Hallucination (faithfulness) measures whether every factual claim generated by the LLM is directly verifiable against the retrieved context."
            )
        ]

    # 4. DATA ANALYST
    elif "analyst" in career or "data" in career:
        return [
            MCQQuestion(
                id="da_1",
                question="In SQL, what is the difference between ROW_NUMBER(), RANK(), and DENSE_RANK() when two rows have duplicate values?",
                options=[
                    MCQOption(id="A", text="ROW_NUMBER assigns unique sequential integers; RANK leaves gaps after duplicates; DENSE_RANK assigns consecutive ranks without gaps"),
                    MCQOption(id="B", text="They behave identically"),
                    MCQOption(id="C", text="DENSE_RANK skips numbers; RANK does not"),
                    MCQOption(id="D", text="ROW_NUMBER can only be used with COUNT()")
                ],
                correct_option_id="A",
                explanation="With ties [100, 100, 90]: ROW_NUMBER gives 1, 2, 3; RANK gives 1, 1, 3; DENSE_RANK gives 1, 1, 2."
            ),
            MCQQuestion(
                id="da_2",
                question="In exploratory data analysis, which measure of central tendency is least sensitive to extreme outliers?",
                options=[
                    MCQOption(id="A", text="Arithmetic Mean"),
                    MCQOption(id="B", text="Median"),
                    MCQOption(id="C", text="Standard Deviation"),
                    MCQOption(id="D", text="Variance")
                ],
                correct_option_id="B",
                explanation="The Median is the middle value of sorted data, making it robust and unaffected by extreme skewness or outlier values."
            ),
            MCQQuestion(
                id="da_3",
                question="In SQL, what is the purpose of the 'COALESCE(val1, val2, val3)' function?",
                options=[
                    MCQOption(id="A", text="Concatenates string columns together"),
                    MCQOption(id="B", text="Returns the first non-null expression among its arguments"),
                    MCQOption(id="C", text="Converts integers to decimal floats"),
                    MCQOption(id="D", text="Calculates average across three rows")
                ],
                correct_option_id="B",
                explanation="COALESCE inspects its arguments in order and returns the first non-NULL value, frequently used to provide default fallback values."
            ),
            MCQQuestion(
                id="da_4",
                question="In statistics and A/B testing, what is a Type I error?",
                options=[
                    MCQOption(id="A", text="Failing to reject a false null hypothesis (False Negative)"),
                    MCQOption(id="B", text="Rejecting a true null hypothesis (False Positive)"),
                    MCQOption(id="C", text="A calculation error in sample standard deviation"),
                    MCQOption(id="D", text="Using sample size smaller than 30")
                ],
                correct_option_id="B",
                explanation="Type I error (alpha) occurs when you conclude there is an effect or difference when in reality none exists (False Positive)."
            ),
            MCQQuestion(
                id="da_5",
                question="In Pandas, what does the 'df.dropna(subset=['email'])' method do?",
                options=[
                    MCQOption(id="A", text="Drops the entire email column from the DataFrame"),
                    MCQOption(id="B", text="Removes rows where the 'email' column contains NaN / null values"),
                    MCQOption(id="C", text="Fills null emails with empty strings"),
                    MCQOption(id="D", text="Converts emails to lowercase")
                ],
                correct_option_id="B",
                explanation="Passing subset=['email'] restricts row deletion only to rows where the specified column possesses missing/null entries."
            ),
            MCQQuestion(
                id="da_6",
                question="In SQL, which window function retrieves the value of a column from the immediately preceding row within the partition?",
                options=[
                    MCQOption(id="A", text="LEAD()"),
                    MCQOption(id="B", text="LAG()"),
                    MCQOption(id="C", text="FIRST_VALUE()"),
                    MCQOption(id="D", text="PRIOR()")
                ],
                correct_option_id="B",
                explanation="LAG(column, offset) accesses data from a previous row at a specified physical offset, essential for calculating day-over-day growth rates."
            ),
            MCQQuestion(
                id="da_7",
                question="What does the Interquartile Range (IQR) represent in descriptive statistics?",
                options=[
                    MCQOption(id="A", text="Difference between Maximum and Minimum"),
                    MCQOption(id="B", text="Difference between the 75th percentile (Q3) and 25th percentile (Q1)"),
                    MCQOption(id="C", text="Square root of variance"),
                    MCQOption(id="D", text="Average deviation from median")
                ],
                correct_option_id="B",
                explanation="IQR = Q3 - Q1, capturing the spread of the middle 50% of the dataset and serving as the foundation for box plot outlier fences (1.5 * IQR)."
            ),
            MCQQuestion(
                id="da_8",
                question="In business analytics, what does 'Customer Churn Rate' measure?",
                options=[
                    MCQOption(id="A", text="The rate at which new customers register accounts"),
                    MCQOption(id="B", text="The percentage of customers who stop using or subscribing to a product/service over a given time period"),
                    MCQOption(id="C", text="The average customer lifetime revenue"),
                    MCQOption(id="D", text="Customer acquisition cost per click")
                ],
                correct_option_id="B",
                explanation="Churn Rate = (Lost Customers during period) / (Total Customers at start of period), measuring customer attrition."
            ),
            MCQQuestion(
                id="da_9",
                question="In SQL, what is the fundamental difference between 'WHERE' and 'HAVING' clauses?",
                options=[
                    MCQOption(id="A", text="HAVING filters rows before grouping; WHERE filters aggregated groups"),
                    MCQOption(id="B", text="WHERE filters individual rows before aggregation; HAVING filters groups after GROUP BY aggregation is applied"),
                    MCQOption(id="C", text="WHERE is only for numeric columns"),
                    MCQOption(id="D", text="HAVING can only be used with subqueries")
                ],
                correct_option_id="B",
                explanation="WHERE applies row-level filters prior to grouping. HAVING filters the result of aggregate expressions (e.g. HAVING COUNT(*) > 5) after GROUP BY."
            ),
            MCQQuestion(
                id="da_10",
                question="What does a Pearson correlation coefficient of r = -0.85 between two continuous variables indicate?",
                options=[
                    MCQOption(id="A", text="No correlation whatsoever"),
                    MCQOption(id="B", text="A strong negative linear relationship (as one variable increases, the other decreases)"),
                    MCQOption(id="C", text="A weak positive relationship"),
                    MCQOption(id="D", text="An 85% probability of causation")
                ],
                correct_option_id="B",
                explanation="Pearson's r ranges between -1 and +1. An r of -0.85 reflects a strong negative linear association."
            ),
            MCQQuestion(
                id="da_11",
                question="In SQL, what is the output of 'SELECT COUNT(*)' versus 'SELECT COUNT(column_name)' when a table has rows with NULL in that column?",
                options=[
                    MCQOption(id="A", text="Both return the exact same count"),
                    MCQOption(id="B", text="COUNT(*) counts all rows including NULLs; COUNT(column_name) ignores NULL entries"),
                    MCQOption(id="C", text="COUNT(column_name) throws a syntax error if null exists"),
                    MCQOption(id="D", text="COUNT(*) ignores NULLs")
                ],
                correct_option_id="B",
                explanation="COUNT(*) counts the total number of rows regardless of content; COUNT(col) counts only rows where the specified column is not NULL."
            ),
            MCQQuestion(
                id="da_12",
                question="In cohort analysis, what is the standard way to group users?",
                options=[
                    MCQOption(id="A", text="By their operating system"),
                    MCQOption(id="B", text="By a shared characteristic or event timing (e.g. month of initial signup/acquisition) and tracking behavior over time"),
                    MCQOption(id="C", text="By their alphabetical first name"),
                    MCQOption(id="D", text="By their IP subnet")
                ],
                correct_option_id="B",
                explanation="Cohort analysis tracks retention, engagement, and LTV over successive time periods for groups sharing a common starting timestamp (e.g. Jan 2026 cohort)."
            ),
            MCQQuestion(
                id="da_13",
                question="In Pandas, what does 'df.merge(df2, on='id', how='left')' perform?",
                options=[
                    MCQOption(id="A", text="Inner Join"),
                    MCQOption(id="B", text="Left Outer Join keeping all rows from df and matching records from df2 (filling unmatched with NaN)"),
                    MCQOption(id="C", text="Vertical concatenation of rows"),
                    MCQOption(id="D", text="Cross Join generating Cartesian product")
                ],
                correct_option_id="B",
                explanation="A Left Outer Join preserves every record from the left DataFrame and merges matching data from the right DataFrame on the shared key."
            ),
            MCQQuestion(
                id="da_14",
                question="What is the Central Limit Theorem (CLT) in inferential statistics?",
                options=[
                    MCQOption(id="A", text="All datasets follow a uniform distribution"),
                    MCQOption(id="B", text="The sampling distribution of the sample mean approaches a normal distribution as sample size N increases, regardless of population distribution shape"),
                    MCQOption(id="C", text="The median always equals the mean in large datasets"),
                    MCQOption(id="D", text="Sample variance decreases to zero")
                ],
                correct_option_id="B",
                explanation="CLT establishes that given a sufficiently large sample (N >= 30), the distribution of sample means approximates normality, justifying confidence intervals and hypothesis tests."
            ),
            MCQQuestion(
                id="da_15",
                question="In SQL Common Table Expressions (CTEs), what keyword introduces the temporary named result set?",
                options=[
                    MCQOption(id="A", text="DEFINE"),
                    MCQOption(id="B", text="WITH"),
                    MCQOption(id="C", text="TEMPORARY"),
                    MCQOption(id="D", text="CREATE TABLE")
                ],
                correct_option_id="B",
                explanation="A CTE is defined using the 'WITH cte_name AS (SELECT ...)' syntax, improving query readability and modular decomposition."
            ),
            MCQQuestion(
                id="da_16",
                question="What visualization chart is best suited for displaying the distribution and spread of continuous numerical data across categories?",
                options=[
                    MCQOption(id="A", text="Pie Chart"),
                    MCQOption(id="B", text="Box Plot (Box-and-Whisker) or Violin Plot"),
                    MCQOption(id="C", text="Radar Chart"),
                    MCQOption(id="D", text="Network Graph")
                ],
                correct_option_id="B",
                explanation="Box plots visually communicate median, quartiles, IQR, and outliers cleanly across groups."
            ),
            MCQQuestion(
                id="da_17",
                question="In SQL, what is the result of '1 = NULL'?",
                options=[
                    MCQOption(id="A", text="TRUE"),
                    MCQOption(id="B", text="FALSE"),
                    MCQOption(id="C", text="UNKNOWN / NULL (Three-valued logic)"),
                    MCQOption(id="D", text="Syntax Error")
                ],
                correct_option_id="C",
                explanation="SQL utilizes three-valued logic (TRUE, FALSE, UNKNOWN). Comparisons with NULL evaluate to UNKNOWN, which is why 'IS NULL' must be used."
            ),
            MCQQuestion(
                id="da_18",
                question="What is 'Survivorship Bias' in data analytics?",
                options=[
                    MCQOption(id="A", text="A bias occurring when you only analyze data that passed a selection hurdle while overlooking entities that failed to make it through"),
                    MCQOption(id="B", text="A bug where database backups survive node deletion"),
                    MCQOption(id="C", text="Survey questions leading users to say yes"),
                    MCQOption(id="D", text="Time series data lacking seasonal adjustment")
                ],
                correct_option_id="A",
                explanation="Survivorship bias concentrates on successful survivors of a process and ignores those that were eliminated, leading to overly optimistic conclusions."
            ),
            MCQQuestion(
                id="da_19",
                question="In data pipelines, what is the difference between ETL and ELT?",
                options=[
                    MCQOption(id="A", text="ETL transforms data in an intermediate compute layer before loading; ELT loads raw data directly into modern cloud warehouses (BigQuery/Snowflake) and transforms in-engine"),
                    MCQOption(id="B", text="ELT cannot handle structured SQL tables"),
                    MCQOption(id="C", text="ETL is only for real-time streaming"),
                    MCQOption(id="D", text="They are identical processes")
                ],
                correct_option_id="A",
                explanation="Modern cloud data warehouses leverage massively parallel processing, enabling ELT (Extract, Load raw, Transform inside warehouse via SQL/dbt)."
            ),
            MCQQuestion(
                id="da_20",
                question="In A/B testing, what does statistical power (typically set to 80%) measure?",
                options=[
                    MCQOption(id="A", text="The speed of the database server"),
                    MCQOption(id="B", text="The probability of correctly rejecting the null hypothesis when an actual real effect exists (1 - Beta)"),
                    MCQOption(id="C", text="The percentage of user clicks"),
                    MCQOption(id="D", text="The confidence interval width")
                ],
                correct_option_id="B",
                explanation="Statistical power is the sensitivity of the experiment: the probability that the test will detect a true treatment effect of a specified minimum magnitude."
            )
        ]

    # 5. SOFTWARE ENGINEER / BACKEND (Default)
    else:
        return [
            MCQQuestion(
                id="se_1",
                question="What is the average-case time complexity of lookup, insertion, and deletion operations in a well-distributed Hash Table?",
                options=[
                    MCQOption(id="A", text="O(1)"),
                    MCQOption(id="B", text="O(log N)"),
                    MCQOption(id="C", text="O(N)"),
                    MCQOption(id="D", text="O(N log N)")
                ],
                correct_option_id="A",
                explanation="A Hash Table provides amortized O(1) constant time complexity for insert, search, and delete operations when using an effective hash function with minimal collisions."
            ),
            MCQQuestion(
                id="se_2",
                question="In Python, what is the output of calling add_item(1) followed by add_item(2)?",
                code_snippet="def add_item(val, lst=[]):\n    lst.append(val)\n    return lst\n\nprint(add_item(1))\nprint(add_item(2))",
                options=[
                    MCQOption(id="A", text="[1] and [2]"),
                    MCQOption(id="B", text="[1] and [1, 2]"),
                    MCQOption(id="C", text="[1] and [2, 1]"),
                    MCQOption(id="D", text="TypeError: mutable default argument")
                ],
                correct_option_id="B",
                explanation="Default parameter values in Python are evaluated once when the function is defined, so mutable defaults like lists persist across function calls."
            ),
            MCQQuestion(
                id="se_3",
                question="Which of the following correctly describes the logical order of execution of SQL clauses?",
                options=[
                    MCQOption(id="A", text="SELECT -> FROM -> WHERE -> GROUP BY -> HAVING -> ORDER BY"),
                    MCQOption(id="B", text="FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY"),
                    MCQOption(id="C", text="FROM -> SELECT -> WHERE -> GROUP BY -> ORDER BY -> HAVING"),
                    MCQOption(id="D", text="WHERE -> FROM -> GROUP BY -> HAVING -> SELECT -> ORDER BY")
                ],
                correct_option_id="B",
                explanation="SQL query execution begins at the data source (FROM/JOIN), filters rows (WHERE), groups them (GROUP BY), filters groups (HAVING), evaluates expressions (SELECT), and finally sorts (ORDER BY)."
            ),
            MCQQuestion(
                id="se_4",
                question="In RESTful API design, which HTTP method is required to be strictly idempotent according to RFC 7231?",
                options=[
                    MCQOption(id="A", text="POST"),
                    MCQOption(id="B", text="PATCH"),
                    MCQOption(id="C", text="PUT"),
                    MCQOption(id="D", text="CONNECT")
                ],
                correct_option_id="C",
                explanation="PUT replaces the target resource entirely; repeating the same PUT request multiple times leaves the system in the identical state, satisfying the definition of idempotence."
            ),
            MCQQuestion(
                id="se_5",
                question="In relational database design, what does Third Normal Form (3NF) strictly require beyond 2NF?",
                options=[
                    MCQOption(id="A", text="All attributes must be atomic and non-repeating"),
                    MCQOption(id="B", text="Every non-key attribute must depend directly on the entire primary key, not a subset"),
                    MCQOption(id="C", text="There must be no transitive dependency for non-prime attributes on candidate keys"),
                    MCQOption(id="D", text="All foreign keys must have cascading deletion rules")
                ],
                correct_option_id="C",
                explanation="3NF requires a relation to be in 2NF and have no transitive functional dependencies of non-prime attributes on any candidate key."
            ),
            MCQQuestion(
                id="se_6",
                question="What is the worst-case time complexity of QuickSort when an unbalanced pivot is selected at every partition step?",
                options=[
                    MCQOption(id="A", text="O(N log N)"),
                    MCQOption(id="B", text="O(N^2)"),
                    MCQOption(id="C", text="O(log N)"),
                    MCQOption(id="D", text="O(2^N)")
                ],
                correct_option_id="B",
                explanation="If the pivot consistently splits an array of size N into 0 and N-1 elements, the recursion tree height degrades from log N to N, yielding O(N^2) total comparisons."
            ),
            MCQQuestion(
                id="se_7",
                question="In Git, what is the core behavioral difference between 'git merge' and 'git rebase'?",
                options=[
                    MCQOption(id="A", text="git merge deletes commit history; git rebase preserves it"),
                    MCQOption(id="B", text="git merge creates a 3-way merge commit; git rebase reapplies commits onto a new base commit linearly"),
                    MCQOption(id="C", text="git rebase can only be used on remote branches"),
                    MCQOption(id="D", text="git merge converts all commits into a single squash commit")
                ],
                correct_option_id="B",
                explanation="Merge preserves the historical timeline with a merge commit; rebase rewrites commits atop target tip, producing linear history."
            ),
            MCQQuestion(
                id="se_8",
                question="What does the following JavaScript asynchronous code print to the console?",
                code_snippet="console.log('1');\nsetTimeout(() => console.log('2'), 0);\nPromise.resolve().then(() => console.log('3'));\nconsole.log('4');",
                options=[
                    MCQOption(id="A", text="1, 2, 3, 4"),
                    MCQOption(id="B", text="1, 4, 2, 3"),
                    MCQOption(id="C", text="1, 4, 3, 2"),
                    MCQOption(id="D", text="1, 3, 4, 2")
                ],
                correct_option_id="C",
                explanation="Synchronous code runs first (1, 4), then microtasks in Promise queue are drained (3), and finally macrotasks like setTimeout run (2)."
            ),
            MCQQuestion(
                id="se_9",
                question="Which ACID property ensures that transactions execute concurrently without seeing intermediate, uncommitted states of other transactions?",
                options=[
                    MCQOption(id="A", text="Atomicity"),
                    MCQOption(id="B", text="Consistency"),
                    MCQOption(id="C", text="Isolation"),
                    MCQOption(id="D", text="Durability")
                ],
                correct_option_id="C",
                explanation="Isolation determines how transaction integrity is visible to other concurrent users, preventing dirty reads and non-repeatable reads."
            ),
            MCQQuestion(
                id="se_10",
                question="In Redis, what is the default eviction behavior when maxmemory is reached and 'allkeys-lru' policy is set?",
                options=[
                    MCQOption(id="A", text="Throws out-of-memory error on every write"),
                    MCQOption(id="B", text="Evicts least recently used keys among all keys"),
                    MCQOption(id="C", text="Evicts keys with an explicit TTL expiration set only"),
                    MCQOption(id="D", text="Evicts keys randomly")
                ],
                correct_option_id="B",
                explanation="The 'allkeys-lru' policy evicts the least recently used (LRU) keys across the entire keyspace regardless of whether a TTL expiration was configured."
            ),
            MCQQuestion(
                id="se_11",
                question="Which tree traversal algorithm yields keys in strictly non-decreasing ascending order for any valid Binary Search Tree (BST)?",
                options=[
                    MCQOption(id="A", text="Pre-order traversal (Root, Left, Right)"),
                    MCQOption(id="B", text="In-order traversal (Left, Root, Right)"),
                    MCQOption(id="C", text="Post-order traversal (Left, Right, Root)"),
                    MCQOption(id="D", text="Level-order traversal (BFS)")
                ],
                correct_option_id="B",
                explanation="Traversing Left -> Root -> Right (In-order) visits nodes in sorted ascending sequence for any binary search tree."
            ),
            MCQQuestion(
                id="se_12",
                question="What is the auxiliary space complexity of a recursive Depth-First Search (DFS) on a tree of height H?",
                options=[
                    MCQOption(id="A", text="O(1)"),
                    MCQOption(id="B", text="O(H)"),
                    MCQOption(id="C", text="O(N^2)"),
                    MCQOption(id="D", text="O(2^H)")
                ],
                correct_option_id="B",
                explanation="Recursive DFS creates stack frames corresponding to the current traversal path from root to leaf, bounded by the height of the tree H."
            ),
            MCQQuestion(
                id="se_13",
                question="What is the semantic distinction between HTTP status code 401 Unauthorized and 403 Forbidden?",
                options=[
                    MCQOption(id="A", text="401 indicates server failure; 403 indicates invalid query parameters"),
                    MCQOption(id="B", text="401 indicates missing or invalid authentication credentials; 403 indicates identity was recognized but authorization to access resource is denied"),
                    MCQOption(id="C", text="401 is for GET requests; 403 is for POST and PUT requests"),
                    MCQOption(id="D", text="There is no difference in RFC 7231")
                ],
                correct_option_id="B",
                explanation="401 signifies unauthenticated (must log in). 403 signifies forbidden (identity known, but lacking permission)."
            ),
            MCQQuestion(
                id="se_14",
                question="Why are B+ Trees overwhelmingly preferred over B Trees for disk-based relational database indexes?",
                options=[
                    MCQOption(id="A", text="B+ Trees require zero memory locks during write operations"),
                    MCQOption(id="B", text="Leaves are linked sequentially for fast range scans and internal nodes store only keys maximizing fanout"),
                    MCQOption(id="C", text="B Trees do not support binary searching"),
                    MCQOption(id="D", text="B+ Trees have an average lookup time of O(1)")
                ],
                correct_option_id="B",
                explanation="In B+ Trees, non-leaf nodes store only index keys (maximizing fanout per disk page), and all leaf nodes form a contiguous doubly-linked list enabling rapid sequential range scans."
            ),
            MCQQuestion(
                id="se_15",
                question="In distributed microservices, how does the Circuit Breaker pattern behave in the 'Half-Open' state?",
                options=[
                    MCQOption(id="A", text="All incoming requests are immediately dropped"),
                    MCQOption(id="B", text="It permits a limited number of test requests through to evaluate whether downstream service has recovered"),
                    MCQOption(id="C", text="It runs a full database backup before resuming operations"),
                    MCQOption(id="D", text="It duplicates all traffic across two independent data centers")
                ],
                correct_option_id="B",
                explanation="After an open circuit timeout expires, the breaker transitions to Half-Open to allow a trial burst of requests. If they succeed, it closes the circuit."
            ),
            MCQQuestion(
                id="se_16",
                question="According to the CAP Theorem, what fundamental trade-off must a distributed data store make during an unavoidable network partition (P)?",
                options=[
                    MCQOption(id="A", text="Between Performance and Security"),
                    MCQOption(id="B", text="Between Consistency (all nodes see latest data) and Availability (every request receives non-error response)"),
                    MCQOption(id="C", text="Between Latency and Storage throughput"),
                    MCQOption(id="D", text="Between Compression ratio and Encryption depth")
                ],
                correct_option_id="B",
                explanation="When a partition occurs, a distributed system must choose between Consistency (CP) or Availability (AP)."
            ),
            MCQQuestion(
                id="se_17",
                question="What is an architectural security trade-off when using stateless JWT authentication compared to server-side session stores?",
                options=[
                    MCQOption(id="A", text="JWTs cannot be validated without continuous database roundtrips"),
                    MCQOption(id="B", text="JWTs cannot be revoked instantly prior to expiration without maintaining a distributed token revocation blacklist"),
                    MCQOption(id="C", text="JWTs can only be sent over unencrypted HTTP"),
                    MCQOption(id="D", text="JWTs do not support digital signatures")
                ],
                correct_option_id="B",
                explanation="Because JWTs are self-contained and cryptographically verified statelessly, revoking a compromised token before expiration requires introducing a centralized revocation list."
            ),
            MCQQuestion(
                id="se_18",
                question="What is the primary difference between dynamic programming Memoization (top-down) and Tabulation (bottom-up)?",
                options=[
                    MCQOption(id="A", text="Memoization avoids all recursion; Tabulation always uses recursion"),
                    MCQOption(id="B", text="Tabulation iteratively computes and fills a table from base cases up, eliminating recursive call stack overhead"),
                    MCQOption(id="C", text="Tabulation requires exponential memory space"),
                    MCQOption(id="D", text="Memoization is always O(1) time complexity")
                ],
                correct_option_id="B",
                explanation="Tabulation avoids recursion stack overhead by filling subproblems systematically from base cases up."
            ),
            MCQQuestion(
                id="se_19",
                question="In Docker, why is multi-stage building considered an industry best practice for production images?",
                options=[
                    MCQOption(id="A", text="It forces containers to run in rootless mode by default"),
                    MCQOption(id="B", text="It separates build-time dependencies (compilers, SDKs) from runtime artifacts, producing minimal, secure production containers"),
                    MCQOption(id="C", text="It merges all Docker layers into a single uncompressed tarball"),
                    MCQOption(id="D", text="It eliminates the need for container port forwarding")
                ],
                correct_option_id="B",
                explanation="Multi-stage builds leave heavyweight compilers and dev tools behind in temporary build stages, copying only the compiled executable into a slim final runtime base."
            ),
            MCQQuestion(
                id="se_20",
                question="What is the time complexity of building a Binary Heap from an unordered array of N elements using the bottom-up 'heapify' algorithm?",
                options=[
                    MCQOption(id="A", text="O(N log N)"),
                    MCQOption(id="B", text="O(N)"),
                    MCQOption(id="C", text="O(N^2)"),
                    MCQOption(id="D", text="O(1)")
                ],
                correct_option_id="B",
                explanation="Bottom-up heap construction converges to linear O(N) time because sifting down from lower levels requires fewer swaps."
            )
        ]

def get_role_coding_challenges(target_career: str = "Cloud & DevOps Engineer") -> List[CodingChallenge]:
    career = (target_career or "").lower()

    # 1. CLOUD & DEVOPS ENGINEER
    if "devops" in career or "cloud" in career or "infrastructure" in career:
        return [
            CodingChallenge(
                id="code_cdo_01",
                title="Log Parser - HTTP 5xx Error Rate Aggregator",
                difficulty="Medium",
                language="python",
                problem_statement="Given a list of web server log entries where each entry is a string format 'TIMESTAMP STATUS_CODE RESPONSE_TIME_MS' (e.g. '2026-11-19T10:00:00 500 240'), parse the logs and return a tuple (total_requests, error_count, error_percentage_rounded) where error_count represents HTTP 5xx errors (status >= 500 and status <= 599).",
                starter_code="def parse_log_errors(logs: list[str]) -> tuple[int, int, float]:\n    # Implement optimal log parsing\n    total = len(logs)\n    if total == 0:\n        return (0, 0, 0.0)\n    errors = 0\n    for entry in logs:\n        parts = entry.strip().split()\n        if len(parts) >= 2:\n            status = int(parts[1])\n            if 500 <= status <= 599:\n                errors += 1\n    pct = round((errors / total) * 100, 2)\n    return (total, errors, pct)\n",
                sample_input="logs = ['2026-11-19 200 45', '2026-11-19 502 120', '2026-11-19 500 300', '2026-11-19 200 50']",
                sample_output="(4, 2, 50.0)",
                test_cases=[
                    {"input": "['2026-11-19 200 45', '2026-11-19 502 120', '2026-11-19 500 300', '2026-11-19 200 50']", "expected": "(4, 2, 50.0)"},
                    {"input": "['2026-11-19 200 10', '2026-11-19 404 15']", "expected": "(2, 0, 0.0)"}
                ]
            ),
            CodingChallenge(
                id="code_cdo_02",
                title="IPv4 Address & Subnet Octet Validator",
                difficulty="Easy",
                language="python",
                problem_statement="Given an IPv4 address string (e.g., '192.168.1.1'), return True if it is a valid IPv4 address and False otherwise. A valid IPv4 consists of four decimal octets separated by dots, each ranging from 0 to 255 with no leading zeros unless the number is '0'.",
                starter_code="def is_valid_ipv4(ip: str) -> bool:\n    # Implement IPv4 validation\n    parts = ip.split('.')\n    if len(parts) != 4:\n        return False\n    for p in parts:\n        if not p.isdigit() or (len(p) > 1 and p[0] == '0'):\n            return False\n        val = int(p)\n        if val < 0 or val > 255:\n            return False\n    return True\n",
                sample_input="ip = '192.168.1.1'",
                sample_output="True",
                test_cases=[
                    {"input": "'192.168.1.1'", "expected": "True"},
                    {"input": "'256.100.0.1'", "expected": "False"}
                ]
            )
        ]

    # 2. FULL-STACK DEVELOPER
    elif "full" in career or "frontend" in career or "web" in career:
        return [
            CodingChallenge(
                id="code_fsd_01",
                title="URL Query Parameter Parser & Serializer",
                difficulty="Easy",
                language="python",
                problem_statement="Given a URL query string without the leading '?' (e.g. 'role=developer&level=senior&tags=react&tags=python'), parse it into a dictionary where repeated keys map to a list of values, and single keys map to single string values.",
                starter_code="def parse_query_params(query: str) -> dict:\n    # Implement query parameter parser\n    if not query:\n        return {}\n    result = {}\n    pairs = query.split('&')\n    for pair in pairs:\n        if '=' in pair:\n            k, v = pair.split('=', 1)\n            if k in result:\n                if isinstance(result[k], list):\n                    result[k].append(v)\n                else:\n                    result[k] = [result[k], v]\n            else:\n                result[k] = v\n    return result\n",
                sample_input="query = 'name=Rakshita&track=devops&track=fullstack'",
                sample_output="{'name': 'Rakshita', 'track': ['devops', 'fullstack']}",
                test_cases=[
                    {"input": "'name=Rakshita&track=devops&track=fullstack'", "expected": "{'name': 'Rakshita', 'track': ['devops', 'fullstack']}"},
                    {"input": "'page=1&limit=20'", "expected": "{'page': '1', 'limit': '20'}"}
                ]
            ),
            CodingChallenge(
                id="code_fsd_02",
                title="Nested JSON State Flattener",
                difficulty="Medium",
                language="python",
                problem_statement="Given a nested dictionary representing frontend form state or API payloads, flatten it into a single-level dictionary with dot-notation keys (e.g. {'user': {'profile': {'age': 22}}} -> {'user.profile.age': 22}).",
                starter_code="def flatten_json_state(d: dict, parent_key: str = '', sep: str = '.') -> dict:\n    # Implement recursive state flattener\n    items = {}\n    for k, v in d.items():\n        new_key = f\"{parent_key}{sep}{k}\" if parent_key else k\n        if isinstance(v, dict):\n            items.update(flatten_json_state(v, new_key, sep=sep))\n        else:\n            items[new_key] = v\n    return items\n",
                sample_input="d = {'user': {'name': 'Rakshita', 'skills': {'primary': 'React'}}}",
                sample_output="{'user.name': 'Rakshita', 'user.skills.primary': 'React'}",
                test_cases=[
                    {"input": "{'user': {'name': 'Rakshita', 'skills': {'primary': 'React'}}}", "expected": "{'user.name': 'Rakshita', 'user.skills.primary': 'React'}"},
                    {"input": "{'status': 'active'}", "expected": "{'status': 'active'}"}
                ]
            )
        ]

    # 3. AI / ML ENGINEER
    elif "ai" in career or "ml" in career or "machine" in career or "deep" in career:
        return [
            CodingChallenge(
                id="code_aiml_01",
                title="Cosine Similarity & Top-K Vector Matcher",
                difficulty="Medium",
                language="python",
                problem_statement="Given a query vector Q of length D and a list of candidate vectors candidates where each candidate is a tuple (id, vector), compute the cosine similarity between Q and each candidate, returning the top-K candidate IDs sorted by similarity in descending order.",
                starter_code="import math\n\ndef top_k_cosine_similarity(query: list[float], candidates: list[tuple[str, list[float]]], k: int = 1) -> list[str]:\n    # Implement cosine similarity\n    def cosine_sim(v1, v2):\n        dot = sum(a * b for a, b in zip(v1, v2))\n        norm1 = math.sqrt(sum(a * a for a in v1))\n        norm2 = math.sqrt(sum(b * b for b in v2))\n        return dot / (norm1 * norm2) if norm1 and norm2 else 0.0\n\n    scores = [(cid, cosine_sim(query, vec)) for cid, vec in candidates]\n    scores.sort(key=lambda x: x[1], reverse=True)\n    return [cid for cid, _ in scores[:k]]\n",
                sample_input="query = [1.0, 0.0], candidates = [('doc1', [1.0, 0.0]), ('doc2', [0.0, 1.0])], k = 1",
                sample_output="['doc1']",
                test_cases=[
                    {"input": "query = [1.0, 0.0], candidates = [('doc1', [1.0, 0.0]), ('doc2', [0.0, 1.0])], k = 1", "expected": "['doc1']"},
                    {"input": "query = [0.0, 1.0], candidates = [('doc1', [1.0, 0.0]), ('doc2', [0.0, 1.0])], k = 1", "expected": "['doc2']"}
                ]
            ),
            CodingChallenge(
                id="code_aiml_02",
                title="Precision, Recall & F1-Score Metric Evaluator",
                difficulty="Easy",
                language="python",
                problem_statement="Given two lists of equal length representing true binary labels and predicted binary labels (1 or 0), compute and return a tuple of rounded floats (precision, recall, f1_score). Return (0.0, 0.0, 0.0) if denominator is zero.",
                starter_code="def evaluate_classification_metrics(y_true: list[int], y_pred: list[int]) -> tuple[float, float, float]:\n    # Implement precision, recall, f1\n    tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 1)\n    fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 1)\n    fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 0)\n    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0\n    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0\n    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0\n    return (round(precision, 2), round(recall, 2), round(f1, 2))\n",
                sample_input="y_true = [1, 0, 1, 1], y_pred = [1, 0, 1, 0]",
                sample_output="(1.0, 0.67, 0.8)",
                test_cases=[
                    {"input": "y_true = [1, 0, 1, 1], y_pred = [1, 0, 1, 0]", "expected": "(1.0, 0.67, 0.8)"},
                    {"input": "y_true = [1, 1], y_pred = [1, 1]", "expected": "(1.0, 1.0, 1.0)"}
                ]
            )
        ]

    # 4. DATA ANALYST
    elif "analyst" in career or "data" in career:
        return [
            CodingChallenge(
                id="code_da_01",
                title="Running Moving Average Over Window K",
                difficulty="Easy",
                language="python",
                problem_statement="Given a list of numeric transaction amounts and an integer window size K, compute the moving average for each window of length K, returning a list of rounded averages to 2 decimal places.",
                starter_code="def moving_averages(data: list[float], k: int) -> list[float]:\n    # Implement rolling window average\n    if not data or k <= 0 or len(data) < k:\n        return []\n    window_sum = sum(data[:k])\n    result = [round(window_sum / k, 2)]\n    for i in range(k, len(data)):\n        window_sum += data[i] - data[i - k]\n        result.append(round(window_sum / k, 2))\n    return result\n",
                sample_input="data = [10, 20, 30, 40, 50], k = 3",
                sample_output="[20.0, 30.0, 40.0]",
                test_cases=[
                    {"input": "data = [10, 20, 30, 40, 50], k = 3", "expected": "[20.0, 30.0, 40.0]"},
                    {"input": "data = [10, 10, 10], k = 2", "expected": "[10.0, 10.0]"}
                ]
            ),
            CodingChallenge(
                id="code_da_02",
                title="Categorical Group-By & Metrics Summary Aggregator",
                difficulty="Medium",
                language="python",
                problem_statement="Given a list of dictionary sales records [{'category': 'Tech', 'amount': 150.0}, ...], compute the total count and total amount per category, returning a dictionary mapping category to {'count': int, 'total': float}.",
                starter_code="def aggregate_sales_by_category(records: list[dict]) -> dict:\n    # Implement aggregation\n    summary = {}\n    for r in records:\n        cat = r.get('category', 'Unknown')\n        amt = float(r.get('amount', 0.0))\n        if cat not in summary:\n            summary[cat] = {'count': 0, 'total': 0.0}\n        summary[cat]['count'] += 1\n        summary[cat]['total'] = round(summary[cat]['total'] + amt, 2)\n    return summary\n",
                sample_input="records = [{'category': 'Cloud', 'amount': 200}, {'category': 'Cloud', 'amount': 300}]",
                sample_output="{'Cloud': {'count': 2, 'total': 500.0}}",
                test_cases=[
                    {"input": "[{'category': 'Cloud', 'amount': 200}, {'category': 'Cloud', 'amount': 300}]", "expected": "{'Cloud': {'count': 2, 'total': 500.0}}"},
                    {"input": "[]", "expected": "{}"}
                ]
            )
        ]

    # 5. DEFAULT / SOFTWARE ENGINEER / BACKEND
    else:
        return [
            CodingChallenge(
                id="code_se_01",
                title="Two Sum (Sorted Array) - Two Pointer Scan",
                difficulty="Medium",
                language="python",
                problem_statement="Given a 1-indexed sorted array of integers numbers and a target sum, find two distinct indices [i, j] such that numbers[i] + numbers[j] == target. Implement an optimal O(N) time and O(1) auxiliary space solution.",
                starter_code="def two_sum_sorted(numbers: list[int], target: int) -> list[int]:\n    # Implement optimal two pointer scan\n    left = 0\n    right = len(numbers) - 1\n    while left < right:\n        current_sum = numbers[left] + numbers[right]\n        if current_sum == target:\n            return [left + 1, right + 1]\n        elif current_sum < target:\n            left += 1\n        else:\n            right -= 1\n    return []\n",
                sample_input="numbers = [2, 7, 11, 15], target = 9",
                sample_output="[1, 2]",
                test_cases=[
                    {"input": "[2, 7, 11, 15], target = 9", "expected": "[1, 2]"},
                    {"input": "[2, 3, 4], target = 6", "expected": "[1, 3]"}
                ]
            ),
            CodingChallenge(
                id="code_se_02",
                title="Valid Parentheses - Stack Balance Validator",
                difficulty="Easy",
                language="python",
                problem_statement="Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid. An input string is valid if open brackets are closed by the same type of brackets in the correct order. Implement in O(N) time and O(N) space using a Stack.",
                starter_code="def is_valid_parentheses(s: str) -> bool:\n    # Implement stack validator\n    stack = []\n    mapping = {')': '(', '}': '{', ']': '['}\n    for char in s:\n        if char in mapping:\n            top_elem = stack.pop() if stack else '#'\n            if mapping[char] != top_elem:\n                return False\n        else:\n            stack.append(char)\n    return not stack\n",
                sample_input="s = '()[]{}'",
                sample_output="True",
                test_cases=[
                    {"input": "'()[]{}'", "expected": "True"},
                    {"input": "'([)]'", "expected": "False"}
                ]
            )
        ]
