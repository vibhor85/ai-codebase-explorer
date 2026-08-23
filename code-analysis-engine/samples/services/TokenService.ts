import { logDetails } from '../utils/Logger';

export const tokenCall = () => {
  logDetails('Logggin token');
  return { token: 'Bearer token' };
};
