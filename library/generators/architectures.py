"""
library/generators/architectures.py - 35 System Architecture & Topology Flowcards.
Renders deterministic diagrams with nodes, bus interconnects, data flow arrows,
and protocol tags.
"""

import html
from typing import Dict, List, Any
from library.engine.svg_builder import SVGBuilder
from library.engine.geometry import circuit_trace_path

ARCHITECTURE_PRESETS: List[Dict[str, Any]] = [
    {"id": "fastmcp-agent-topology", "title": "FastMCP AI Agent Mesh", "theme": "kemet_nocturne", "nodes": ["Client Host", "MCP Router", "Tool Server", "Vector DB"]},
    {"id": "microservices-service-mesh", "title": "Istio Envoy Service Mesh", "theme": "tokyo_night", "nodes": ["API Gateway", "Auth Svc", "Order Svc", "Payment Svc"]},
    {"id": "raft-consensus-cluster", "title": "Raft Distributed Consensus", "theme": "nord_frost", "nodes": ["Leader (Node 1)", "Follower 2", "Follower 3", "WAL Log"]},
    {"id": "kafka-event-stream-pipeline", "title": "Kafka Event Bus Pipeline", "theme": "monokai_pro", "nodes": ["Producers", "Kafka Broker", "Schema Reg", "Consumer Lag"]},
    {"id": "nix-store-derivation-dag", "title": "Nix Store Derivation Graph", "theme": "nord_frost", "nodes": ["flake.nix", "drv Parser", "/nix/store", "Closure"]},
    {"id": "kubernetes-ingress-controller", "title": "K8s Ingress & Pod Replica", "theme": "dracula", "nodes": ["TLS Ingress", "ClusterIP", "Pod Replica 1", "Pod Replica 2"]},
    {"id": "hexagonal-clean-architecture", "title": "Hexagonal Ports & Adapters", "theme": "solarized_dark", "nodes": ["Primary Port", "Domain Core", "Secondary Port", "DB Adapter"]},
    {"id": "event-driven-cqrs-es", "title": "CQRS & Event Sourcing Store", "theme": "cyberpunk_2077", "nodes": ["Command Bus", "Event Store", "Projection Engine", "Read Model"]},
    {"id": "zero-trust-auth-guard", "title": "Zero-Trust Session Guard", "theme": "kemet_nocturne", "nodes": ["Edge Middleware", "Token Verifier", "RBAC Policy", "Downstream"]},
    {"id": "graphql-federation-mesh", "title": "Apollo Federation Supergraph", "theme": "dracula", "nodes": ["Apollo Router", "Users Subgraph", "Billing Subgraph", "Catalog Subgraph"]},
    
    {"id": "redis-cluster-sharding", "title": "Redis Cluster Slot Hash", "theme": "amber_crt", "nodes": ["Client Shard", "Master Slot A", "Master Slot B", "Replica Sync"]},
    {"id": "postgresql-wal-replication", "title": "PostgreSQL Streaming WAL", "theme": "solarized_dark", "nodes": ["Primary Instance", "WAL Sender", "WAL Receiver", "Standby Replica"]},
    {"id": "distributed-tracing-jaeger", "title": "OpenTelemetry Trace Span", "theme": "tokyo_night", "nodes": ["OTel Collector", "Trace Span Root", "Child Span A", "Jaeger UI"]},
    {"id": "websocket-realtime-pubsub", "title": "WebSockets Realtime Engine", "theme": "emerald_matrix", "nodes": ["WSS Handshake", "Socket Worker", "Redis Pub/Sub", "State Broadcast"]},
    {"id": "lambda-serverless-pipeline", "title": "Event-Driven Serverless Flow", "theme": "amber_crt", "nodes": ["S3 Event", "Lambda Exec", "DynamoDB Put", "SNS Notice"]},
    {"id": "ci-cd-github-actions-pipeline", "title": "Hermetic CI/CD Build Matrix", "theme": "nord_frost", "nodes": ["Push Event", "Linter / Test", "Docker Build", "Deploy Registry"]},
    {"id": "rag-vector-search-flow", "title": "RAG Embedding & Retrieval", "theme": "cyberpunk_2077", "nodes": ["User Prompt", "Embedding Model", "HNSW Index", "Context Injection"]},
    {"id": "neural-llm-inference-pipeline", "title": "PagedAttention vLLM Serving", "theme": "monokai_pro", "nodes": ["K/V Cache", "Tensor Parallel", "Model Weights", "Token Stream"]},
    {"id": "multi-tenant-isolation-tier", "title": "Multi-Tenant Row Level DB", "theme": "rose_pine", "nodes": ["Tenant Gateway", "Tenant Claim", "RLS Filter", "Isolated View"]},
    {"id": "p2p-libp2p-dht-network", "title": "libp2p Kademlia DHT Net", "theme": "emerald_matrix", "nodes": ["Bootstrap Node", "Routing Table", "K-Bucket", "Peer Content"]},
    
    {"id": "edge-cdn-caching-layer", "title": "Edge Anycast Stale-While-Reval", "theme": "solarized_dark", "nodes": ["Client Request", "Edge POP Cache", "Cache Shield", "Origin Server"]},
    {"id": "oauth2-oidc-pkce-flow", "title": "OAuth 2.1 PKCE Auth State", "theme": "kemet_nocturne", "nodes": ["Code Challenge", "Auth Server", "Token Exchange", "JWKS Verify"]},
    {"id": "saga-distributed-transactions", "title": "Temporal Orchestrated Saga", "theme": "tokyo_night", "nodes": ["Workflow Initiator", "Step 1: Reserve", "Step 2: Charge", "Compensate Action"]},
    {"id": "outbox-pattern-broker", "title": "Transactional Outbox Pattern", "theme": "dracula", "nodes": ["ACID Commit", "Outbox Table", "Debezium CDC", "Message Broker"]},
    {"id": "circuit-breaker-resilience", "title": "Resilience4j State Machine", "theme": "amber_crt", "nodes": ["Closed (Normal)", "Trip Threshold", "Open (Fast Fail)", "Half-Open Test"]},
    {"id": "api-gateway-rate-limiter", "title": "Token Bucket Rate Limiter", "theme": "cyberpunk_2077", "nodes": ["Incoming Burst", "Token Refill", "Leaky Bucket", "200 / 429 Resp"]},
    {"id": "lakehouse-iceberg-catalog", "title": "Apache Iceberg Lakehouse", "theme": "nord_frost", "nodes": ["Metadata Tree", "Manifest List", "Parquet Data", "Snapshot Log"]},
    {"id": "observability-prometheus-grafana", "title": "Prometheus Scraping Target", "theme": "amber_crt", "nodes": ["Metric Exporter", "Prometheus Pull", "Alertmanager", "Grafana Panel"]},
    {"id": "etcd-key-value-quorum", "title": "etcd B+Tree Quorum Engine", "theme": "monokai_pro", "nodes": ["Quorum Read", "bbolt Engine", "MVCC Revision", "Watch Event"]},
    {"id": "nextjs-app-router-rsc-flow", "title": "Next.js RSC Wire Protocol", "theme": "kemet_nocturne", "nodes": ["Server Component", "Flight Stream", "Client Hydration", "DOM Diff"]},
    
    {"id": "embedded-sqlite-vfs-layer", "title": "SQLite WAL & VFS Subsystem", "theme": "solarized_dark", "nodes": ["B-Tree Engine", "Pager Module", "WAL Frame", "OS Virtual FS"]},
    {"id": "secure-enclave-crypto-kms", "title": "AWS Nitro Enclave KMS", "theme": "nord_frost", "nodes": ["Attestation Doc", "KMS Root Key", "Enclave Memory", "Cipher Output"]},
    {"id": "dns-anycast-routing-tree", "title": "BGP Anycast Geo-DNS Tree", "theme": "rose_pine", "nodes": ["User Resolver", "BGP Path Select", "Regional Node", "Authoritative NS"]},
    {"id": "webrtc-peer-mesh-signaling", "title": "WebRTC ICE & DTLS-SRTP Mesh", "theme": "tokyo_night", "nodes": ["Signaling WS", "STUN / TURN", "ICE Candidate", "P2P DataChannel"]},
    {"id": "kemet-deterministic-engine", "title": "Kemet Deterministic Core", "theme": "kemet_nocturne", "nodes": ["CLI Command", "Seeded RNG", "Pure SVG Emitter", "Zero-Drift Git"]},
]

def generate_architecture_svg(preset_id: str, theme_override: str = None) -> str:
    preset = next((p for p in ARCHITECTURE_PRESETS if p["id"] == preset_id), ARCHITECTURE_PRESETS[0])
    theme = theme_override or preset["theme"]
    title = preset["title"]
    nodes = preset["nodes"]
    
    w, h = 820, 280
    builder = SVGBuilder(w, h, theme, title=f"{title} - Topology Card", desc=f"Architecture flow {preset_id}")
    
    builder.add_custom_css("""
      .card-canvas { fill: var(--vf-card); stroke: var(--vf-border); stroke-width: 1; }
      .blueprint-grid { stroke: var(--vf-border); stroke-width: 0.5; opacity: 0.35; stroke-dasharray: 2 4; }
      .node-box { fill: var(--vf-bg); stroke: var(--vf-border); stroke-width: 1.5; }
      .node-title { font-family: var(--vf-font-mono); font-size: 11px; font-weight: 700; fill: var(--vf-text); }
      .node-sub { font-family: var(--vf-font-mono); font-size: 9.5px; fill: var(--vf-text-muted); }
      .bus-wire { stroke: var(--vf-accent-2); stroke-width: 1.8; fill: none; stroke-dasharray: 4 2; }
      .header-title { font-family: var(--vf-font-sans); font-size: 16px; font-weight: 800; fill: var(--vf-text); }
      .header-meta { font-family: var(--vf-font-mono); font-size: 11px; fill: var(--vf-text-muted); }
      .port-dot { fill: var(--vf-accent-1); }
    """)
    
    # Outer frame
    builder.add_body(f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="8" class="card-canvas" />')
    
    # Blueprint grid
    for gx in range(40, w, 40):
        builder.add_body(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{h}" class="blueprint-grid" />')
    for gy in range(40, h, 40):
        builder.add_body(f'<line x1="0" y1="{gy}" x2="{w}" y2="{gy}" class="blueprint-grid" />')
        
    escaped_title = html.escape(title.upper())
    # Top banner header
    builder.add_body(f"""
    <g transform="translate(32, 28)">
      <rect x="0" y="-8" width="16" height="16" rx="3" fill="var(--vf-accent-1)" />
      <text x="26" y="6" class="header-title">{escaped_title}</text>
      <text x="26" y="24" class="header-meta">TOPOLOGY // LATENCY: &lt; 2.4ms • STATUS: DETERMINISTIC ONLINE</text>
    </g>
    """)
    
    # Node coordinates
    node_w, node_h = 150, 72
    y_node = 110
    total_nodes = len(nodes)
    spacing = (w - 64 - (total_nodes * node_w)) / max(1, (total_nodes - 1))
    
    node_coords = []
    for i, name in enumerate(nodes):
        x = 32 + i * (node_w + spacing)
        node_coords.append((x, y_node, html.escape(name)))
        
    # Draw interconnect wires
    wires = []
    for i in range(len(node_coords) - 1):
        x1 = node_coords[i][0] + node_w
        y1 = y_node + node_h / 2
        x2 = node_coords[i+1][0]
        y2 = y1
        wires.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="bus-wire" />')
        # Flow packet
        wires.append(f'<circle cx="{(x1+x2)/2}" cy="{y1}" r="3" fill="var(--vf-accent-1)" />')
    builder.add_body(f'<g class="interconnects">{"".join(wires)}</g>')
    
    # Draw Nodes
    node_boxes = []
    for idx, (nx, ny, nname) in enumerate(node_coords):
        node_boxes.append(f"""
        <g transform="translate({nx}, {ny})">
          <rect x="0" y="0" width="{node_w}" height="{node_h}" rx="6" class="node-box" />
          <circle cx="12" cy="16" r="3" class="port-dot" />
          <text x="22" y="19" class="node-title">NODE_0{idx+1}</text>
          <text x="12" y="42" font-family="var(--vf-font-sans)" font-size="12px" font-weight="600" fill="var(--vf-text)">{nname}</text>
          <text x="12" y="58" class="node-sub">gRPC / JSON-RPC</text>
          
          <!-- Port connectors -->
          <circle cx="0" cy="{node_h/2}" r="3" fill="var(--vf-accent-2)" />
          <circle cx="{node_w}" cy="{node_h/2}" r="3" fill="var(--vf-accent-2)" />
        </g>
        """)
    builder.add_body(f'<g class="nodes-layer">{"".join(node_boxes)}</g>')
    
    # Bottom Telemetry Ledger Bar
    builder.add_body(f"""
    <g transform="translate(32, 230)">
      <rect x="0" y="0" width="{w-64}" height="28" rx="4" fill="var(--vf-bg)" stroke="var(--vf-border)" />
      <circle cx="16" cy="14" r="3.5" fill="var(--vf-accent-3)" />
      <text x="30" y="18" font-family="var(--vf-font-mono)" font-size="10.5" fill="var(--vf-text-muted)">ENVOY MESH // MTLS VERIFIED: YES • PACKET LOSS: 0.00% • ARCHITECTURE: RESILIENT</text>
    </g>
    """)
    
    return builder.build()
