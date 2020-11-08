import axios from 'axios';
import mock from '../mock/api';

export const client = axios.create({
    baseURL: 'http://localhost:5000/api',
})
if (JSON.parse(process.env.VUE_APP_USE_MOCK)) {
    mock.run(client)
}
export default {
  setDoToday(id, dotoday) {
    return client.put(`/members/${id}`, {
      dotoday: dotoday
    })
  },
  getMembers() {
    return client.get('/members')
  }
}