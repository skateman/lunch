const prod = {
  API_URL: ''
};

const dev = {
  API_URL: 'http://localhost:8001'
};

export const config = process.env.NODE_ENV === 'development' ? dev : prod;
