import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000'; // Backend URL

export const correctSentence = async (sentence) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/correct_sentence`, { sentence });
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Something went wrong!' };
  }
};
