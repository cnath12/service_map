import { ServiceConnection } from './types';

export const mockServiceConnections: ServiceConnection[] = [
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

export const createMockServiceConnection = (
  source: string,
  target: string,
  score: number = 0.8,
  traffic_count: number = 100
): ServiceConnection => ({
  source_service: source,
  target_service: target,
  score,
  traffic_count
});