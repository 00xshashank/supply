import ForceGraph2D from "react-force-graph-2d";
import { useEffect, useRef, useState } from "react";
import { forceManyBody, forceLink, forceCollide } from "d3-force";

/* ---------- Types ---------- */

interface GraphNode {
  id: string;   // elementId
  name?: string;
  labels?: string[];
}

interface GraphLink {
  id: string;
  source: string;
  target: string;
  type?: string;
}

interface Research {
  findings?: string;
  keyMetrics?: {
    metric: string;
    value: string;
    context?: string;
  }[];
  risks?: {
    risk: string;
    severity: string;
    mitigation?: string;
  }[];
  recommendations?: {
    action: string;
    priority: string;
    timeframe?: string;
    rationale?: string;
  }[];
  confidence?: string;
  lastUpdated?: string;
}

/* ---------- Component ---------- */

export default function GraphPage() {
  const [graph, setGraph] = useState<{
    nodes: GraphNode[];
    links: GraphLink[];
  }>({
    nodes: [],
    links: []
  });

  // elementId -> research
  const [researchMap, setResearchMap] =
    useState<Record<string, Research>>({});

  const [selectedNode, setSelectedNode] =
    useState<GraphNode | null>(null);
  const [selectedResearch, setSelectedResearch] =
    useState<Research | null>(null);

  /* ---------- Load Graph ---------- */
  useEffect(() => {
    fetch("http://localhost:8000/api/node-information/", { credentials: "include"})
      .then(res => res.json())
      .then(data => {
        console.log("Graph data loaded:", data);
        setGraph({
          nodes: data.nodes,
          links: data.edges
        });
      })
      .catch(err => console.error("Error loading graph:", err));
  }, []);

  /* ---------- Load Research Once ---------- */
  useEffect(() => {
    fetch("http://localhost:8000/api/research", { credentials: "include"})
      .then(res => res.json())
      .then(data => {
        console.log("Raw research data:", data);
        
        // Extract the content array from the response
        const researchArray = data.content || [];
        console.log("Research array:", researchArray);
        
        // Build a map of nodeId -> research data
        const map: Record<string, Research> = {};
        
        researchArray.forEach((item: any) => {
          console.log("Processing research item:", item);
          if (item.id && item.result) {
            try {
              // Parse the result string - it contains Python dict with single quotes
              let resultStr = item.result;
              
              // Replace Unicode escape sequences
              resultStr = resultStr.replace(/\\u202f/g, ' ');
              
              // Convert Python dict format to JSON
              resultStr = resultStr.replace(/'/g, '"');
              
              const parsed = JSON.parse(resultStr);
              map[item.id] = parsed;
            } catch (e) {
              console.error("Failed to parse research for", item.id, e);
            }
          }
        });
        
        console.log("Research map:", map);
        setResearchMap(map);
      })
      .catch(err => console.error("Error loading research:", err));
  }, []);

  /* ---------- Node Click ---------- */
  const handleNodeClick = (node: GraphNode) => {
    console.log("Selected node:", node);
    console.log("Looking for research with ID:", node.id);
    console.log("Available research IDs:", Object.keys(researchMap));
    
    const research = researchMap[node.id];
    console.log("Found research (raw):", research);
    console.log("Research type:", typeof research);
    console.log("Research keys:", research ? Object.keys(research) : "none");
    
    setSelectedNode(node);
    setSelectedResearch(research || null);
  };

  const graphRef = useRef<any>(null);
  useEffect(() => {
    const fg = graphRef.current;
    if (fg && graph.nodes.length > 0) {
      // Increase repulsion between nodes
      fg.d3Force("charge", forceManyBody().strength(-1000));
      
      // Increase link distance
      fg.d3Force("link", forceLink().distance(400));
      
      // Add collision to prevent overlap (adjust radius based on your node sizes)
      fg.d3Force("collide", forceCollide(20));
      
      // Reheat the simulation to apply changes and spread out
      fg.d3ReheatSimulation();
    }
  }, [graph]);

  /* ---------- Render ---------- */
  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "Arial, sans-serif" }}>
      
      {/* Graph */}
      <div style={{ flex: 2, position: "relative" }}>
        <ForceGraph2D
            ref={graphRef}
            width={window.innerWidth * 0.66}
            height={window.innerHeight}
            graphData={graph}
            onNodeClick={(node: any) => {
              console.log("Node clicked:", node);
              handleNodeClick(node);
            }}
            nodeLabel={(node: any) => node.name || node.labels?.[0] || node.id}
            nodeRelSize={12}  // Slightly increased for larger click areas
            nodeColor={(node: any) => node.id === selectedNode?.id ? "#ff7f0e" : "#1f77b4"}
            nodeCanvasObjectMode={() => "after"}
            nodeCanvasObject={(node: any, ctx, globalScale) => {
                const label = node.name || node.labels?.[0] || node.id;
                const fontSize = 12 / globalScale;

                ctx.font = `${fontSize}px Sans-Serif`;
                ctx.fillStyle = "black";
                ctx.textAlign = "center";
                ctx.textBaseline = "top";
                ctx.fillText(label, node.x, node.y + 15);
            }}
            
            d3AlphaDecay={0.02}
            d3VelocityDecay={0.3}
            
            linkColor={() => "#999"}
            linkWidth={1}
            
            enableNodeDrag={true}
            enableZoomInteraction={true}
            enablePanInteraction={true}
            warmupTicks={200}  // Increased for better initial spreading
            cooldownTicks={300}  // Increased for more stabilization time
            onEngineStop={() => console.log("Graph stabilized")}
            />
      </div>

      {/* Side Panel */}
      <div
        style={{
          flex: 1,
          padding: "24px",
          borderLeft: "2px solid #ddd",
          overflowY: "auto",
          backgroundColor: "#f5f5f5"
        }}
      >
        {!selectedNode && (
          <div style={{ 
            color: "#666", 
            textAlign: "center", 
            marginTop: "40px",
            fontSize: "16px"
          }}>
            👈 Click on a node to view research details
          </div>
        )}

        {selectedNode && (
          <>
            {/* Header Section */}
            <div style={{
              backgroundColor: "white",
              padding: "20px",
              borderRadius: "8px",
              marginBottom: "16px",
              boxShadow: "0 2px 4px rgba(0,0,0,0.1)"
            }}>
              <h2 style={{ margin: "0 0 12px 0", color: "#1f77b4" }}>
                {selectedNode.name || "Node Details"}
              </h2>
              <div style={{ fontSize: "12px", color: "#666" }}>
                <div><strong>Element ID:</strong> {selectedNode.id}</div>
                {selectedNode.labels && selectedNode.labels.length > 0 && (
                  <div style={{ marginTop: "4px" }}>
                    <strong>Labels:</strong> {selectedNode.labels.join(", ")}
                  </div>
                )}
              </div>
            </div>

            {!selectedResearch && (
              <div style={{
                backgroundColor: "#fff3cd",
                padding: "16px",
                borderRadius: "8px",
                border: "1px solid #ffc107",
                color: "#856404"
              }}>
                ⚠️ No research data available for this node
              </div>
            )}

            {/* Findings */}
            {selectedResearch?.findings && (
              <div style={{
                backgroundColor: "white",
                padding: "20px",
                borderRadius: "8px",
                marginBottom: "16px",
                boxShadow: "0 2px 4px rgba(0,0,0,0.1)"
              }}>
                <h3 style={{ 
                  margin: "0 0 12px 0", 
                  color: "#333",
                  fontSize: "18px",
                  borderBottom: "2px solid #1f77b4",
                  paddingBottom: "8px"
                }}>
                  📊 Findings
                </h3>
                <p style={{ margin: 0, lineHeight: "1.6", color: "#444" }}>
                  {selectedResearch.findings}
                </p>
              </div>
            )}

            {/* Key Metrics */}
            {selectedResearch?.keyMetrics && selectedResearch.keyMetrics.length > 0 && (
              <div style={{
                backgroundColor: "white",
                padding: "20px",
                borderRadius: "8px",
                marginBottom: "16px",
                boxShadow: "0 2px 4px rgba(0,0,0,0.1)"
              }}>
                <h3 style={{ 
                  margin: "0 0 12px 0", 
                  color: "#333",
                  fontSize: "18px",
                  borderBottom: "2px solid #1f77b4",
                  paddingBottom: "8px"
                }}>
                  📈 Key Metrics
                </h3>
                {selectedResearch.keyMetrics.map((m, i) => (
                  <div key={i} style={{
                    backgroundColor: "#f8f9fa",
                    padding: "12px",
                    borderRadius: "6px",
                    marginBottom: "10px",
                    borderLeft: "4px solid #28a745"
                  }}>
                    <div style={{ fontWeight: "bold", color: "#333", marginBottom: "4px" }}>
                      {m.metric}
                    </div>
                    <div style={{ fontSize: "16px", color: "#1f77b4", fontWeight: "600" }}>
                      {m.value}
                    </div>
                    {m.context && (
                      <div style={{ fontSize: "13px", color: "#666", marginTop: "6px" }}>
                        {m.context}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}

            {/* Risks */}
            {selectedResearch?.risks && selectedResearch.risks.length > 0 && (
              <div style={{
                backgroundColor: "white",
                padding: "20px",
                borderRadius: "8px",
                marginBottom: "16px",
                boxShadow: "0 2px 4px rgba(0,0,0,0.1)"
              }}>
                <h3 style={{ 
                  margin: "0 0 12px 0", 
                  color: "#333",
                  fontSize: "18px",
                  borderBottom: "2px solid #dc3545",
                  paddingBottom: "8px"
                }}>
                  ⚠️ Risks
                </h3>
                {selectedResearch.risks.map((r, i) => (
                  <div key={i} style={{
                    backgroundColor: "#fff5f5",
                    padding: "12px",
                    borderRadius: "6px",
                    marginBottom: "10px",
                    borderLeft: `4px solid ${
                      r.severity === "High" ? "#dc3545" : 
                      r.severity === "Medium" ? "#ffc107" : "#28a745"
                    }`
                  }}>
                    <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "4px" }}>
                      <span style={{ fontWeight: "bold", color: "#333" }}>{r.risk}</span>
                      <span style={{
                        fontSize: "12px",
                        padding: "2px 8px",
                        borderRadius: "12px",
                        backgroundColor: 
                          r.severity === "High" ? "#dc3545" : 
                          r.severity === "Medium" ? "#ffc107" : "#28a745",
                        color: "white"
                      }}>
                        {r.severity}
                      </span>
                    </div>
                    {r.mitigation && (
                      <div style={{ fontSize: "13px", color: "#666", marginTop: "6px" }}>
                        <strong>Mitigation:</strong> {r.mitigation}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}

            {/* Recommendations */}
            {selectedResearch?.recommendations && selectedResearch.recommendations.length > 0 && (
              <div style={{
                backgroundColor: "white",
                padding: "20px",
                borderRadius: "8px",
                marginBottom: "16px",
                boxShadow: "0 2px 4px rgba(0,0,0,0.1)"
              }}>
                <h3 style={{ 
                  margin: "0 0 12px 0", 
                  color: "#333",
                  fontSize: "18px",
                  borderBottom: "2px solid #17a2b8",
                  paddingBottom: "8px"
                }}>
                  💡 Recommendations
                </h3>
                {selectedResearch.recommendations.map((rec, i) => (
                  <div key={i} style={{
                    backgroundColor: "#e7f3ff",
                    padding: "12px",
                    borderRadius: "6px",
                    marginBottom: "10px",
                    borderLeft: `4px solid ${
                      rec.priority === "High" ? "#dc3545" : 
                      rec.priority === "Medium" ? "#ffc107" : "#28a745"
                    }`
                  }}>
                    <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "4px" }}>
                      <span style={{ fontWeight: "bold", color: "#333" }}>{rec.action}</span>
                      <span style={{
                        fontSize: "12px",
                        padding: "2px 8px",
                        borderRadius: "12px",
                        backgroundColor: 
                          rec.priority === "High" ? "#dc3545" : 
                          rec.priority === "Medium" ? "#ffc107" : "#28a745",
                        color: "white"
                      }}>
                        {rec.priority}
                      </span>
                    </div>
                    {rec.timeframe && (
                      <div style={{ fontSize: "12px", color: "#666", marginTop: "4px" }}>
                        <strong>⏱️ Timeframe:</strong> {rec.timeframe}
                      </div>
                    )}
                    {rec.rationale && (
                      <div style={{ fontSize: "13px", color: "#555", marginTop: "6px" }}>
                        {rec.rationale}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}

            {/* Footer Info */}
            {(selectedResearch?.confidence || selectedResearch?.lastUpdated) && (
              <div style={{
                backgroundColor: "white",
                padding: "16px",
                borderRadius: "8px",
                boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
                fontSize: "13px",
                color: "#666"
              }}>
                {selectedResearch?.confidence && (
                  <div style={{ marginBottom: "8px" }}>
                    <strong>Confidence Level:</strong> {selectedResearch.confidence}
                  </div>
                )}
                {selectedResearch?.lastUpdated && (
                  <div>
                    <strong>Last Updated:</strong>{" "}
                    {new Date(selectedResearch.lastUpdated).toLocaleString()}
                  </div>
                )}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}