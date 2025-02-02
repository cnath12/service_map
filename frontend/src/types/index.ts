export interface ServiceConnection {
    source_service: string;
    target_service: string;
    score: number;
    traffic_count: number;
  }
  
  export interface ServiceNode extends d3.SimulationNodeDatum {
    id: string;
    x: number;
    y: number;
  }
  
  export interface ServiceLink extends d3.SimulationLinkDatum<ServiceNode> {
    source: string | ServiceNode;
    target: string | ServiceNode;
    score: number;
  }