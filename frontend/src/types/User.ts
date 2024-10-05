export interface User {
  id: number;
  username: string;
  roles: string[];
  timezone: string;
  isActive: boolean;
  lastUpdatedAt: string;
  createdAt: string;
}
