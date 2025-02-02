import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import { ServiceConnection, ServiceNode, ServiceLink } from '../types';

interface ServiceMapProps {
  connections: ServiceConnection[];
}

export const ServiceMap: React.FC<ServiceMapProps> = ({ connections }) => {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current || !connections.length) return;

    const svg = d3.select(svgRef.current);
    const width = 800;
    const height = 600;

    // Clear existing content
    svg.selectAll("*").remove();

    // Create nodes and links for force simulation
    const nodes: ServiceNode[] = Array.from(
      new Set(connections.flatMap(c => [c.source_service, c.target_service]))
    ).map(id => ({ 
      id, 
      x: Math.random() * width, 
      y: Math.random() * height 
    }));

    const links: ServiceLink[] = connections.map(c => ({
      source: c.source_service,
      target: c.target_service,
      score: c.score
    }));

    // Create force simulation
    const simulation = d3.forceSimulation<ServiceNode>(nodes)
      .force('link', d3.forceLink<ServiceNode, ServiceLink>(links)
        .id(d => d.id)
        .distance(100))
      .force('charge', d3.forceManyBody().strength(-200))
      .force('center', d3.forceCenter(width / 2, height / 2));

    // Create container for zoom
    const g = svg.append('g');

    // Add zoom behavior
    svg.call(d3.zoom<SVGSVGElement, unknown>()
      .extent([[0, 0], [width, height]])
      .scaleExtent([0.1, 4])
      .on('zoom', (event) => {
        g.attr('transform', event.transform);
      }));

    // Draw links
    const link = g.selectAll('.link')
      .data(links)
      .join('line')
      .attr('class', 'link')
      .style('stroke-width', d => (d.score || 0) * 5)
      .style('stroke', '#999');

    // Draw nodes
    const node = g.selectAll('.node')
      .data(nodes)
      .join('g')
      .attr('class', 'node')
      .call(d3.drag<any, ServiceNode>()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended));

    // Add circles to nodes
    node.append('circle')
      .attr('r', 5)
      .style('fill', '#69b3a2');

    // Add labels to nodes
    node.append('text')
      .text(d => d.id)
      .attr('dx', 12)
      .attr('dy', 4);

    // Update positions on tick
    simulation.on('tick', () => {
      link
        .attr('x1', d => (d.source as ServiceNode).x)
        .attr('y1', d => (d.source as ServiceNode).y)
        .attr('x2', d => (d.target as ServiceNode).x)
        .attr('y2', d => (d.target as ServiceNode).y);

      node
        .attr('transform', d => `translate(${d.x},${d.y})`);
    });

    // Drag functions
    function dragstarted(event: d3.D3DragEvent<SVGGElement, ServiceNode, ServiceNode>, d: ServiceNode) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event: d3.D3DragEvent<SVGGElement, ServiceNode, ServiceNode>, d: ServiceNode) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragended(event: d3.D3DragEvent<SVGGElement, ServiceNode, ServiceNode>, d: ServiceNode) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    // Cleanup function
    return () => {
      simulation.stop();
    };
  }, [connections]);

  return (
    <svg
        ref={svgRef}
        width="800"
        height="600"
        className="border border-gray-300 rounded-lg"
        aria-label="Service Map Visualization"
      >
      <g className="links" />
      <g className="nodes" />
    </svg>
  );
};

export default ServiceMap;