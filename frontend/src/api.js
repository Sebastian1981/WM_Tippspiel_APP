import axios from 'axios'

const API = axios.create({ baseURL: 'http://localhost:8000' })

export const predict = (team_a, team_b, match_phase = 'group') =>
  API.post('/api/predict', { team_a, team_b, match_phase }).then(r => r.data)

export const getMatchdayTips = (day) =>
  API.get(`/api/matchday/${day}`).then(r => r.data)

export const getSpecialQuestions = () =>
  API.get('/api/special-questions').then(r => r.data)

export const addResult = (result) =>
  API.post('/api/results', result).then(r => r.data)

export const getResults = () =>
  API.get('/api/results').then(r => r.data)
