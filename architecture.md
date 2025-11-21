# AI DevSecOps Pipeline Orchestrator
## Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                 AI DevSecOps Pipeline Orchestrator              │
│                         (Python Application)                     │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
        ┌──────────────┐ ┌──────────┐ ┌──────────────┐
        │  MCP Client  │ │  OpenAI  │ │ E2B Sandboxes│
        │   (stdio)    │ │   API    │ │     API      │
        └──────────────┘ └──────────┘ └──────────────┘
                │
                ▼
        ┌──────────────┐
        │ Docker MCP   │
        │   Gateway    │
        └──────────────┘
                │
        ┌───────┼────────┐
        │       │        │
        ▼       ▼        ▼
    ┌────┐  ┌────┐  ┌────────┐
    │ GH │  │ SL │  │  PW    │
    │MCP │  │MCP │  │  MCP   │
    └────┘  └────┘  └────────┘
```

## Component Architecture

### Layer 1: Orchestration Layer
**Location**: `src/core/orchestrator.py`

Coordinates the entire pipeline:
- Workflow management
- Component integration
- Error handling
- Result aggregation

### Layer 2: Integration Layer

#### MCP Client (`src/mcp/`)
- **client.py**: Base MCP client
- **github.py**: GitHub operations
- **slack.py**: Slack notifications

#### AI Services (`src/patch/`)
- **generator.py**: OpenAI integration
- Patch generation
- Test script creation

#### Sandbox Services (`src/sandbox/`)
- **manager.py**: E2B management
- Test execution
- Result capture

### Layer 3: Business Logic

#### Vulnerability Detection (`src/vulnerability/`)
- **scanner.py**: Dependency scanning
- CVE detection
- Risk prioritization

### Layer 4: Infrastructure

#### Configuration (`src/core/`)
- **config.py**: Environment management
- Settings validation

#### Utilities (`src/utils/`)
- **logger.py**: Logging setup
- Rich formatting

## Data Flow

### 1. Vulnerability Detection Flow
```
Repository → GitHub MCP → requirements.txt → Scanner → Vulnerabilities
```

### 2. Patch Generation Flow
```
Vulnerabilities → OpenAI API → Patches → Validation
```

### 3. Testing Flow
```
Patches → E2B Sandbox → Install → Test → Results
```

### 4. Notification Flow
```
Results → Slack MCP → Team Notification
```

## Technology Stack

### Core Technologies
- **Python 3.10+**: Main language
- **MCP SDK**: Model Context Protocol
- **E2B**: Secure sandboxes
- **OpenAI**: AI patch generation

### MCP Servers (Docker)
- **github-official**: Repository operations
- **slack**: Team notifications
- **playwright**: Browser automation

### Supporting Libraries
- **pydantic**: Data validation
- **click**: CLI framework
- **rich**: Terminal UI
- **aiohttp**: Async HTTP

## Security Architecture

### Isolation Layers
1. **E2B Sandboxes**: Complete isolation for code execution
2. **Docker Containers**: MCP servers in containers
3. **API Keys**: Secure credential management
4. **OAuth**: GitHub authentication

### Data Protection
- API keys in environment variables
- No hardcoded credentials
- Secure communication channels
- Audit logging

## Scalability Considerations

### Parallel Processing
- Multiple E2B sandboxes simultaneously
- Async operations throughout
- Non-blocking I/O

### Resource Management
- Sandbox lifecycle management
- Connection pooling
- Automatic cleanup

## Error Handling

### Levels
1. **Component Level**: Try/catch in each module
2. **Integration Level**: Graceful degradation
3. **Pipeline Level**: Rollback and recovery
4. **User Level**: Clear error messages

### Logging
- Rich formatted output
- Severity levels
- Contextual information
- Debug mode support Documentation

### High-Level Architecture Diagram

```mermaid
graph TB
    subgraph "External Systems"
        GH[GitHub Repositories]
        CVE[CVE Databases]
        SLACK[Slack Workspace]
        NOTION[Notion Workspace]
    end

    subgraph "Docker MCP Gateway"
        GATEWAY[MCP Gateway<br/>Port: 3000]
        
        subgraph "MCP Servers"
            MCP_GH[GitHub MCP Server]
            MCP_PG[PostgreSQL MCP Server]
            MCP_SLACK[Slack MCP Server]
            MCP_BROWSER[Browserbase MCP Server]
            MCP_NOTION[Notion MCP Server]
        end
    end

    subgraph "AI Orchestration Layer"
        AGENT[AI Agent Controller<br/>Claude/GPT-4]
        VULN[Vulnerability Detector]
        PATCH[Patch Generator]
        VALIDATOR[Validation Engine]
        DEPLOY[Deployment Manager]
    end

    subgraph "E2B Sandbox Environment"
        SANDBOX_MGR[Sandbox Manager]
        
        subgraph "Isolated Sandboxes"
            SB1[Patch Test Sandbox 1]
            SB2[Patch Test Sandbox 2]
            SB3[Security Test Sandbox]
            SBN[... Sandbox N]
        end
    end

    subgraph "Data Layer"
        DB[(Vulnerability DB<br/>Patch History<br/>Audit Logs)]
        CACHE[Redis Cache]
        S3[Artifact Storage]
    end

    GH --> MCP_GH
    CVE --> VULN
    SLACK <--> MCP_SLACK
    NOTION <--> MCP_NOTION

    GATEWAY --> MCP_GH
    GATEWAY --> MCP_PG
    GATEWAY --> MCP_SLACK
    GATEWAY --> MCP_BROWSER
    GATEWAY --> MCP_NOTION

    AGENT --> GATEWAY
    AGENT --> VULN
    AGENT --> PATCH
    AGENT --> VALIDATOR
    AGENT --> DEPLOY

    VULN --> DB
    PATCH --> SANDBOX_MGR
    VALIDATOR --> SANDBOX_MGR

    SANDBOX_MGR --> SB1
    SANDBOX_MGR --> SB2
    SANDBOX_MGR --> SB3
    SANDBOX_MGR --> SBN

    MCP_PG --> DB
    VALIDATOR --> CACHE
    DEPLOY --> S3

    style GATEWAY fill:#e1f5fe
    style AGENT fill:#fff3e0
    style SANDBOX_MGR fill:#e8f5e9
    style DB fill:#f3e5f5
```

### Low-Level Architecture Diagram

```mermaid
graph TB
    subgraph "Client Layer"
        UI[Web Dashboard<br/>React + TypeScript]
        CLI[CLI Tool<br/>Node.js]
        API_CLIENT[API Client SDK]
    end

    subgraph "API Gateway"
        NGINX[Nginx<br/>Rate Limiting]
        AUTH[Auth Service<br/>OAuth 2.0]
        WEBHOOK[Webhook Handler]
    end

    subgraph "Core Services"
        subgraph "Vulnerability Service"
            SCANNER[Code Scanner<br/>Semgrep/Snyk]
            CVE_MON[CVE Monitor]
            DEP_CHECK[Dependency Checker]
        end

        subgraph "Patch Service"
            STRATEGY[Strategy Engine]
            CODE_GEN[Code Generator<br/>AST Manipulation]
            TEMPLATE[Patch Templates]
        end

        subgraph "Validation Service"
            TEST_RUNNER[Test Runner]
            SEC_TEST[Security Tests]
            PERF_TEST[Performance Tests]
        end

        subgraph "Deployment Service"
            ROLLOUT[Rollout Manager]
            CANARY[Canary Controller]
            ROLLBACK[Rollback Engine]
        end
    end

    subgraph "MCP Integration Layer"
        MCP_CLIENT[MCP Client<br/>@modelcontextprotocol/sdk]
        TRANSPORT[HTTP Transport]
        
        subgraph "Server Connections"
            GH_CONN[GitHub Connection]
            PG_CONN[PostgreSQL Connection]
            SLACK_CONN[Slack Connection]
            BROWSER_CONN[Browser Connection]
        end
    end

    subgraph "E2B Integration"
        E2B_SDK[E2B SDK<br/>@e2b/code-interpreter]
        
        subgraph "Sandbox Operations"
            CREATE[Sandbox Creation]
            EXEC[Code Execution]
            MONITOR[Resource Monitor]
            CLEANUP[Cleanup Manager]
        end
    end

    subgraph "Infrastructure"
        QUEUE[Message Queue<br/>RabbitMQ]
        WORKER[Worker Pool<br/>Bull.js]
        METRICS[Metrics<br/>Prometheus]
        LOGS[Logging<br/>ELK Stack]
    end

    UI --> NGINX
    CLI --> NGINX
    API_CLIENT --> NGINX

    NGINX --> AUTH
    NGINX --> WEBHOOK
    AUTH --> SCANNER
    AUTH --> STRATEGY
    AUTH --> TEST_RUNNER
    AUTH --> ROLLOUT

    SCANNER --> CVE_MON
    SCANNER --> DEP_CHECK
    STRATEGY --> CODE_GEN
    STRATEGY --> TEMPLATE
    TEST_RUNNER --> SEC_TEST
    TEST_RUNNER --> PERF_TEST
    ROLLOUT --> CANARY
    ROLLOUT --> ROLLBACK

    MCP_CLIENT --> TRANSPORT
    TRANSPORT --> GH_CONN
    TRANSPORT --> PG_CONN
    TRANSPORT --> SLACK_CONN
    TRANSPORT --> BROWSER_CONN

    E2B_SDK --> CREATE
    E2B_SDK --> EXEC
    E2B_SDK --> MONITOR
    E2B_SDK --> CLEANUP

    TEST_RUNNER --> E2B_SDK
    CODE_GEN --> E2B_SDK

    SCANNER --> QUEUE
    QUEUE --> WORKER
    WORKER --> E2B_SDK

    style E2B_SDK fill:#e8f5e9
    style MCP_CLIENT fill:#e1f5fe
    style AUTH fill:#ffe0b2
```

### Data Flow Diagram

```mermaid
sequenceDiagram
    participant User
    participant GitHub
    participant MCP Gateway
    participant AI Agent
    participant Vuln Detector
    participant Patch Gen
    participant E2B Sandbox
    participant Validator
    participant Database
    participant Slack

    User->>GitHub: Push Code
    GitHub->>MCP Gateway: Webhook Event
    MCP Gateway->>AI Agent: Trigger Analysis
    
    AI Agent->>Vuln Detector: Scan Repository
    Vuln Detector->>MCP Gateway: Query GitHub MCP
    MCP Gateway->>GitHub: Fetch Code
    GitHub-->>MCP Gateway: Return Code
    MCP Gateway-->>Vuln Detector: Code Data
    
    Vuln Detector->>Database: Check CVE Database
    Database-->>Vuln Detector: Known Vulnerabilities
    Vuln Detector-->>AI Agent: Vulnerability Report
    
    AI Agent->>Patch Gen: Generate Patches
    Patch Gen->>AI Agent: Multiple Patch Strategies
    
    loop For Each Patch Strategy
        AI Agent->>E2B Sandbox: Create Sandbox
        E2B Sandbox-->>AI Agent: Sandbox ID
        
        AI Agent->>E2B Sandbox: Deploy Code + Patch
        E2B Sandbox->>E2B Sandbox: Apply Patch
        
        AI Agent->>Validator: Run Tests
        Validator->>E2B Sandbox: Execute Test Suite
        E2B Sandbox-->>Validator: Test Results
        
        Validator->>E2B Sandbox: Security Scan
        E2B Sandbox-->>Validator: Security Report
        
        Validator->>Database: Store Results
        Validator-->>AI Agent: Validation Report
        
        AI Agent->>E2B Sandbox: Cleanup
    end
    
    AI Agent->>AI Agent: Select Best Patch
    AI Agent->>MCP Gateway: Create PR via GitHub MCP
    MCP Gateway->>GitHub: Open Pull Request
    
    AI Agent->>MCP Gateway: Send Notification
    MCP Gateway->>Slack: Patch Ready for Review
    
    Slack-->>User: Notification
    User->>GitHub: Review & Approve PR
    
    GitHub->>MCP Gateway: PR Approved
    MCP Gateway->>AI Agent: Deploy Signal
    AI Agent->>E2B Sandbox: Final Validation
    E2B Sandbox-->>AI Agent: Success
    
    AI Agent->>GitHub: Merge PR
    AI Agent->>Database: Update Audit Log
    AI Agent->>Slack: Deployment Complete
```

### Component Interaction Diagram

```mermaid
graph LR
    subgraph "Input Sources"
        CODE[Source Code]
        SEC_ADV[Security Advisories]
        DEPS[Dependencies]
    end

    subgraph "Detection Phase"
        STATIC[Static Analysis]
        DYNAMIC[Dynamic Analysis]
        SBOM[SBOM Analysis]
    end

    subgraph "Generation Phase"
        AST[AST Parser]
        TEMPLATES[Fix Templates]
        AI_GEN[AI Generation]
    end

    subgraph "Validation Phase"
        UNIT[Unit Tests]
        INTEGRATION[Integration Tests]
        SECURITY[Security Tests]
        PERFORMANCE[Performance Tests]
    end

    subgraph "Deployment Phase"
        STAGING[Staging Deploy]
        CANARY_D[Canary Deploy]
        PROD[Production Deploy]
    end

    CODE --> STATIC
    SEC_ADV --> DYNAMIC
    DEPS --> SBOM

    STATIC --> AST
    DYNAMIC --> AI_GEN
    SBOM --> TEMPLATES

    AST --> UNIT
    TEMPLATES --> INTEGRATION
    AI_GEN --> SECURITY

    UNIT --> STAGING
    INTEGRATION --> STAGING
    SECURITY --> CANARY_D
    PERFORMANCE --> CANARY_D

    STAGING --> PROD
    CANARY_D --> PROD

    style STATIC fill:#ffebee
    style AI_GEN fill:#e8f5e9
    style SECURITY fill:#fff3e0
```

### E2B Sandbox Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Idle: System Ready
    
    Idle --> Creating: Vulnerability Detected
    Creating --> Provisioning: Request Sandbox
    Provisioning --> Ready: Sandbox Allocated
    
    Ready --> Deploying: Deploy Code
    Deploying --> Testing: Run Tests
    Testing --> Analyzing: Collect Metrics
    
    Analyzing --> Success: Tests Pass
    Analyzing --> Failed: Tests Fail
    
    Success --> Reporting: Generate Report
    Failed --> Reporting: Generate Report
    
    Reporting --> Cleaning: Store Results
    Cleaning --> Destroyed: Release Resources
    
    Destroyed --> Idle: Ready for Next
    
    Testing --> Error: Timeout/Crash
    Error --> Cleaning: Force Cleanup
```

### Security Architecture

```mermaid
graph TB
    subgraph "Security Layers"
        subgraph "Network Security"
            FW[Firewall Rules]
            VPN[VPN Access]
            TLS[TLS Encryption]
        end

        subgraph "Authentication"
            OAuth[OAuth 2.0]
            MFA[Multi-Factor Auth]
            RBAC[Role-Based Access]
        end

        subgraph "Isolation"
            E2B_ISO[E2B Sandbox Isolation]
            DOCKER_ISO[Docker Container Isolation]
            NET_ISO[Network Segmentation]
        end

        subgraph "Data Security"
            ENCRYPT[Encryption at Rest]
            HASH[Secret Hashing]
            VAULT[Secret Management]
        end

        subgraph "Audit & Compliance"
            AUDIT_LOG[Audit Logging]
            COMPLIANCE[Compliance Reports]
            MONITOR_SEC[Security Monitoring]
        end
    end

    FW --> VPN
    VPN --> TLS
    OAuth --> MFA
    MFA --> RBAC
    E2B_ISO --> DOCKER_ISO
    DOCKER_ISO --> NET_ISO
    ENCRYPT --> HASH
    HASH --> VAULT
    AUDIT_LOG --> COMPLIANCE
    COMPLIANCE --> MONITOR_SEC

    style E2B_ISO fill:#e8f5e9
    style OAuth fill:#e1f5fe
    style AUDIT_LOG fill:#fff3e0
```

### Scalability Design

```mermaid
graph TB
    subgraph "Load Balancing"
        LB[Load Balancer]
        API1[API Server 1]
        API2[API Server 2]
        APIN[API Server N]
    end

    subgraph "Queue System"
        QUEUE_MGR[Queue Manager]
        Q1[High Priority Queue]
        Q2[Normal Queue]
        Q3[Low Priority Queue]
    end

    subgraph "Worker Pool"
        WORKER_MGR[Worker Manager]
        W1[Worker 1]
        W2[Worker 2]
        WN[Worker N]
    end

    subgraph "E2B Sandbox Pool"
        POOL_MGR[Pool Manager]
        subgraph "Available"
            SB_A1[Sandbox]
            SB_A2[Sandbox]
        end
        subgraph "In Use"
            SB_U1[Sandbox]
            SB_U2[Sandbox]
        end
        subgraph "Reserved"
            SB_R1[Sandbox]
            SB_R2[Sandbox]
        end
    end

    LB --> API1
    LB --> API2
    LB --> APIN

    API1 --> QUEUE_MGR
    API2 --> QUEUE_MGR
    APIN --> QUEUE_MGR

    QUEUE_MGR --> Q1
    QUEUE_MGR --> Q2
    QUEUE_MGR --> Q3

    Q1 --> WORKER_MGR
    Q2 --> WORKER_MGR
    Q3 --> WORKER_MGR

    WORKER_MGR --> W1
    WORKER_MGR --> W2
    WORKER_MGR --> WN

    W1 --> POOL_MGR
    W2 --> POOL_MGR
    WN --> POOL_MGR

    POOL_MGR --> SB_A1
    POOL_MGR --> SB_U1
    POOL_MGR --> SB_R1

    style POOL_MGR fill:#e8f5e9
    style QUEUE_MGR fill:#e1f5fe
```

## Technical Stack

### Core Technologies
- **Runtime**: Node.js 20.x with TypeScript
- **AI Models**: Claude 3.5 Sonnet / GPT-4
- **Framework**: Express.js / Fastify
- **Database**: PostgreSQL 15 + Redis
- **Message Queue**: RabbitMQ / Bull.js

### MCP Integration
- **MCP SDK**: @modelcontextprotocol/sdk
- **Transport**: HTTP/STDIO
- **Docker CLI**: docker mcp command suite

### E2B Integration
- **SDK**: @e2b/code-interpreter
- **Sandboxes**: Ubuntu 22.04 isolated environments
- **Resource Limits**: 1 CPU, 2GB RAM per sandbox

### Security Tools
- **SAST**: Semgrep, SonarQube
- **Dependency Scanning**: Snyk, OWASP Dependency Check
- **Container Scanning**: Trivy, Clair

### Monitoring & Observability
- **Metrics**: Prometheus + Grafana
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **Tracing**: OpenTelemetry + Jaeger
- **Alerting**: PagerDuty / Opsgenie

## Deployment Architecture

### Container Structure
```yaml
services:
  api-gateway:
    image: nginx:alpine
    ports: ["80:80", "443:443"]
  
  orchestrator:
    image: devsecops-orchestrator:latest
    environment:
      - E2B_API_KEY=${E2B_API_KEY}
  
  mcp-gateway:
    image: docker:mcp-gateway
    ports: ["3000:3000"]
  
  postgres:
    image: postgres:15
    volumes: ["./data:/var/lib/postgresql/data"]
  
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: devsecops-orchestrator
spec:
  replicas: 3
  selector:
    matchLabels:
      app: orchestrator
  template:
    metadata:
      labels:
        app: orchestrator
    spec:
      containers:
      - name: orchestrator
        image: devsecops-orchestrator:latest
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
```

## Performance Considerations

### Optimization Strategies
1. **Sandbox Pooling**: Pre-warm sandboxes for instant availability
2. **Parallel Processing**: Test multiple patches simultaneously
3. **Caching**: Cache vulnerability data and test results
4. **Async Operations**: Non-blocking I/O for all external calls
5. **Resource Limits**: Enforce strict limits on sandbox resources

### Benchmarks
- **Sandbox Creation**: < 2 seconds
- **Patch Generation**: < 10 seconds
- **Test Execution**: < 5 minutes (average)
- **Full Pipeline**: < 15 minutes end-to-end

## Disaster Recovery

### Backup Strategy
- **Database**: Daily snapshots with 30-day retention
- **Artifacts**: S3 versioning with lifecycle policies
- **Configuration**: Git-based config management

### Failover Plan
- **Multi-region**: Deploy across 3+ regions
- **Auto-failover**: Health checks trigger automatic failover
- **Data Replication**: Real-time replication to standby regions