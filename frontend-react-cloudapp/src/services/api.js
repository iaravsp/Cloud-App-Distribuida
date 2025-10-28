import axios from 'axios'

// Use VITE_API_BASE_URL from your .env file (e.g., http://LOAD_BALANCER_PUBLIC_IP/api)
const baseURL = import.meta.env.VITE_API_BASE_URL;

const api = axios.create({
  baseURL,
  timeout: 10000
})

export default api
