import { userAPICall } from './UserRepository';

export const getUser = () => {
  console.log('User Fetching');
  return userAPICall();
};
