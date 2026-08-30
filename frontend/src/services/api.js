import axios from "axios";


const API_URL =
  import.meta.env.VITE_API_URL ||
  "http://localhost:8000/api";


export const askQuestion =
  async (message) => {

    const response =
      await axios.post(
        `${API_URL}/chat`,
        {
          message
        }
      );

    return response.data;
  };