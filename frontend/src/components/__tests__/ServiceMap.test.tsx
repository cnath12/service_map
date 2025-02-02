import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { ServiceMap } from '../ServiceMap';

const mockConnections = [
  {
    source_service: "Login Service",
    target_service: "Auth",
    score: 0.8,
    traffic_count: 100
  },
  {
    source_service: "Auth",
    target_service: "User Profile DB",
    score: 0.6,
    traffic_count: 75
  }
];

describe('ServiceMap', () => {
  it('renders without crashing', () => {
    const { container } = render(<ServiceMap connections={[]} />);
    const svg = container.querySelector('svg');
    expect(svg).toBeInTheDocument();
    expect(svg).toHaveAttribute('width', '800');
    expect(svg).toHaveAttribute('height', '600');
  });

  it('renders with connections', () => {
    const { container } = render(<ServiceMap connections={mockConnections} />);
    
    // Check SVG attributes
    const svg = container.querySelector('svg');
    expect(svg).toHaveAttribute('width', '800');
    expect(svg).toHaveAttribute('height', '600');
    
    // Check if service names are rendered
    expect(screen.getByText('Login Service')).toBeInTheDocument();
    expect(screen.getByText('Auth')).toBeInTheDocument();
    expect(screen.getByText('User Profile DB')).toBeInTheDocument();
  });
});