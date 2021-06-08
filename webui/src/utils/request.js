import axios from 'axios'

const http = axios.create({
  baseURL: '',
  timeout: 60 * 5 * 1000
})
http.interceptors.request.use(
  config => {
    config.headers = {
      'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1lIjoidGVzdCIsImV4cCI6MTYxMTUwMDM3NCwiaXNzIjoiSnd0S2V5TmFtZSIsImF1ZCI6Ikp3dEtleU5hbWUifQ.8nnKmig8Ar5uAC5WDZLxJZEl9mEpPsqbN4YrBt-H_UQ'
    }
    return config
  }, error => {
    console.log(error)
    return Promise.reject(error)
  }
)

http.interceptors.response.use(response => {
  return response.data
})

export default http
