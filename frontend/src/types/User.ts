export interface User {
  id: number | string;
  username: string;
  password: string;
  roles: string[];
  timezone: string;
  active: boolean;
  created_ts: string;
  updated_ts: string;
}
