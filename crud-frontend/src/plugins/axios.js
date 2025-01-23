import axios from 'axios'

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000/',
  timeout: 1000,
  headers: { 'Content-Type': 'application/json' },
})

export default {
  install: (app) => {
    app.config.globalProperties.$axios = axiosInstance
  },
}
