// API Configuration for Frontend
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const API_ENDPOINTS = {
    // Auth endpoints
    REGISTER: `${API_BASE_URL}/register`,
    LOGIN: `${API_BASE_URL}/token`,
    ME: `${API_BASE_URL}/users/me`,

    // Learning endpoints
    EXPLAIN: `${API_BASE_URL}/explain`,
    GENERATE_QUIZ: `${API_BASE_URL}/generate-quiz`,
    EVALUATE: `${API_BASE_URL}/evaluate`,
    RETEACH: `${API_BASE_URL}/reteach`,
    PROGRESS: `${API_BASE_URL}/progress`,

    // Health check
    HEALTH: `${API_BASE_URL}/`,
};

export default API_BASE_URL;
